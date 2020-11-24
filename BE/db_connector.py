import pymysql

from config import database

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
                            db = 'brandi-admin',
                            )
    db.cursor().execute("""SET time_zone='Asia/Seoul'""")
    
    return db