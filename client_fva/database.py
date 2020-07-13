from PyQt5 import QtSql
import logging

logger = logging.getLogger()


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

    query.exec_("""create table if not exists mysigns(id integer primary key autoincrement unique not null,
                   identification varchar(20), document_path varchar(500), document_name varchar(200), 
                   sign_document_path varchar(500), transaction_id integer not null, 
                   transaction_text varchar(250) not null, userid integer not null,
                   FOREIGN KEY (userid) REFERENCES users)""")
    return True, db
