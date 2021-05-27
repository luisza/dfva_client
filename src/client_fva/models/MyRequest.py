import logging

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

logger = logging.getLogger()


class MyRequestModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.db = kwargs.pop('db')
        super(MyRequestModel, self).__init__(*args, **kwargs)

    def get_all(self):
        sql = 'select identification, request_type, document_name, signed_document_path, transaction_status, ' \
              'transaction_text from myrequests where userid=? order by id DESC'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append((query.value(0),
                         query.value(1),
                         query.value(2),
                         query.value(3),
                         query.value(4),
                         query.value(5)))
        return data

    def filter(self, text):
        sql = 'select identification, request_type, document_name, signed_document_path, transaction_status, ' \
              'transaction_text from myrequests where identification like ? and  userid = ? order by id DESC'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue("%{}%".format(text))
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append((query.value(0), query.value(1), query.value(2), query.value(3), query.value(4), query.value(5)))
        return data

    def delete_myrequest(self, row):
        id = self.data(self.index(row, 0))
        query = QSqlQuery(self.db)
        query.prepare("delete from myrequests where id = ?")
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())
        self.refresh()

    def add_myrequest(self, identification, request_type, document_path, document_name, signed_document_path="",
                      transaction_status=0, transaction_text=""):
        querystr = """insert into myrequests(identification, request_type, document_path, document_name, 
                      signed_document_path, transaction_status, transaction_text, userid) 
                      values(?, ?, ?, ?, ?, ?, ?, ?) """
        query = QSqlQuery(self.db)
        query.prepare(querystr)
        query.addBindValue(identification)
        query.addBindValue(request_type)
        query.addBindValue(document_path)
        query.addBindValue(document_name)
        query.addBindValue(signed_document_path)
        query.addBindValue(transaction_status)
        query.addBindValue(transaction_text)
        query.addBindValue(self.user)
        if not query.exec_():
            logger.error(query.lastError().text())
        return query.lastInsertId()

    def update_myrequest(self, id, **kwargs):
        query = QSqlQuery(self.db)
        keys = list(kwargs.keys())
        keysstr = ["%s = ?" % (x,) for x in keys]
        querystr = 'update myrequests set %s where id = ?' % (", ".join(keysstr), )
        query.prepare(querystr)
        for k in keys:
            query.addBindValue(kwargs[k])
        query.addBindValue(id)
        if not query.exec_():
            logger.error(query.lastError().text())

