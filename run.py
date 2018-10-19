from flask import Flask,render_template

from modules import DBProcess
from modules import BasicProcess

app = Flask(__name__)
dp = DBProcess()

@app.route("/")
def hello_world():
    message = "Hello Python!"
    return render_template("test.html", message = message)

@app.route("/front_test")
def front_test():
    return render_template("front_test.html")
'''
@app.route("/vr")
def vr():
    return render_template("vr.html")
'''


@app.route("/test_postgresql")
def hello_postgresql():
    dp.dbInsert({"user_id":"a001", "steps_num":12230, "calorie":300})
    result = dp.dbSelect("id,calorie,datetime")
    return render_template("test.html", psqldatas = result)


if __name__ == "__main__":
    app.run()