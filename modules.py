import os
'''
https://devcenter.heroku.com/articles/config-vars
'''
from boto.s3.connection import S3Connection
import psycopg2

class SensorProcess():
    def __init__(self):pass
    def insertSensorData(self):
        dp = DBProcess()
        conn = dp.getDBConn()
        cursor = conn.cursor()
        #cursor.execute("insert ")
        #conn.commit()
        dp.closeConn(cursor, conn)

'''
http://h2shiki.hateblo.jp/entry/2016/05/05/210738
'''
class DBProcess():
    def __init__(self):
        self.tableName = "nagara"
        s3 = S3Connection(
            os.environ["DB_HOSTNAME"],
            os.environ["DB_DATABASE"],
            os.environ["DB_PORT"],
            os.environ["DB_USER"],
            os.environ["DB_PASSWORD"]
        )
    
    def getDBConn(self):
        return psycopg2.connect(
            host = DB_HOSTNAME,
            database = DB_DATABASE,
            port = DB_PORT,
            user = DB_USER,
            password = DB_PASSWORD
        )
    
    def closeConn(self, cursor, conn):
        cursor.close()
        conn.close()
    
    def dbInsert(self):
        pass
    
    def dbSelect(self, attr):
        '''
        [入力]
        ●"項目1,項目2,..."
        ●すべての項目を取得する場合は"*"のみ．
        '''
        conn = self.getDBConn()
        cursor = conn.cursor()
        cursor.execute("select "+ str + " from " + self.tableName)
        result = cursor.fetchall()
        self.closeConn(cursor, conn)
        return result

class BasicProcess():
    def __init__(self):
        self.dp = DBProcess()
        #self.sp = SensorProcess()
    
    def getDBCalorie(self):
        calorie = self.dp.dbSelect("calorie")
    
    #def shapeData():
