from client_fva.ui.managecontactsui import Ui_ManageContacts
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMenu
from client_fva.models.Group import GroupModel
from client_fva.ui.contactAddDialog import AddContactDialog
from client_fva.models.Contact import ContactModel
# column numbers
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
        self.last_group = -1
        self.contacts_model = ContactModel(user=current_user,
                                           db=self.db,
                                           tableview=self.contactsTableView)
        self.groups_model = GroupModel(user=current_user,
                                       db=self.db,
                                       tableview=self.groupsTableView)
        self.initialize_and_populate_groups()
        self.initialize_and_populate_contacts()
        self.groupsTableView.selectionModel().currentRowChanged.connect(
            lambda: self.groupSelected())
        self.addGroup.clicked.connect(lambda: self.addGroupDB())
        self.addContact.clicked.connect(lambda: self.addContactDB())

    def initialize_and_populate_groups(self):
        self.groupsTableView.setModel(self.groups_model)
        self.groupsTableView.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.groupsTableView.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        self.groups_model.refresh()
        self.groupsTableView.contextMenuEvent = self.contextGroupMenuEvent

    def contextGroupMenuEvent(self, pos):
        if self.groupsTableView.selectionModel().selection().indexes():
            for i in self.groupsTableView.selectionModel().selection().indexes():
                row, column = i.row(), i.column()
            menu = QMenu()
            deleAction = menu.addAction("Delete")
            action = menu.exec_(self.groupsTableView.mapToGlobal(pos.pos()))
            if action == deleAction:
                self.deleteGroupAction(row, column)

    def initialize_and_populate_contacts(self):
        self.contactsTableView.setModel(self.contacts_model)
        self.contactsTableView.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.contactsTableView.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        self.contacts_model.refresh()
        self.contactsTableView.contextMenuEvent = self.contextContactMenuEvent

    def contextContactMenuEvent(self, pos):
        if self.contactsTableView.selectionModel().selection().indexes():
            for i in self.contactsTableView.selectionModel().selection().indexes():
                row, column = i.row(), i.column()
            menu = QMenu()
            deleAction = menu.addAction("Delete")
            action = menu.exec_(self.contactsTableView.mapToGlobal(pos.pos()))
            if action == deleAction:
                self.deleteContactAction(row, column)

    def groupSelected(self):
        index = self.groupsTableView.currentIndex()
        print("group change")
        if index.isValid():
            record = self.groups_model.record(index.row())
            self.last_group = record.value(ID)
            self.contacts_model.setGroup(self.last_group)
            self.contacts_model.refresh()
            #self.contacts_model.setFilter("groupid = %d" % (groupid,))
        # else:
        #    self.contacts_model.setFilter("groupid = -1")
        # self.contacts_model.select()
        # self.contactsTableView.horizontalHeader().setVisible(
        #    self.contacts_model.rowCount() > 0)

    def get_last_group(self):
        if self.last_group == -1:
            record = self.groups_model.record(0)
            self.last_group = record.value(ID)
            self.contacts_model.setGroup(self.last_group)
        return self.last_group

    def addGroupDB(self):

        text, okPressed = QInputDialog.getText(
            self.widget, "Add Group", "Group name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            self.groups_model.addGroup(text)

    def deleteGroupAction(self, row, column):
        self.groups_model.deleteGroup(row)

    def addContactDB(self):

        firstname, lastname, identification, ok = AddContactDialog.new_contact(
            self.widget)
        if ok:
            group = self.get_last_group()
            self.contacts_model.addContact(firstname, lastname, identification)

    def deleteContactAction(self, row, column):
        self.contacts_model.deleteContact(row)
