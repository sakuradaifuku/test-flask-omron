import os
import datetime
import psycopg2
import fitbit, time

class SensorProcess():
    def __init__(self):
        self.dp = DBProcess()
        # メモしたID等
        self.CLIENT_ID = os.environ["CLIENT_ID"]
        self.CLIENT_SECRET = os.environ["CLIENT_SECRET"]
        self.ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
        self.REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]

        # ID等の設定
        self.client = fitbit.Fitbit(self.CLIENT_ID,                                                                self.CLIENT_SECRET,
                            access_token=self.ACCESS_TOKEN,
                            refresh_token=self.REFRESH_TOKEN,
                            )

    def getDataFromFitbit(self):
        count = 0 # 10000レコード(2000回)のカウントに使う
        # data_from_fitbit = []
        while count < 2000:
            #現在の年月日，時刻
            today = datetime.datetime.now()
            today_before_minutes = today + datetime.timedelta(minutes=-5)

            #消費カロリー関連のデータ取得
            raw_data = self.client.intraday_time_series("activities/calories", base_date="today", detail_level="1min", start_time="{0}:{1}".format(today_before_minutes.hour, today_before_minutes.minute), end_time="{0}:{1}".format(datetime.datetime.now().hour, datetime.datetime.now().minute))
            list_of_dict_cal_time = raw_data["activities-calories-intraday"]["dataset"]
            len_dicts_cal_time = len(list_of_dict_cal_time)

            #カロリーのリストを作成
            calories_list =[]
            for i in range(len_dicts_cal_time):
                tmp = list_of_dict_cal_time[i]["value"]
                tmp = float(f"{tmp:.2f}") #小数点2桁まで
                calories_list.append(tmp)

            #時間のリスト(str)を作成
            str_time_list = []
            for i in range(len_dicts_cal_time):
                tmp = list_of_dict_cal_time[i]["time"]
                str_time_list.append(tmp)  #["00:00:00"]

            #上で作った文字列の時刻リストをdatetime型に
            str_split_time = []
            for i in range(len_dicts_cal_time):
                tmp = str_time_list[i].split(":")
                str_split_time.append(tmp) # [["00", "00", "00"], ・・]
            #ここでdatetimeに変更
            datetime_time = []
            for i in range(len_dicts_cal_time):
                datetime_time.append(datetime.datetime(int(today.year), int(today.month), int(today.day), int(str_split_time[i][0]), int(str_split_time[i][1]), int(str_split_time[i][2])))

            #calories_listとdatetime_timeから辞書を作成，キー設定
            #辞書のリスト作成
            for i in range(len_dicts_cal_time):
                tmp = {"datetime": datetime_time[i], "calories": calories_list[i]}
                tmp["user_id"] = "a001" # user_id（固定）の追加
                self.dp.dbInsert(tmp)
                # data_from_fitbit.append(tmp)

            count += 1
            time.sleep(120)

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
                id = str(self.getMaxID()+1)
                sql = "insert into {0}(id,{1}) values({2},{3})".format(self.tableName, attrs, id, datas)
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
            calories.append({"id":_calorie[0], "calorie":_calorie[1], "datetime":_calorie[2]})
        
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

    def get15minConsumedCaloire(self, DB_data):
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
            time = "{0}:{1}".format(record["datetime"].hour,record["datetime"].minute)
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

    def selectExercise(self, rest):
        if rest <= 0:
            return -1
        elif rest < 200:
            return "弱", "movie1"
        elif rest < 500:
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