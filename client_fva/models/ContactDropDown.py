import logging
import re

from PyQt5.QtCore import QStringListModel
from PyQt5.QtSql import QSqlQuery

ID = 0
FIRSTNAME = 1
LASTNAME = 2
IDENTIFICATION = 3

logger = logging.getLogger()


class ContactModel(QStringListModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        super(ContactModel, self).__init__(*args, **kwargs)
        self.context_data = {}
        self.inicialize()

    def get_all(self):
        query = QSqlQuery(self.db)
        query.prepare("select distinct(identification), firstname, lastname from contacts where userid = ?")
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append((
                    query.value(0),
                    query.value(1) + ' ' + query.value(2),
            ))
        return data

    def inicialize(self):
        for text in self.get_all():
            idx = self.rowCount()
            self.insertRow(idx)
            self.setData(self.index(idx), text[1])
            self.context_data[text[1]] = text[0]


    def deserialize_contact(self, text):
        if text in self.context_data:
            return self.context_data[text]
        else:
            if self.valid_identification(text):
                return text

    def valid_identification(self, identification):
        pattern = r'(^[1|5]\d{11}$)|(^\d{2}-\d{4}-\d{4}$)'  # only person identifications
        if re.match(pattern, identification):
            return True
        return False