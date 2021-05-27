from pathlib import Path

from PyQt5 import QtSql
import logging

from client_fva.user_settings import UserSettings

logger = logging.getLogger()


def createDB():
    settings = UserSettings.getInstance()
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(str(Path(settings.get_home_path()) / Path('dfva_client.db')))

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
                   signed_document_path varchar(500), transaction_status integer not null, 
                   transaction_text varchar(250) not null, userid integer not null,
                   FOREIGN KEY (userid) REFERENCES users)""")

    query.exec_("""create table if not exists myrequests(id integer primary key autoincrement unique not null,
                   identification varchar(20), request_type varchar(250) not null, document_path varchar(500), 
                   document_name varchar(200), signed_document_path varchar(500), 
                   transaction_status integer not null, transaction_text varchar(250) not null, 
                   userid integer not null, FOREIGN KEY (userid) REFERENCES users)""")

    query.exec_("""create table if not exists serialalias(serial varchar(30) unique not null,
                   alias varchar(20) )""")
    return True, db
