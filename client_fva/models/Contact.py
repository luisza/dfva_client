'''
Created on 23 abr. 2018

@author: luis
'''

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore
ID = 0
NAME = 1

FIRSTNAME = 0
LASTNAME = 1
IDENTIFICATION = 2


class ContactModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        self.tableview = kwargs.pop('tableview')
        self.group = None
        super(ContactModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        flags = super(ContactModel, self).flags(index)

        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setGroup(self, group):
        self.group = group

    def setData(self, index, value, role):
        print("setData", index.column(), value)
        if index.column() not in (1, 2):
            return False

        primaryKeyIndex = self.index(index.row(), 0)
        id = self.data(primaryKeyIndex)

        self.clear()

        if index.column() == 1:
            ok = self.setName(id, value)
        self.refresh()
        return ok

    def setName(self, id, name):
        query = QSqlQuery(db=self.db)
        query.prepare('update groups set name = ? where id = ? and userid = ?')
        query.addBindValue(name)
        query.addBindValue(id)
        query.addBindValue(self.user)
        return query.exec_()

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
        query = 'select firstname,  lastname,  identification from contacts where groupid=%d and userid=%d' % (
            self.group, self.user
        )
        self.setQuery(query, db=self.db)
        self.setHeaderData(FIRSTNAME, QtCore.Qt.Horizontal, "First Name")
        self.setHeaderData(LASTNAME, QtCore.Qt.Horizontal, "Last Name")
        self.setHeaderData(
            IDENTIFICATION, QtCore.Qt.Horizontal, "Identification")
        #self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        #self.setHeaderData(NAME, QtCore.Qt.Horizontal, "name")
        #self.tableview.setColumnHidden(ID, True)
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)
