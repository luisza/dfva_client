import logging
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

logger = logging.getLogger()


class UserModel(QSqlQueryModel):

    def __init__(self, *args, **kwargs):
        self.db = kwargs.pop('db')
        super(UserModel, self).__init__(*args, **kwargs)

    def get_user_by_identification(self, identification):
        userid = None
        query = QSqlQuery(db=self.db)
        query.prepare('SELECT id FROM users WHERE identification = ?')
        query.addBindValue(identification)
        if not query.exec_():
            logger.error(query.lastError().text())
        while query.next():
            userid = query.value(0)
        return userid

    def get_or_create_user(self, identification, first_name, last_name):
        user_id = self.get_user_by_identification(identification)
        if not user_id:
            insquery = QSqlQuery(self.db)
            insquery.prepare("insert into users(firstname, lastname, identification) values(?, ?, ?)")
            insquery.addBindValue(first_name)
            insquery.addBindValue(last_name)
            insquery.addBindValue(identification)
            if not insquery.exec_():
                logger.error(insquery.lastError().text())
            user_id = self.get_user_by_identification(identification)
        return user_id