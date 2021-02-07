import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem

from client_fva.models.ContactDropDown import ContactModel
from client_fva.models.MyRequest import MyRequestModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.requestauthenticationui import Ui_RequestAuthentication
from client_fva.user_settings import UserSettings


class PersonAuthenticationOpers(QThread):
    has_result = pyqtSignal(int)
    has_changes = pyqtSignal(str, int, bool, str)
    remove_check = pyqtSignal(str)

    def __init__(self, tid, person, identifications, user):
        self.identifications = identifications
        self.person = person
        super(PersonAuthenticationOpers, self).__init__()
        self.tid = tid
        self.result = None
        self.pending_check = {}
        self.wait_time = UserSettings.getInstance().check_wait_time
        storage = SessionStorage.getInstance()
        self.myrequest = MyRequestModel(db=storage.db, user=user)


    def log_transaction(self, identification, data):
        self.has_changes.emit(identification, data['status'], False, data['status_text'])
        self.myid = self.myrequest.add_myrequest(identification, 'autenticación', '', '', signed_document_path="",
                      transaction_status=data['status'], transaction_text=data['status_text'])

    def log_check_transaction(self, identification, data):
        self.has_changes.emit(identification, data['status'], data['received_notification'], data['status_text'])
        self.myrequest.update_myrequest(self.myid, transaction_status=data['status'],
                                        transaction_text=data['status_text'])

    def run(self):
        for identification in self.identifications:
            result = self.person.authenticate(identification)
            self.log_transaction(identification, result)
            if result['status'] == 0:
                self.pending_check[identification] = result['id']
            else:
                self.remove_check.emit(identification)
        while self.pending_check:
            for identification in list(self.pending_check.keys()):
                result = self.person.check_authenticate(self.pending_check[identification])
                self.log_check_transaction(identification, result)
                if result['received_notification']:
                    del self.pending_check[identification]
                    self.remove_check.emit(identification)
            time.sleep(self.wait_time)
        self.has_result.emit(self.tid)


class RequestAuthentication(Ui_RequestAuthentication):

    CONNECTING = 0
    CONNECTED = 1
    REJECTED = 2
    ERROR = 3

    def __init__(self, widget, main_app, db, index):
        Ui_RequestAuthentication.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.session_storage = SessionStorage.getInstance()
        self.setupUi(self.widget)
        self.person = self.session_storage.persons[index]
        self.user = self.session_storage.users[index]


        self.contacts_model = ContactModel(user=self.user, db=db)

        completer = QCompleter()
        completer.setModel(self.contacts_model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.searchContact.setCompleter(completer)
        self.add_contact.clicked.connect(lambda: self.add_contact_to_list())
        self.requestAuthentication.clicked.connect(self.request_authentication)
        self.cleanbtn.clicked.connect(self.cleantable)

        self.auth_list = []
        self.status_widgets = {}
        self.initialize()


    def initialize(self):
        self.contacts.setColumnCount(3)
        self.contacts.setHorizontalHeaderItem(0, QTableWidgetItem("Estado"))
        self.contacts.setHorizontalHeaderItem(1, QTableWidgetItem("Identificación"))
        self.contacts.setHorizontalHeaderItem(2, QTableWidgetItem("Nombre"))
        self.contacts.resizeColumnsToContents()
        self.contacts_count = 0
        self.contacts.contextMenuEvent = self.context_element_menu_event

    def inactive_btn(self):
        self.cleanbtn.setEnabled(False)
        self.add_contact.setEnabled(False)
        self.requestAuthentication.setEnabled(False)

    def active_btn(self):
        self.cleanbtn.setEnabled(True)
        self.add_contact.setEnabled(True)
        self.requestAuthentication.setEnabled(True)


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

    def add_contact_to_list(self):
        txt = self.searchContact.text()
        id = self.contacts_model.deserialize_contact(txt)
        if id:
            if id not in self.auth_list:
                if id != txt:
                    self.insert_item(id, txt)
                else:
                    self.insert_item(id, '')
                self.auth_list.append(id)
                self.searchContact.setText('')
            else:
                QtWidgets.QMessageBox.warning(self.widget, 'Contacto ya existente',
                                              "El contacto seleccionado fue agregado a la lista anteriormente.")

        else:
            QtWidgets.QMessageBox.warning(self.widget, 'Contacto no identificado',
                 "Lo ingresado no es un nombre de contacto o un número de identificación válido.")

    def request_authentication(self):
        self.inactive_btn()
        self.requestAuthProgressBar.setRange(0, len(self.auth_list))
        self.auth_pending = len(self.auth_list)
        self.update_process_bar(0, "Enviando peticiones de autenticación")
        self.pao = PersonAuthenticationOpers(1, self.person, self.auth_list, self.user)
        self.pao.has_result.connect(self.end_authentication)
        self.pao.has_changes.connect(self.check_transaction_change)
        self.pao.remove_check.connect(self.check_transaction_end)
        self.pao.start()

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
        self.auth_list.pop(row)
        self.contacts_count -= 1

    def cleantable(self):
        for x in range(len(self.auth_list)):
            self.contacts.removeRow(0)
            self.auth_list.pop()
        self.contacts.setRowCount(0)
        self.contacts_count=0

    def update_process_bar(self, value, text):
        self.requestAuthProgressBar.setValue(value)
        if text:
            self.requestAuthProgressBar.setFormat(text)

    def end_authentication(self, id):
        self.update_process_bar(len(self.auth_list), 'Solicitud de autorizaciones completo')
        self.active_btn()


    def check_transaction_end(self, identification):
        self.auth_pending -= 1
        self.update_process_bar(len(self.auth_list) - self.auth_pending,
                                'Solicitudes faltantes %d'%self.auth_pending)

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