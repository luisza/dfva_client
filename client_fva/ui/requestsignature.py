import os
from base64 import b64decode
from pathlib import Path

import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem, QCompleter

from client_fva.models.ContactDropDown import ContactModel
from client_fva.models.MyRequest import MyRequestModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.filechooser import FileChooser
from client_fva.ui.requestsignatureui import Ui_RequestSignature
from client_fva.user_settings import UserSettings


class PersonSignOpers(QThread):
    has_result = pyqtSignal(int)
    has_changes = pyqtSignal(str, int, bool, str)
    remove_check = pyqtSignal(str)

    def __init__(self, person, identifications, user, data):
        self.data = data
        self.identifications = identifications
        self.person = person
        super(PersonSignOpers, self).__init__()
        self.result = {}
        self.pending_check = {}
        self.wait_time = UserSettings.getInstance().check_wait_time
        storage = SessionStorage.getInstance()
        self.myrequest = MyRequestModel(db=storage.db, user=user)
        self.logs_id = {}

    def log_transaction(self, identification, data):
        self.has_changes.emit(identification, data['status'], False, data['status_text'])
        self.logs_id[identification] = self.myrequest.add_myrequest(identification, 'Firmado', '', '', signed_document_path="",
                      transaction_status=data['status'], transaction_text=data['status_text'])

    def log_check_transaction(self, identification, data):
        self.has_changes.emit(identification, data['status'], data['received_notification'], data['status_text'])
        self.myrequest.update_myrequest(self.logs_id[identification], transaction_status=data['status'],
                                        transaction_text=data['status_text'])

    def sign_document(self, identification, data):
        self.result[identification] = self.person.sign(identification, data["document"], data["resume"],
                                       _format=data["_format"], file_path=data["file_path"],
                                       algorithm=data["algorithm"], is_base64=data["is_base64"],
                                       wait=False, extras=data["extras"])
        self.log_transaction(identification, self.result[identification])
        status = self.result[identification]['status']
        if status == 0:
            pending_check = self.result[identification]['id']
            received = False
            while received:
                self.result[identification] = self.person.sign_authenticate(pending_check)
                self.log_check_transaction(identification, self.result[identification])
                status=self.result[identification]['status']
                if self.result[identification]['received_notification']:
                    received = True
                    if self.result[identification].get('signed_document'):
                        with open(data["save_path"], "wb") as arch:
                            arch.write(b64decode(self.result["signed_document"]))
                    self.remove_check.emit(identification)
            time.sleep(self.wait_time)
        return status

    def run(self):
        data = dict(**self.data)
        pending = []
        for identification in self.identifications:
            status = self.sign_document(identification, data)
            if status == 0:
                data["file_path"] = data["save_path"]
            else:
                pending.append(identification)

        # second change
        for identification in pending:
            status = self.sign_document(identification, data)
            if status == 0:
                data["file_path"] = data["save_path"]
        self.has_result.emit()


class RequestSignature(QWidget, Ui_RequestSignature):

    CONNECTING = 0
    CONNECTED = 1
    REJECTED = 2
    ERROR = 3

    def __init__(self, widget, main_app, db, index):
        Ui_RequestSignature.__init__(self)
        super().__init__(widget)
        self.widget = widget
        self.main_app = main_app
        self.setupUi(widget)
        self.session_storage = SessionStorage.getInstance()
        self.person = self.session_storage.persons[index]
        self.user = self.session_storage.users[index]
        self.contacts_count = 0
        self.settings = UserSettings.getInstance()
        self.browseFiles.clicked.connect(self.get_document_path)
        self.filesWidget.set_parent(self)

        self.contacts_model = ContactModel(user=self.user, db=db)

        self.sign_list = []
        self.status_widgets = {}

        completer = QCompleter()
        completer.setModel(self.contacts_model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.search.setCompleter(completer)
        self.add_contact.clicked.connect(lambda: self.add_contact_to_list())
        self.requestSignature.clicked.connect(self.request_signature)
        self.initialize()

    def add_file(self, path):
        if path:  # only add it to the list if something was actually selected - none if user clicked cancel
            if not self.filesWidget.count():  # only one file can be added at the time
                self.path = path
                self.filesWidget.addItem(path)
            else:
                QtWidgets.QMessageBox.critical(self.widget, "Solo un documento permitido",
                                               "Solo un documento puede ser validado/firmado a la vez.")


    @pyqtSlot(name='get_document_path')
    def get_document_path(self):

        d = FileChooser()
        path = d.openFileNameDialog()
        self.add_file(path)
        del d

    def initialize(self):
        self.contacts.setColumnCount(3)
        self.contacts.setHorizontalHeaderItem(0, QTableWidgetItem("Estado"))
        self.contacts.setHorizontalHeaderItem(1, QTableWidgetItem("Identificación"))
        self.contacts.setHorizontalHeaderItem(2, QTableWidgetItem("Nombre"))
        self.contacts.resizeColumnsToContents()
        self.contacts_count = 0
        self.contacts.contextMenuEvent = self.context_element_menu_event

    def inactive_btn(self):
        self.add_contact.setEnabled(False)
        self.requestSignature.setEnabled(False)

    def active_btn(self):
        self.add_contact.setEnabled(True)
        self.requestSignature.setEnabled(True)

    def add_contact_to_list(self):
        txt = self.search.text()
        id = self.contacts_model.deserialize_contact(txt)
        if id:
            if id not in self.sign_list:
                if id != txt:
                    self.insert_item(id, txt)
                else:
                    self.insert_item(id, '')
                self.sign_list.append(id)
                self.search.setText('')
            else:
                QtWidgets.QMessageBox.warning(self.widget, 'Contacto ya existente',
                                              "El contacto seleccionado fue agregado a la lista anteriormente.")

        else:
            QtWidgets.QMessageBox.warning(self.widget, 'Contacto no identificado',
                 "Lo ingresado no es un nombre de contacto o un número de identificación válido.")

    def insert_item(self, identification, name):

        status_widget = QTableWidgetItem()
        status_widget.setIcon(QtGui.QIcon(":/images/autentication.png"))

        self.contacts.insertRow(self.contacts.rowCount())
        self.contacts.setItem(self.contacts_count, 0, status_widget)
        self.contacts.setItem(self.contacts_count, 1, QTableWidgetItem(identification))
        self.contacts.setItem(self.contacts_count, 2, QTableWidgetItem(name))
        self.contacts_count += 1
        self.status_widgets[identification] = status_widget
        self.contacts.resizeColumnsToContents()

    def change_person_status(self,status_widget,  status, error_text="Error o rechazo por parte del usuario"):
        if status == self.CONNECTING:
            status_widget.setIcon(QtGui.QIcon(":/images/connecting.png"))
            status_widget.setToolTip('Conectando al servicio de firmado')
        elif status == self.CONNECTED:
            status_widget.setIcon(QtGui.QIcon(":/images/connected.png"))
            status_widget.setToolTip('Persona autenticada satisfactoriamente')
        elif status == self.REJECTED:
            status_widget.setIcon(QtGui.QIcon(":/images/rejected.png"))
            status_widget.setToolTip('Persona autenticada satisfactoriamente')
        elif status == self.ERROR:
            status_widget.setIcon(QtGui.QIcon(":/images/error.png"))
            status_widget.setToolTip(error_text)

    def context_element_menu_event(self, pos):
        if self.contacts.selectedIndexes():
            selected = self.contacts.currentIndex()
            if selected.isValid():
                row, column = selected.row(), selected.column()
                menu = QtWidgets.QMenu()
                menu.setStyleSheet("QMenu::item{color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);}")
                delete_action = menu.addAction("Delete")
                delete_action.setIcon(QtGui.QIcon(":images/delete.png"))
                action = menu.exec_(self.contacts.mapToGlobal(pos.pos()))
                if action == delete_action:
                    self.delete_element(row)

    def delete_element(self, row):
        self.contacts.removeRow(row)
        self.sign_list.pop(row)
        self.contacts_count -= 1

    def update_process_bar(self, value, text):
        self.progress.setValue(value)
        if text:
            self.progress.setFormat(text)

    def request_signature(self):
        self.start_sign()
        self.sign_document()
        self.end_sign()

    def start_sign(self):
        self.inactive_btn()
        self.progress.setRange(0, len(self.sign_list))

    def end_sign(self):
        self.update_process_bar(len(self.sign_list), 'Solicitud de firmado completa')
        self.active_btn()

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
        _format = self.get_format()
        if _format is None:
            QtWidgets.QMessageBox.critical(self.widget, "Formato de archivo no soportado",
                                           "Lo lamentamos, el archivo seleccionado no tiene un formato soportado por "
                                           "este sistema.")
            return
        resume = self.resumen.toPlainText()
        #    def __init__(self, person, identifications, user, data):
        self.pso = PersonSignOpers(self.person, self.sign_list, self.user,
                                  {"document": None, "resume": resume,
                                   "_format": _format, "algorithm": self.settings.algorithm, "is_base64": False,
                                   "wait": False, "extras": extras,  "file_path": self.path,
                                   "save_path": self.get_save_document_path(), "file_name": self.get_document_name()})

        self.pso.has_result.connect(self.end_sign)
        self.pso.has_changes.connect(self.check_transaction_change)
        self.pso.remove_check.connect(self.check_transaction_end)
        self.pso.start()



    def check_transaction_end(self, identification):
        self.sign_pending -= 1
        self.update_process_bar(len(self.sign_list) - self.sign_pending,
                                'Solicitudes faltantes %d'%self.sign_pending)

    def check_transaction_change(self, identification, status, recieved, text):
        # transaction_status
        icon_status = 0
        icon_tooltip = ''
        if status == 0:
            if recieved:
                icon_status = self.CONNECTED
            else:
                icon_status = self.CONNECTING
        elif status == 2:
            icon_status = self.REJECTED
            icon_tooltip = text
        else:
            icon_status = self.ERROR
            icon_tooltip = text
        self.change_person_status(self.status_widgets[identification], icon_status, icon_tooltip)

    def clean_table(self):
        for x in range(len(self.sign_list)):
            self.contacts.removeRow(0)
            self.sign_list.pop()
        self.contacts.setRowCount(0)
        self.contacts_count=0

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

    def get_format(self):
        extension = "".join(Path(self.path).suffixes)
        extension = extension.split('.')[-1].lower().replace(".", "")
        support_extension = self.settings.file_supported_extensions
        if extension in support_extension:
            extension = support_extension[extension]
        else:
            extension = None
        return extension
