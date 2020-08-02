from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QCompleter

from client_fva.models.ContactDropDown import ContactModel
from client_fva.session_storage import SessionStorage
from client_fva.ui.requestauthenticationui import Ui_RequestAuthentication


class RequestAuthentication(Ui_RequestAuthentication):

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
        self.auth_list = []

    def add_contact_to_list(self):
        txt = self.searchContact.text()
        id = self.contacts_model.deserialize_contact(txt)
        if id:
            new_text = id
            if id != txt:
                new_text += " "+txt
            self.contactsListWidget.addItem(new_text)
            self.auth_list.append(id)
            self.searchContact.setText('')
        else:
            QtWidgets.QMessageBox.warning(self.widget, 'Contacto no identificado',
                 "Lo ingresado no es un nombre de contacto o un número de identificación válido.")

    def request_authentication(self):
        print("REQUEST")