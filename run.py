from flask import Flask, render_template
import threading

from modules import BasicProcess, SensorProcess#, DBProcess

app = Flask(__name__)
bp = BasicProcess()
sp = SensorProcess()
# スレッドの生成
thread_fitbit = threading.Thread(target=sp.getDataFromFitbit())
thread_flask = threading.Thread(target=flask_run())

@app.route("/")
def hello_world():
    message = "Hello Python!"
    return render_template("test.html", message = message)

@app.route("/front_test")
def front_test():
    dbData = bp.getDBCalorie()
    calories = bp.shapeCalorieData(dbData)
    calorieperday, currentDay = bp.getDayConsumedCalorie(calories)
    calorieperfift = bp.get15minConsumedCaloire(calories)

    calorieperdayForGraph = bp.getGraphDatas(calorieperday, 15)
    calorieperfiftForGraph = bp.getGraphDatas(calorieperfift, 15)
    currentCalorie = calorieperdayForGraph[currentDay]
    restCalorie = bp.getRestCalorie(calorieperday)
    exerciseRank, movieNum = bp.selectExercise(restCalorie)
    return render_template("front_test.html", 
                calorieperday = calorieperdayForGraph, # リストに日本語含めないように．含める場合は工夫が必要．
                calorieperfift = calorieperfiftForGraph,
                currentCalorie = currentCalorie,
                restCalorie = restCalorie,
                exerciseRank = exerciseRank,
                movieNum = movieNum
                )

@app.route("/test_postgresql")
def hello_postgresql():
    dbData = bp.getDBCalorie()
    calories = bp.shapeCalorieData(dbData)
    calorieperday, currentDay = bp.getDayConsumedCalorie(calories)
    return render_template("test.html", psqldatas = calories, calorieperday = calorieperday)


def flask_run():
    app.run()

if __name__ == "__main__":
    thread_flask.start()
    thread_fitbit.start()
    #flask_run()