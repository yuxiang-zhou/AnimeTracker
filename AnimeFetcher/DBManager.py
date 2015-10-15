import MySQLdb

class DBManager:
    db = None
    cursor = None
    @staticmethod
    def connect(user, password, db_name,host = 'localhost'):
        DBManager.db = MySQLdb.connect(host,user,password,db_name,charset="utf8", use_unicode=True)
        DBManager.cursor = DBManager.db.cursor()

    @staticmethod
    def disconnect():
        DBManager.db.close()

    @staticmethod
    def execute(sql):
        try:
            DBManager.cursor.execute(sql)
            DBManager.db.commit()
        except:
            DBManager.db.rollback()
            print("Failed Executing SQL:" + sql)

    @staticmethod
    def fetchall():
        return DBManager.cursor.fetchall()

    @staticmethod
    def lastrowid():
        return DBManager.cursor.lastrowid