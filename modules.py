import os, datetime
import psycopg2

class SensorProcess():
    def __init__(self):pass
    def insertSensorData(self):
        pass

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
    
    def getMaxID(self):
        with self.getDBConn() as conn:
            with conn.cursor() as cursor:
                sql = "select max(id) from {0}".format(self.tableName)
                cursor.execute(sql)
                result = cursor.fetchone()
                (currentID,) = result
        return currentID
    
    def dbInsert(self, record):
        '''
        [引数]
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

        with self.getDBConn() as conn:
            with conn.cursor() as cursor:
                id = str(self.getMaxID()+1)
                sql = "insert into {0}(id,{1},datetime) values({2},{3},now())".format(self.tableName, attrs, id, datas)
                cursor.execute(sql)
                conn.commit()
    
    def dbSelect(self, attr):
        '''
        [引数]
        ●attr
        ・(str)"項目1,項目2,..."
        ・すべての項目を取得する場合は"*"のみ．
        [戻り値]
        ●(list)[data1,data2,...]
        ・対応するアトリビュートのみ．
        '''
        with self.getDBConn() as conn:
            with conn.cursor() as cursor:
                sql = "select {0} from {1} order by id asc".format(attr, self.tableName)
                cursor.execute(sql)
                result = cursor.fetchall()
        return result

class BasicProcess():
    def __init__(self):
        self.dp = DBProcess()
        #self.sp = SensorProcess()
        self.minDayCalorie = 2000
    
    def getDBCalorie(self):
        calorie = self.dp.dbSelect("id,calorie,datetime")
        return calorie
    
    def shapeCalorieData(self, _calories):
        '''
        [引数]
        ●(list(list))[[data1_1,data1_2,data1_3],[data2_1,...],...]
        [戻り値]
        ●(list(dict))[{"id": data1_1, "calorie":data1_2, "datetime":data1_3},{"id": data2_1, ...},...]
        '''
        calories = []
        for _calorie in _calories:
            calories.append({"id":_calorie[0], "calorie":_calorie[1], "datetime":_calorie[2]})
        
        return calories

    def getDayConsumedCalorie(self, DB_data):
        caloriePerDay = {}
        sum = 0
    
        for num in range(len(DB_data)-1):
            currentDay  =  DB_data[num]["datetime"].day
            nextDay = DB_data[num+1]["datetime"].day
            sum += DB_data[num]["calorie"] # カロリーを加算
            if currentDay != nextDay: # 日が違った場合
                caloriePerDay[currentDay] = sum # currentDayの1日カロリーをリストに格納
                if num+1 == len(DB_data)-1: # 日付が異なりつつ，最後のデータに到達していた場合
                    caloriePerDay[nextDay] = DB_data[num+1]["calorie"]
                    break
                sum = 0

            if num+1 == len(DB_data)-1: # 日付が一致しつつ，最後のデータに到達していた場合
                sum += DB_data[num+1]["calorie"]
                caloriePerDay[currentDay] = sum
            
        return caloriePerDay