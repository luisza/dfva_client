from PyQt5 import QtSql
import logging

logger = logging.getLogger('dfva_client')


def createDB():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('dfva_client.db')

    if not db.open():
        logger.error(db.lastError())
        return False, None

    query = QtSql.QSqlQuery()
    query.exec_("""create table if not exists users(id integer primary key autoincrement unique not null,
                   firstname varchar(20), lastname varchar(20), identification varchar(20))""")

    query.exec_("""create table if not exists groups(id integer primary key autoincrement unique not null, 
                   name varchar(20), userid integer not null, FOREIGN KEY (userid) REFERENCES users)""")

    query.exec_("""create table if not exists contacts(id integer primary key autoincrement unique not null,
                   firstname varchar(20), lastname varchar(20), identification varchar(20),
                   userid integer not null, groupid integer not null,
                   FOREIGN KEY (userid) REFERENCES users, FOREIGN KEY (groupid) REFERENCES groups)""")
    return True, db
