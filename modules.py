import os
import datetime
import psycopg2

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
    
    '''
    def getMaxID(self):
        with self.getDBConn() as conn:
            with conn.cursor() as cursor:
                sql = "select max(id) from {0};".format(self.tableName)
                cursor.execute(sql)
                result = cursor.fetchone()
                (currentID,) = result
        return currentID
    '''

    def dbInsert(self, record):
        '''
        [引数]
        ●record
        ・(dict){"attr1":data1, "attr2":data2,...}
        ・シリアルプライマリーキーであるidは引数にしない！
        ・idはgetMaxID()からから取得する．
        [変更]
        ・datetimeはSQLのnow()から，ではなく引数に含めて受け取る．
        '''
        attrs = ""
        datas = ""
        i = 0
        for attr,data in record.items():
            if i<len(record)-1:
                attrs += str(attr) + ","
                datas += "{0},".format(str(data)) if attr!="user_id" and attr!="datetime" else "'{0}',".format(data)
                i += 1
            else:
                attrs += str(attr)
                datas += "{0}".format(str(data)) if attr!="user_id" and attr!="datetime" else "'{0}'".format(data)

        with self.getDBConn() as conn:
            with conn.cursor() as cursor:
                '''
                #dbnum = self.getMaxID()
                #print("\n\n\n\n\n\n\n\ndbMax : {0}\n\n\n\n\n\n\n".format(dbnum)) # herokuのlogsで確認！！
                id = 0 if not dbnum else dbnum+1
                sql = "insert into {0}(id,{1}) values({2},{3})".format(self.tableName, attrs, id, datas)
                '''
                sql = "insert into {0}({1}) values({2})".format(self.tableName, attrs, datas)
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
        self.caloriePerExercise = {1:200, 2:400, 3:360, 4:600}
    
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
            # psqlで固定小数点型Decimalとなっているが，JSで扱えないのでここでfloatに変換．
            calories.append({"id":_calorie[0], "calorie":float(_calorie[1]), "datetime":_calorie[2]})
        
        return calories

    def getDayConsumedCalorie(self, DB_data):
        '''
        [引数]
        ●(list(dict))[{"id": data1_1, "calorie":data1_2, "datetime":data1_3},{"id": data2_1, ...},...]
        ・DBから取得した日分けされていない全データ
        [戻り値]
        ●(dict){"X月Y日":calorie1, "X月Z日":calorie2, ...}
        ・日ごとのカロリー総和を求めた辞書
        '''
        caloriePerDay = {}
        date = ""
        sum = 0
    
        for num in range(len(DB_data)-1):
            currentDay  =  DB_data[num]["datetime"].day
            nextDay = DB_data[num+1]["datetime"].day
            sum += DB_data[num]["calorie"] # カロリーを加算
            if currentDay != nextDay: # 日が違った場合
                date = "{0}/{1}".format(DB_data[num]["datetime"].month, currentDay)
                caloriePerDay[date] = sum # currentDayの1日カロリーをリストに格納
                if num+1 == len(DB_data)-1: # 日付が異なりつつ，最後のデータに到達していた場合
                    date = "{0}/{1}".format(DB_data[num+1]["datetime"].month, nextDay)
                    caloriePerDay[date] = DB_data[num+1]["calorie"]
                    break
                sum = 0

            if num+1 == len(DB_data)-1: # 日付が一致しつつ，最後のデータに到達していた場合
                date = "{0}/{1}".format(DB_data[num]["datetime"].month, currentDay)
                sum += DB_data[num+1]["calorie"]
                caloriePerDay[date] = sum
            
        return caloriePerDay, date

    def get15minConsumedCaloire(self, DB_data): # ここでちょっと挙動不審あり．動かなくなったら再デプロイして．
        '''
        [引数]
        ●(list(dict))[{"id": data1_1, "calorie":data1_2, "datetime":data1_3},{"id": data2_1, ...},...]
        ・DBから取得した全データ
        [戻り値]
        ●(dict){"X字Y分":calorie, "X時Z分":calorie, ...}
        ・15分ごとのカロリー総和を求めた辞書
        '''
        caloriePer15min = {}
        for record in DB_data:
            dt = record["datetime"]
            time = "{0}/{1}/{2}-{3}:{4}".format(str(dt.year).zfill(2), str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2)) # テンプレート側でtojsonするときになぜか数字大小(文字コード順？)でソートされてしまうから，0で2桁合わせし，JS側で日付・時刻を分割しやすいように「-」を区切り文字にする
            caloriePer15min[time] = record["calorie"] # キー：時刻，バリュー：カロリー
        
        return caloriePer15min

    def getRestCalorie(self, caloriePerDay):
        rest = 0
        '''
        getKey = list(caloriePerDay.keys())
        num = len(getKey)
        rest = self.minDayCalorie - caloriePerDay[getKey[num-1]]
        '''
        getValue = list(caloriePerDay.values())
        rest = self.minDayCalorie - getValue[len(getValue)-1]
        return rest

    def selectExercise(self, DB_data):
        #num = len(DB_data)-1
        eval = DB_data[-1]["calorie"]
        if eval >=179:
            return "弱", "movie1"
        elif eval < 179 and eval >= 143:
            return "中", "movie2"
        else:
            return "強", "movie3"

    '''
    def getExerciseTime(self, rest):
        times = {}
        if rest > 0:
            for key,value in self.caloriePerExercise.items():
                times[key] = rest/value
        else:
            for key,value in self.caloriePerExercise.items():
                times[key] = 0
        return times
    '''

    def getGraphDatas(self, data, dataNum):
        '''
        ●Python→JSでjsonを使う
        http://hungrykirby.hatenablog.com/entry/2017/06/13/083455
        [入力]
        ●(dict){"key1":data1, "key2":data2, ...}
        ●(int)dataNum
        [戻り値]
        ●(dict){"key1":data1, "key2":data2, ...}
        ●dataNumの数だけ後ろの辞書を抽出したもの
        '''
        newDict = {}
        startIndex = 0 if (len(data)-dataNum<0) else len(data)-dataNum
        for i, (k,v) in enumerate(data.items()):
            if i>=startIndex:
                newDict[k] = data[k]
        return newDict