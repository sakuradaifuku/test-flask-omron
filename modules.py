import os
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
        self.DB_HOSTNAME = os.environ["DB_HOSTNAME"]
        self.DB_DATABASE = os.environ["DB_DATABASE"]
        self.DB_PORT = os.environ["DB_PORT"]
        self.DB_USER = os.environ["DB_USER"]
        self.DB_PASSWORD = os.environ["DB_PASSWORD"]
    
    def getDBConn(self):
        return psycopg2.connect(
            host = self.DB_HOSTNAME,
            database = self.DB_DATABASE,
            port = self.DB_PORT,
            user = self.DB_USER,
            password = self.DB_PASSWORD
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
