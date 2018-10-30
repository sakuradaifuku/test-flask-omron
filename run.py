from flask import Flask, render_template

from modules import BasicProcess

app = Flask(__name__)
bp = BasicProcess()

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
    currentCalorie = round(calorieperdayForGraph[currentDay],2)
    restCalorie = round(bp.getRestCalorie(calorieperday),2)
    exerciseRank, movieNum = bp.selectExercise(restCalorie)
    return render_template("front_test.html", 
                calorieperday = calorieperdayForGraph, # リストに日本語含めないように．含める場合はensure_ascii=Falseのオプションが必要？
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

if __name__ == "__main__":
    app.run()