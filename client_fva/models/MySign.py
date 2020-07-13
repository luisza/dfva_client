import logging
import re

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtWidgets

logger = logging.getLogger()
DOCUMENT_NAME = 1
DOCUMENT_PATH = 2
ID = 0

class MySignModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        self.tableview = kwargs.pop('tableview', None)
        self.mysign = None
        super(MySignModel, self).__init__(*args, **kwargs)

    # def flags(self, index):
    #     flags = super(MySignModel, self).flags(index)
    #     if index.column() in (FIRSTNAME, LASTNAME, IDENTIFICATION):
    #         flags |= QtCore.Qt.ItemIsEditable
    #     return flags

    def set_mysign(self, mysign):
        self.mysign = mysign

    # def setData(self, index, value, role):
    #     if index.column() == DOCUMENT_NAME:
    #         column = "documentname"
    #     elif index.column() == DOCUMENT_PATH:
    #         column = "documentpath"
    #     else:
    #         return False
    #     primary_key_index = self.index(index.row(), 0)
    #     id = self.data(primary_key_index)
    #     self.clear()
    #     self.update_contact_data(column, id, value)
    #     self.refresh()
    #     return True

    # def update_contact_data(self, column, id, value):
    #     strquery = 'update contacts set %s = ? where id = ? and userid = ? and groupid = ?' % (column)
    #     query = QSqlQuery(db=self.db)
    #     query.prepare(strquery)
    #     query.addBindValue(value)
    #     query.addBindValue(id)
    #     query.addBindValue(self.user)
    #     query.addBindValue(self.group)
    #     if not query.exec_():
    #         logger.error(query.lastError().text())


    def refresh(self):

        query = 'select id, document_name, sign_document_path from mysigns where userid=%d' % (self.user)
        self.setQuery(query, db=self.db)
        self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(DOCUMENT_NAME, QtCore.Qt.Horizontal, "Nombre")
        self.setHeaderData(DOCUMENT_PATH, QtCore.Qt.Horizontal, "Guardado")
        self.tableview.setColumnHidden(ID, True)
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def delete_mysign(self, row):
        id = self.data(self.index(row, 0))
        query = QSqlQuery(self.db)
        query.prepare("delete from mysigns where id = ?")
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())
        self.refresh()

    def add_mysign(self, identification, document_path, document_name, sign_document_path="", transaction_id=0,
                   transaction_text=""):
        """ mysigns(id , identification, document_path, document_name,
                   sign_document_path, transaction_id,
                   transaction_text, userid )"""

        querystr = """insert into mysigns(identification, document_path, document_name, sign_document_path, transaction_id, 
                   transaction_text, userid) values(?, ?, ?, ?, ?, ?, ?) """

        query = QSqlQuery(self.db)
        query.prepare(querystr)
        query.addBindValue(identification)
        query.addBindValue(document_path)
        query.addBindValue(document_name)
        query.addBindValue(sign_document_path)
        query.addBindValue(transaction_id)
        query.addBindValue(transaction_text)
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        return query.lastInsertId()

    def update_mysign(self, id, **kwargs):
        query = QSqlQuery(self.db)
        keys = list(kwargs.keys())
        keysstr = ["%s = ?" % (x,) for x in keys]
        querystr = 'update mysigns set %s where id = ?' % (", ".join(keysstr), )
        query.prepare(querystr)
        for k in keys:
            query.addBindValue(k)
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())

