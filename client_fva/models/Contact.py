'''
Created on 23 abr. 2018

@author: luis
'''

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore
ID = 0
FIRSTNAME = 1
LASTNAME = 2
IDENTIFICATION = 3


class ContactModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        self.tableview = kwargs.pop('tableview')
        self.group = None
        super(ContactModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        flags = super(ContactModel, self).flags(index)

        if index.column() in (FIRSTNAME, LASTNAME, IDENTIFICATION):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setGroup(self, group):
        self.group = group

    def setData(self, index, value, role):
        print("setData", index.column(), value)

        if index.column() == FIRSTNAME:
            column = "firstname"
        elif index.column() == LASTNAME:
            column = "lastname"
        elif index.column() == IDENTIFICATION:
            column = "identification"
        else:
            return False
        primaryKeyIndex = self.index(index.row(), 0)
        id = self.data(primaryKeyIndex)

        self.clear()
        self.update_contactdata(column, id, value)
        self.refresh()
        return True

    def update_contactdata(self, column, id, value):
        strquery = 'update contacts set %s = ? where id = ? and userid = ? and groupid = ?' % (
            column)
        print(strquery, value, id, self.user)
        query = QSqlQuery(db=self.db)
        query.prepare(strquery)
        query.addBindValue(value)
        query.addBindValue(id)
        query.addBindValue(self.user)
        query.addBindValue(self.group)
        if not query.exec_():
            print(query.lastError().text())

    def addContact(self, firstname, lastname, identification):
        query = QSqlQuery(self.db)
        query.prepare(
            "insert into contacts(groupid, userid, firstname,  lastname,  identification) values(?, ?, ?, ?, ?)")

        query.addBindValue(self.group)
        query.addBindValue(self.user)
        query.addBindValue(firstname)
        query.addBindValue(lastname)
        query.addBindValue(identification)

        if not query.exec_():
            print(query.lastError().text())

        self.refresh()

    def refresh(self):
        if self.group == -1 or self.group is None:
            return
        query = 'select id, firstname,  lastname,  identification from contacts where groupid=%d and userid=%d' % (
            self.group, self.user
        )
        self.setQuery(query, db=self.db)
        self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(FIRSTNAME, QtCore.Qt.Horizontal, "First Name")
        self.setHeaderData(LASTNAME, QtCore.Qt.Horizontal, "Last Name")
        self.setHeaderData(
            IDENTIFICATION, QtCore.Qt.Horizontal, "Identification")

        #self.setHeaderData(NAME, QtCore.Qt.Horizontal, "name")
        self.tableview.setColumnHidden(ID, True)
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def deleteContact(self, row):
        id = self.data(self.index(row, 0))
        query = QSqlQuery(self.db)
        query.prepare("delete from contacts where id = ?")
        query.addBindValue(id)
        if not query.exec_():
            print(query.lastError().text())

        self.refresh()