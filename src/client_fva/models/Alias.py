import logging

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

logger = logging.getLogger()


class Alias(QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')
        super(Alias, self).__init__(*args, **kwargs)

    def filter(self, text):
        sql = 'select alias from serialalias where serial = ?'
        query = QSqlQuery(self.db)
        query.prepare(sql)
        query.addBindValue(text)
        if not query.exec_():
            logger.error(query.lastError().text())
        data = []
        while query.next():
            data.append(query.value(0))
        return data

    def create(self, serial, alias):
        querystr = """insert into serialalias(serial, alias) values(?, ?) """
        query = QSqlQuery(self.db)
        query.prepare(querystr)
        query.addBindValue(serial)
        query.addBindValue(alias)
        if not query.exec_():
            logger.error(query.lastError().text())
        return query.lastInsertId()

    def update(self, serial, alias):
        querystr = 'update serialalias set alias = ? where serial = ?'
        query = QSqlQuery(self.db)
        query.prepare(querystr)

        query.addBindValue(alias)
        query.addBindValue(serial)
        if not query.exec_():
            logger.error(query.lastError().text())

    def create_update(self, serial, alias):
        exist = self.filter(serial) != []
        if exist:
            self.update(serial, alias)
        else:
            self.create(serial, alias)