import logging
import re

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtWidgets

ID = 0
FIRSTNAME = 1
LASTNAME = 2
IDENTIFICATION = 3

logger = logging.getLogger()


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

    def set_group(self, group):
        self.group = group

    def setData(self, index, value, role):
        if index.column() == FIRSTNAME:
            column = "firstname"
        elif index.column() == LASTNAME:
            column = "lastname"
        elif index.column() == IDENTIFICATION:
            column = "identification"
        else:
            return False
        primary_key_index = self.index(index.row(), 0)
        id = self.data(primary_key_index)
        self.clear()
        self.update_contact_data(column, id, value)
        self.refresh()
        return True

    def update_contact_data(self, column, id, value):
        strquery = 'update contacts set %s = ? where id = ? and userid = ? and groupid = ?' % (column)
        query = QSqlQuery(db=self.db)
        query.prepare(strquery)
        query.addBindValue(value)
        query.addBindValue(id)
        query.addBindValue(self.user)
        query.addBindValue(self.group)
        if not query.exec_():
            logger.error(query.lastError().text())

    def add_contact(self, firstname, lastname, identification):
        if self.identification_is_valid(identification):
            query = QSqlQuery(self.db)
            query.prepare("insert into contacts(groupid, userid, firstname,  lastname,  identification) "
                          "values(?, ?, ?, ?, ?)")
            query.addBindValue(self.group)
            query.addBindValue(self.user)
            query.addBindValue(firstname)
            query.addBindValue(lastname)
            query.addBindValue(identification)
            if not query.exec_():
                logger.error(query.lastError().text())
            self.refresh()
        else:
            QtWidgets.QMessageBox.critical(None, 'Contacto Inválido', "No se puede crear el nuevo contacto porque "
                                                                      "la identificación ingresada es inválida.\n"
                                                                      "Formatos aceptados \n * Nacional: 00-0000-0000"
                                                                      "\n * Extranjero: 000000000000")

    def refresh(self):
        if self.group == -1 or self.group is None:
            return
        query = 'select id, firstname,  lastname,  identification from contacts where groupid=%d and userid=%d' % (
                 self.group, self.user)
        self.setQuery(query, db=self.db)
        self.setHeaderData(ID, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(FIRSTNAME, QtCore.Qt.Horizontal, "Nombre")
        self.setHeaderData(LASTNAME, QtCore.Qt.Horizontal, "Apellidos")
        self.setHeaderData(IDENTIFICATION, QtCore.Qt.Horizontal, "Identificación")
        self.tableview.setColumnHidden(ID, True)
        self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def delete_contact(self, row):
        id = self.data(self.index(row, 0))
        query = QSqlQuery(self.db)
        query.prepare("delete from contacts where id = ?")
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())
        self.refresh()

    def delete_group_contacts(self):
        if self.group == -1 or self.group is None:
            return
        query = QSqlQuery(self.db)
        query.prepare("delete from contacts where groupid = ?")
        query.addBindValue(self.group)
        if not query.exec_():
            logger.error(query.lastError().text())
        self.refresh()

    def identification_is_valid(self, identification):
        pattern = r'(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)'  # only person identifications
        if re.match(pattern, identification):
            return True
        return False
