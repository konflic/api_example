import sqlite3
from src.settings import DB_NAME


class DBConnector(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.instance = sqlite3.connect(DB_NAME)


def execute_sql(sql, values=None):
    connect = DBConnector().instance
    if values:
        connect.execute(sql, values)
    else:
        connect.execute(sql)
    connect.commit()
    connect.close()


def get_sql_result(sql, values=None):
    connect = DBConnector().instance
    if values:
        result = connect.execute(sql, values)
    else:
        result = connect.execute(sql)
    header = [description[0] for description in result.description]
    return [dict(zip(header, row)) for row in result.fetchall()]
