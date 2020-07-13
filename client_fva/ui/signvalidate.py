import os
from pathlib import Path
from base64 import b64decode
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget

from client_fva.models.MySign import MySignModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.filechooser import FileChooser
from client_fva.ui.signvalidateui import Ui_SignValidate
from client_fva.user_settings import UserSettings


class PersonSignOpers(QThread):
    has_result = pyqtSignal(int)

    def __init__(self, tid, person, user, data):
        self.data=data
        self.person = person
        super(PersonSignOpers, self).__init__()
        self.tid = tid
        self.result = None
        storage = SessionStorage.getInstance()
        self.mysign = MySignModel(db=storage.db, user=user)

    def run(self):
        data = self.data

        mid = self.mysign.add_mysign(data['identification'], data['file_path'], data['file_name'],
                                     sign_document_path=data['save_path'])
        self.result = self.person.sign(data['identification'],
            data['document'], data['resume'], _format=data['_format'], file_path=data['file_path'],
            algorithm=data['algorithm'], is_base64=data['is_base64'], wait=data['wait'], extras=data['extras']
        )
        self.mysign.update_mysign(mid, transaction_id=self.result['status'], transaction_text=self.result['status_text'])

        with open(data['save_path'], 'wb') as arch:
            arch.write(b64decode(self.result['sign_document']))

        self.has_result.emit(self.tid)


class PersonValidateOpers(QThread):
    has_result = pyqtSignal(int)

    def __init__(self, tid, person, data):
        self.data=data
        self.person = person
        super(PersonValidateOpers, self).__init__()
        self.tid = tid
        self.result = None


    def run(self):
        self.result = self.person.validate(self.data['document'], self.data['file_path'], self.data['algorithm'],
                             self.data['is_base64'], self.data['_format'])
        self.has_result.emit(self.tid)


class SignValidate(QWidget, Ui_SignValidate):

    def __init__(self, widget, main_app, index=None, storage=None):
        Ui_SignValidate.__init__(self)
        super().__init__(widget)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        self.settings = UserSettings.getInstance()
        self.filesWidget.set_parent(self)
        self.path = None
        self.index = index
        self.session_storage = storage
        self.person = storage.persons[index]
        self.browseFiles.clicked.connect(self.get_document_path)
        self.validate.clicked.connect(self.validate_document)
        self.sign.clicked.connect(self.sign_document)
        self.opers = []

        self.person.process_status.connect(self.update_process_bar)
        self.person.end_sign.connect(self.end_sign)
        self.person.end_validate.connect(self.end_validate)

    def add_file(self, path):
        self.path = path
        self.filesWidget.addItem(path)

    def clean(self):
        self.resumen.setText("")
        self.razon.setText("")
        self.lugar.setText("")
        self.path = None
        self.filesWidget.clear()
        self.signValidateProgressBar.setValue(0)

    def get_format(self, validate=False):
        extension = "".join(Path(self.path).suffixes)
        extension = extension.lower().replace('.', '')
        support_extension = self.settings.file_supported_extensions
        if validate:
            support_extension = self.settings.validate_supported_extensions
        if extension in support_extension:
            extension = support_extension[extension]
        else:
            extension = None
        return extension

    @pyqtSlot(name='get_document_path')
    def get_document_path(self):

        d = FileChooser()
        path = d.openFileNameDialog()
        self.add_file(path)
        del d

    @pyqtSlot(name='validate_document')
    def validate_document(self):
        if self.path is None:
            QtWidgets.QMessageBox.warning(None, "Sin documento seleccionado", 'Debe seleccionar un documento' )
            return
        _format = self.get_format(validate=True)
        if _format is None:
            QtWidgets.QMessageBox.warning(None, "Formato de archivo no soportado",
                                          'Lo lamentamos, este archivo no tiene un formato soportado por este sistema')
            return
        validateprocess = PersonValidateOpers(len(self.opers), self.person, {'document': None, 'file_path': self.path,
            'algorithm': self.settings.algorithm, 'is_base64': False, '_format': _format })
        validateprocess.has_result.connect(self.validate_result)
        validateprocess.start()
        self.opers.append(validateprocess)

    @pyqtSlot()
    def end_sign(self):
        self.clean()
        QtWidgets.QMessageBox.information(None, "Documento firmado con éxito",
                                      'El documento fue firmado y guardado con éxito en la carpeta de destino')

    def end_validate(self):
        self.clean()

    def get_document_name(self, signed=False):
        name = Path(self.path).name
        if signed:
            l = name.split('.')
            l.insert(-1, '-firmado.')
            name = "".join(l)
        return name

    def get_save_document_path(self):
        prefix = os.getcwd()
        signed = True
        if self.settings.save_signed_docs_path:
            prefix = self.settings.save_signed_docs_path
            signed = False
        return str(os.path.abspath(os.path.join(prefix, self.get_document_name(signed))))

    @pyqtSlot(name='sign_document')
    def sign_document(self):
        if self.path is None:
            QtWidgets.QMessageBox.warning(None, "Sin documento seleccionado", 'Debe seleccionar un documento' )
            return

        extras = {}
        if self.get_format() == 'pdf':
            if self.razon.text() == '' and self.lugar.text() == '':
                QtWidgets.QMessageBox.warning(None, "Datos faltantes", 'Cuando firma un documento PDF debe indicar el lugar y la razón de firma')
                return
            extras['reason'] = self.razon.text()
            extras['place'] = self.lugar.text()
        self.signValidateProgressBar.setRange(0, 6)
        _format = self.get_format()
        if _format is None:
            QtWidgets.QMessageBox.warning(None, "Formato de archivo no soportado",
                                          'Lo lamentamos, este archivo no tiene un formato soportado por este sistema')
            return
        resume = self.resumen.toPlainText()
        persont = PersonSignOpers(len(self.opers), self.person, self.session_storage.users[self.index],
                                  {'identification': self.person.person, 'document': None, 'resume': resume,
                                      '_format': _format, 'algorithm': self.settings.algorithm, 'is_base64': False,
                                   'wait': True, 'extras': extras,  'file_path': self.path,
                                   'save_path': self.get_save_document_path(), 'file_name': self.get_document_name()})

        persont.has_result.connect(self.sign_result)
        persont.start()
        self.opers.append(persont)

    def update_process_bar(self, value, text):
        self.signValidateProgressBar.setValue(value)
        if text:
            self.signValidateProgressBar.setFormat(text)

    def sign_result(self, tid):
        print(self.opers[tid].result)

    def validate_result(self, tid):
        print(self.opers[tid].result)