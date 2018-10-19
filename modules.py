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
        #self.attrs = ["id", "user_id", "calorie", "heart_rate", "steps_num", "temp", "datetime"]
    
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
    
    def getMaxID(self):
        conn = self.getDBConn()
        cursor = conn.cursor()
        sql = "select max(id) from {0}".format(self.tableName)
        cursor.execute(sql)
        result = cursor.fetchone()
        self.closeConn(cursor, conn)

        (currentID,) = result
        return currentID
    
    def dbInsert(self, record):
        '''
        [入力]
        ●record
        ・(dict){"attr1":data1, "attr2":data2,...}
        ・シリアルプライマリーキーであるidとdatetimeは引数にしない！
        ・idはgetMaxID()から，datetimeはSQLのnow()から取得する．
        '''
        attrs = ""
        datas = ""
        i = 0
        for attr,data in record.items():
            if i<len(record)-1:
                attrs += str(attr) + ","
                datas += "{0},".format(str(data)) if attr!="user_id" else "'{0}',".format(data)
                i += 1
            else:
                attrs += str(attr)
                datas += "{0}".format(str(data)) if attr!="user_id" else "'{0}'".format(data)

        conn = self.getDBConn()
        cursor = conn.cursor()
        id = str(self.getMaxID()+1)
        #sql = "insert into {0}(id,user_id,calorie,datetime) values({1},'a001',400,now())".format(self.tableName, id)
        sql = "insert into {0}(id,{1}) values({2},{3},now())".format(self.tableName, attrs, id, datas)
        cursor.execute(sql)
    
    def dbSelect(self, attr):
        '''
        [入力]
        ●attr
        ・(str)"項目1,項目2,..."
        ・すべての項目を取得する場合は"*"のみ．
        '''
        conn = self.getDBConn()
        cursor = conn.cursor()
        sql = "select {0} from {1} order by id asc".format(attr, self.tableName)
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeConn(cursor, conn)
        return result

class BasicProcess():
    def __init__(self):
        self.dp = DBProcess()
        #self.sp = SensorProcess()
    
    def getDBCalorie(self):
        calorie = self.dp.dbSelect("calorie")
        return calorie
    
    #def shapeData():
