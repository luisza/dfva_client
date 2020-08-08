from base64 import b64decode

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem

from client_fva.models.ContactDropDown import ContactModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.requestauthenticationui import Ui_RequestAuthentication


class PersonAuthenticationOpers(QThread):
    has_result = pyqtSignal(int)

    def __init__(self, tid, person, user, data):
        self.data = data
        self.person = person
        super(PersonAuthenticationOpers, self).__init__()
        self.tid = tid
        self.result = None
        storage = SessionStorage.getInstance()


    def run(self):
        data = self.data
        mid = self.mysign.add_mysign(data["identification"], data["file_path"], data["file_name"],
                                     signed_document_path=data["save_path"])
        self.result = self.person.sign(data["identification"], data["document"], data["resume"],
                                       _format=data["_format"], file_path=data["file_path"],
                                       algorithm=data["algorithm"], is_base64=data["is_base64"],
                                       wait=data["wait"], extras=data["extras"])
        self.mysign.update_mysign(mid, transaction_status=self.result["status"], transaction_text=self.result["status_text"])

        with open(data["save_path"], "wb") as arch:
            arch.write(b64decode(self.result["signed_document"]))

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

        self.contacts_model = ContactModel(user=self.session_storage.users[index], db=db)

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
            if id != txt:
                self.insert_item(id, txt)
            else:
                self.insert_item(id, '')
            self.auth_list.append(id)
            self.searchContact.setText('')
        else:
            QtWidgets.QMessageBox.warning(self.widget, 'Contacto no identificado',
                 "Lo ingresado no es un nombre de contacto o un número de identificación válido.")

    def request_authentication(self):
        print("REQUEST", self.auth_list)

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