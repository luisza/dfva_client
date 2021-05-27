import os
from pathlib import Path
from base64 import b64decode
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget

from client_fva.models.MySign import MySignModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.filechooser import FileChooser
from client_fva.ui.signvalidateui import Ui_SignValidate
from client_fva.ui.validationinformation import ValidationInformation
from client_fva.ui.validationinformationcertificate import ValidationInformationCertificate
from client_fva.user_settings import UserSettings


class PersonSignOpers(QThread):
    has_result = pyqtSignal(int)

    def __init__(self, tid, person, user, data):
        self.data = data
        self.person = person
        super(PersonSignOpers, self).__init__()
        self.tid = tid
        self.result = None
        self.session_storage = SessionStorage.getInstance()
        self.mysign = MySignModel(db=self.session_storage.db, user=user)

    def run(self):
        data = self.data
        mid = self.mysign.add_mysign(data["identification"], data["file_path"], data["file_name"],
                                     signed_document_path=data["save_path"])
        self.result = self.person.sign(data["identification"], data["document"], data["resume"],
                                       _format=data["_format"], file_path=data["file_path"],
                                       algorithm=data["algorithm"], is_base64=data["is_base64"],
                                       wait=data["wait"], extras=data["extras"])

        self.mysign.update_mysign(mid, transaction_status=self.result["status"], transaction_text=self.result["status_text"])

        if self.result.get('signed_document'):
            with open(data["save_path"], "wb") as arch:
                arch.write(b64decode(self.result["signed_document"]))

        self.has_result.emit(self.tid)


class PersonValidateOpers(QThread):
    has_result = pyqtSignal(int)

    def __init__(self, tid, person, data):
        self.data = data
        self.person = person
        super(PersonValidateOpers, self).__init__()
        self.tid = tid
        self.result = None

    def run(self):
        self.result = self.person.validate(self.data["document"], self.data["file_path"], self.data["algorithm"],
                                           self.data["is_base64"], self.data["_format"])
        self.has_result.emit(self.tid)


class SignValidate(QWidget, Ui_SignValidate):

    def __init__(self, widget, main_app, serial):
        Ui_SignValidate.__init__(self)
        super().__init__(widget)
        self.storage = SessionStorage.getInstance()
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        self.settings = UserSettings.getInstance()
        self.filesWidget.set_parent(self)
        self.path = None
        self.serial = serial
        self.person = self.storage.session_info[serial]['personclient']
        self.browseFiles.clicked.connect(self.get_document_path)
        self.validate.clicked.connect(self.validate_document)
        self.sign.clicked.connect(self.sign_document)
        self.opers = []

        self.filesWidget.contextMenuEvent = self.context_file_menu_event

        self.person.process_status.connect(self.update_process_bar)
        self.person.end_sign.connect(self.end_sign)
        self.person.end_validate.connect(self.end_validate)

    def disconnect(self):
        self.person.process_status.disconnect(self.update_process_bar)
        self.person.end_sign.disconnect(self.end_sign)
        self.person.end_validate.disconnect(self.end_validate)

    def context_file_menu_event(self, pos):
        if self.filesWidget.selectedIndexes():
            selected = self.filesWidget.currentRow()  # user can only select one file at the time
            menu = QtWidgets.QMenu()
            menu.setStyleSheet("QMenu::item{color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);}")
            delete_action = menu.addAction("Delete")
            delete_action.setIcon(QtGui.QIcon(":images/delete.png"))
            action = menu.exec_(self.filesWidget.mapToGlobal(pos.pos()))
            if action == delete_action:
                self.delete_file(selected)

    def add_file(self, path):
        if path:  # only add it to the list if something was actually selected - none if user clicked cancel
            if not self.filesWidget.count():  # only one file can be added at the time
                self.path = path
                self.filesWidget.addItem(path)
            else:
                QtWidgets.QMessageBox.critical(self.widget, "Solo un documento permitido",
                                               "Solo un documento puede ser validado/firmado a la vez.")

    def delete_file(self, selected_row):
        self.path = None
        self.filesWidget.takeItem(selected_row)

    def clean(self):
        self.resumen.setText("")
        self.razon.setText("")
        self.lugar.setText("")
        self.path = None
        self.filesWidget.clear()
        self.signValidateProgressBar.setValue(0)

    def get_format(self, validate=False):
        extension = "".join(Path(self.path).suffixes)
        extension = extension.split('.')[-1].lower().replace(".", "")
        support_extension = self.settings.file_supported_extensions
        if validate:
            support_extension = self.settings.validate_supported_extensions
        if extension in support_extension:
            extension = support_extension[extension]
        else:
            extension = None
        return extension

    @pyqtSlot(name="get_document_path")
    def get_document_path(self):
        d = FileChooser()
        path = d.openFileNameDialog()
        self.add_file(path)
        del d

    @pyqtSlot(name="validate_document")
    def validate_document(self):
        if self.path is None:
            QtWidgets.QMessageBox.critical(self.widget, "Sin documento seleccionado",
                                           "Debe seleccionar un documento para llevar a cabo la acción seleccionada.")
            return
        _format = self.get_format(validate=True)
        if _format is None:
            QtWidgets.QMessageBox.critical(self.widget, "Formato de archivo no soportado",
                                           "Lo lamentamos, el archivo seleccionado no tiene un formato soportado por "
                                           "este sistema.")
            return
        validateprocess = PersonValidateOpers(len(self.opers), self.person, {"document": None, "file_path": self.path,
                                                                             "algorithm": self.settings.algorithm,
                                                                             "is_base64": False, "_format": _format})
        validateprocess.has_result.connect(self.validate_result)
        validateprocess.start()
        self.opers.append(validateprocess)

    @pyqtSlot()
    def end_sign(self):
        self.clean()
        QtWidgets.QMessageBox.information(self.widget, "Documento firmado con éxito",
                                          "El documento seleccionado fue firmado y guardado con éxito en la carpeta de "
                                          "destino.")

    def end_validate(self):
        self.clean()

    def get_document_name(self, signed=False):
        name = Path(self.path).name
        if signed:
            l = name.split(".")
            l.insert(-1, "-firmado.")
            name = "".join(l)
        return name

    def get_save_document_path(self):
        prefix = os.getcwd()
        signed = True
        if self.settings.save_signed_docs_path:
            prefix = self.settings.save_signed_docs_path
            signed = False
        return str(os.path.abspath(os.path.join(prefix, self.get_document_name(signed))))

    @pyqtSlot(name="sign_document")
    def sign_document(self):
        if self.path is None:
            QtWidgets.QMessageBox.critical(self.widget, "Sin documento seleccionado",
                                           "Debe seleccionar un documento para llevar a cabo la acción seleccionada.")
            return

        extras = {}
        if self.get_format() == "pdf":
            if self.razon.text() == "" and self.lugar.text() == "":
                QtWidgets.QMessageBox.critical(self.widget, "Datos faltantes",
                                               "Para firmar un documento PDF se debe indicar el lugar y la razón "
                                               "de la firma.")
                return
            extras["reason"] = self.razon.text()
            extras["place"] = self.lugar.text()
        self.signValidateProgressBar.setRange(0, 6)
        _format = self.get_format()
        if _format is None:
            QtWidgets.QMessageBox.critical(self.widget, "Formato de archivo no soportado",
                                           "Lo lamentamos, el archivo seleccionado no tiene un formato soportado por "
                                           "este sistema.")
            return
        resume = self.resumen.toPlainText()
        persont = PersonSignOpers(len(self.opers), self.person, self.storage.session_info[self.serial]['user'],
                                  {"identification": self.person.person, "document": None, "resume": resume,
                                   "_format": _format, "algorithm": self.settings.algorithm, "is_base64": False,
                                   "wait": True, "extras": extras,  "file_path": self.path,
                                   "save_path": self.get_save_document_path(), "file_name": self.get_document_name()})
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
        if self.opers[tid].data['_format'] == 'certificate':
            vi = ValidationInformationCertificate(self.widget, self.main_app)
            vi.status.setText(self.opers[tid].result['status_text'])
            vi.set_status_icon(self.opers[tid].result['was_successfully'])
            vi.add_owner(self.opers[tid].result)
            vi.show()
        else:
            vi = ValidationInformation(self.widget, self.main_app)
            vi.status.setText(self.opers[tid].result['status_text'])
            if 'validation_data' in self.opers[tid].result:
                if 'firmas' in self.opers[tid].result['validation_data']:
                    for signer in self.opers[tid].result['validation_data']['firmas']:
                        vi.add_signer(signer)
                if 'resumen' in self.opers[tid].result['validation_data']:
                   vi.add_resumen(self.opers[tid].result['validation_data']['resumen'])
                if 'errores' in self.opers[tid].result['validation_data']:
                    vi.add_errors(self.opers[tid].result['validation_data']['errores'])
                vi.set_status_icon(self.opers[tid].result['status'])
            elif 'errores' in self.opers[tid].result:
                QtWidgets.QMessageBox.critical(self.widget, "Problemas validando el documento",
                                               self.opers[tid].result['errores'])
                vi.set_status_icon(1)
            vi.show()


