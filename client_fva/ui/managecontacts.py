import re

from client_fva.ui.managecontactsui import Ui_ManageContacts
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMenu
from client_fva.models.Group import GroupModel
from client_fva.ui.contactAddDialog import AddContactDialog
from client_fva.models.Contact import ContactModel

# column number for matching
ID = 0
NAME = FIRSTNAME = 1
GROUPUSERID = LASTNAME = 2
IDENTIFICATION = 3
CONTACTSUSERID = 4
GROUPID = 5


class ManageContacts(Ui_ManageContacts):

    def __init__(self, widget, main_app, db, current_user):
        Ui_ManageContacts.__init__(self)
        self.widget = widget
        self.main_app = main_app
        self.db = db
        self.current_user = current_user
        self.setupUi(widget)
        self.selected_group = -1
        self.contacts_model = ContactModel(user=current_user, db=self.db, tableview=self.contactsTableView)
        self.groups_model = GroupModel(user=current_user, db=self.db, tableview=self.groupsTableView)
        self.proxy_model_contact = QtCore.QSortFilterProxyModel()  # to allow contacts search
        self.initialize_and_populate_groups()
        self.initialize_and_populate_contacts()
        self.groupsTableView.selectionModel().currentRowChanged.connect(lambda: self.group_selected())
        self.addGroup.clicked.connect(lambda: self.add_group_db())
        self.addContact.clicked.connect(lambda: self.add_contact_db())
        self.searchContact.textChanged.connect(self.search_contacts)

    def initialize_and_populate_groups(self):
        self.groupsTableView.setModel(self.groups_model)
        self.groupsTableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.groupsTableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.groups_model.refresh()
        self.groupsTableView.contextMenuEvent = self.context_group_menu_event
        self.groupsTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                                             QtWidgets.QAbstractItemView.DoubleClicked)  # only edit on double click

    def context_group_menu_event(self, pos):
        if self.groupsTableView.selectedIndexes():
            selected = self.groupsTableView.currentIndex()  # user can only select one group at the time
            if selected.isValid():
                row, column = selected.row(), selected.column()
                menu = QMenu()
                menu.setStyleSheet("QMenu::item{color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);}")
                delete_action = menu.addAction("Delete")
                delete_action.setIcon(QtGui.QIcon(":images/delete.png"))
                action = menu.exec_(self.groupsTableView.mapToGlobal(pos.pos()))
                if action == delete_action:
                    self.delete_group_action(row, column)

    def initialize_and_populate_contacts(self):
        self.proxy_model_contact.setSourceModel(self.contacts_model)
        self.proxy_model_contact.setFilterKeyColumn(-1)  # so it searches by all columns
        self.contactsTableView.setModel(self.proxy_model_contact)
        self.contactsTableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.contactsTableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.contacts_model.refresh()
        self.contactsTableView.contextMenuEvent = self.context_contact_menu_event
        self.contactsTableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                                               QtWidgets.QAbstractItemView.DoubleClicked)  # only edit on double click

    def context_contact_menu_event(self, pos):
        if self.contactsTableView.selectedIndexes():
            selected = self.contactsTableView.currentIndex()  # user can only select one contact at the time
            if selected.isValid():
                row, column = selected.row(), selected.column()
                menu = QMenu()
                menu.setStyleSheet("QMenu::item{color:rgb(76, 118, 82);background-color:rgb(216, 230, 225);}")
                delete_action = menu.addAction("Delete")
                delete_action.setIcon(QtGui.QIcon(":images/delete.png"))
                action = menu.exec_(self.contactsTableView.mapToGlobal(pos.pos()))
                if action == delete_action:
                    self.delete_contact_action(row, column)

    def group_selected(self):
        index = self.groupsTableView.currentIndex()
        if index.isValid():
            record = self.groups_model.record(index.row())
            self.selected_group = record.value(ID)
            self.contacts_model.set_group(self.selected_group)
            self.contacts_model.refresh()

    def add_group_db(self):
        text, okPressed = QInputDialog.getText(self.widget, "Agregar Grupo", "Nombre", QLineEdit.Normal, "")
        if okPressed and text:
            self.groups_model.add_group(text)
            self.groupsTableView.selectRow(self.groups_model.rowCount()-1)  # select the added group

    def delete_group_action(self, row, column):
        self.contacts_model.delete_group_contacts()
        self.groups_model.delete_group(row)
        if self.groups_model.rowCount():
            self.groupsTableView.selectRow(0)
        else:
            self.selected_group = -1  # selected deleted and nothing to select, so we set it up to 0

    def add_contact_db(self):
        if self.selected_group > 0:
            firstname, lastname, identification, ok = AddContactDialog.new_contact(self.widget)
            if ok:
                self.contacts_model.add_contact(firstname, lastname, identification)
                self.contactsTableView.selectRow(self.contacts_model.rowCount()-1)  # select the added contact
        else:
            QtWidgets.QMessageBox.information(None, 'Seleccione Grupo', "Por favor seleccione un grupo para agregar "
                                                                        "contactos.")

    def delete_contact_action(self, row, column):
        self.contacts_model.delete_contact(row)

    def search_contacts(self, text):
        regex = ".*{}.*".format(text)  # a contains search
        self.proxy_model_contact.setFilterRegExp(QtCore.QRegExp(regex, QtCore.Qt.CaseInsensitive))

