'''
Created on 23 abr. 2018

@author: luis
'''

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore
ID = 0
NAME = 1


class GroupModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        self.tableview = kwargs.pop('tableview')
        super(GroupModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        flags = super(GroupModel, self).flags(index)

        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

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

    def addGroup(self, name):
        query = QSqlQuery(self.db)
        query.prepare("insert into groups(name, userid) values(?, ?)")
        query.addBindValue(name)
        query.addBindValue(self.user)
        if not query.exec_():
            print(query.lastError().text())

        self.refresh()

    def refresh(self):
        self.setQuery('select id, name from groups', db=self.db)
        self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(NAME, QtCore.Qt.Horizontal, "name")
        self.tableview.setColumnHidden(ID, True)
        # self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def deleteGroup(self, row):
        id = self.data(self.index(row, 0))
        query = QSqlQuery(self.db)
        query.prepare("delete from groups where id = ?")
        query.addBindValue(id)
        if not query.exec_():
            print(query.lastError().text())

        self.refresh()
