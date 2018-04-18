from client_fva.ui.managecontactsui import Ui_ManageContacts
from PyQt5 import QtWidgets, Qt, QtSql, QtCore, QtGui

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
        self.contacts_model = None
        self.groups_model = None
        self.initialize_and_populate_groups()
        self.initialize_and_populate_contacts()
        self.groupsTableView.selectionModel().currentRowChanged.connect(lambda: self.groupChanged())
        self.addGroup.clicked.connect(lambda: self.addGroupDB())

    def initialize_and_populate_groups(self):
        self.groups_model = QtSql.QSqlRelationalTableModel(None, self.db)
        self.groups_model.setTable("groups")
        self.groups_model.setFilter("userid = %d" % (self.current_user, ))
        self.groups_model.setRelation(GROUPUSERID, QtSql.QSqlRelation("users", "id", "id"))
        self.groups_model.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.groups_model.setHeaderData(NAME, QtCore.Qt.Horizontal, "Name")
        self.groups_model.setHeaderData(GROUPUSERID, QtCore.Qt.Horizontal, "User")
        self.groups_model.select()
        self.groupsTableView.setModel(self.groups_model)
        self.groupsTableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.groupsTableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.groupsTableView.setColumnHidden(ID, True)
        self.groupsTableView.setColumnHidden(GROUPUSERID, True)
        self.groupsTableView.resizeColumnsToContents()
        self.groupsTableView.horizontalHeader().setStretchLastSection(True)

    def initialize_and_populate_contacts(self):
        self.contacts_model = QtSql.QSqlRelationalTableModel(None, self.db)
        self.contacts_model.setTable("contacts")
        self.contacts_model.setRelation(CONTACTSUSERID, QtSql.QSqlRelation("users", "id", "id"))
        self.contacts_model.setRelation(GROUPID, QtSql.QSqlRelation("groups", "id", "id"))
        self.contacts_model.setHeaderData(ID, QtCore.Qt.Horizontal, "Id")
        self.contacts_model.setHeaderData(FIRSTNAME, QtCore.Qt.Horizontal, "First Name")
        self.contacts_model.setHeaderData(LASTNAME, QtCore.Qt.Horizontal, "Last Name")
        self.contacts_model.setHeaderData(IDENTIFICATION, QtCore.Qt.Horizontal, "Identification")
        self.contacts_model.setHeaderData(CONTACTSUSERID, QtCore.Qt.Horizontal, "User")
        self.contacts_model.setHeaderData(GROUPID, QtCore.Qt.Horizontal, "Group")
        self.contacts_model.select()
        self.contactsTableView.setModel(self.contacts_model)
        self.contactsTableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.contactsTableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.contactsTableView.setColumnHidden(ID, True)
        self.contactsTableView.setColumnHidden(CONTACTSUSERID, True)
        self.contactsTableView.setColumnHidden(GROUPID, True)
        self.contactsTableView.resizeColumnsToContents()
        self.contactsTableView.horizontalHeader().setStretchLastSection(True)

    def groupChanged(self):
        index = self.groupsTableView.currentIndex()
        if index.isValid():
            record = self.groups_model.record(index.row())
            groupid = record.value(ID)
            self.contacts_model.setFilter("groupid = %d" % (groupid,))
        else:
            self.contacts_model.setFilter("groupid = -1")
        self.contacts_model.select()
        self.contactsTableView.horizontalHeader().setVisible(self.contacts_model.rowCount() > 0)
        print(self.contacts_model.rowCount())

    def addGroupDB(self):
        row = self.groups_model.rowCount()
        self.groups_model.insertRow(row)
        index = self.groups_model.index(row, NAME)
        self.groupsTableView.setCurrentIndex(index)
        self.groupsTableView.edit(index)


