import pymysql
from config.py import database

def connect_db():
    db = pymysql.connect(
                            host     = database['host'],
                            port     = database['port'],
                            user     = database['user'],
                            password = database['password'],
                            database = database['database'],
                            charset  = database['charset'],
                            cursor   = pymysql.cursors.DictCursor,
                            autocommit = False,
                            read_timeout = 20,
                            db = 'brandi',
                            )
    return db
