import logging
import re

from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

logger = logging.getLogger()
DOCUMENT_NAME = 1
DOCUMENT_PATH = 2
DOCUMENT_STATUS = 3
DOCUMENT_STATUS_TEXT = 4
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

    def get_all(self):
        sql = 'select document_name, sign_document_path, transaction_id, transaction_text from mysigns where userid=? order by id DESC'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append((
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
            ))
        return data

    def filter(self, text):
        sql = 'select document_name, sign_document_path, transaction_id, transaction_text from mysigns where document_name like "%?%" and  userid=? order by id DESC'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(text)
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append((
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
            ))
        return data
    def refresh(self):

        query = 'select id, document_name, sign_document_path, transaction_id, transaction_text from mysigns where userid=%d order by id DESC' % (self.user)
        self.setQuery(query, db=self.db)
        self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(DOCUMENT_NAME, QtCore.Qt.Horizontal, "Nombre")
        self.setHeaderData(DOCUMENT_PATH, QtCore.Qt.Horizontal, "Ruta de guardado")
        self.setHeaderData(DOCUMENT_STATUS, QtCore.Qt.Horizontal, "Estado")
        self.setHeaderData(DOCUMENT_STATUS_TEXT, QtCore.Qt.Horizontal, "Texto de estado")
        self.tableview.setColumnHidden(ID, True)
        self.tableview.setColumnHidden(DOCUMENT_STATUS_TEXT, True)
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
            query.addBindValue(kwargs[k])
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())

    def set_icon(self):
        qti = QTableWidgetItem()
        qti.setIcon(QtGui.QIcon(":/images/connecting.png"))

