from flask import Flask,render_template
<<<<<<< HEAD
from modules import DBProcess
from modules import BasicProcess
=======
from modules import Modules
>>>>>>> 0f8bc87b795508baea0258eedcf09fdf29b6aab7

app = Flask(__name__)
dp = DBProcess()

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/python")
def hello_python():
    message = "Hello Python!"
    return render_template("test.html", message = message)

@app.route("/front-test")
def front_test():
    return render_template("front-test.html")

<<<<<<< HEAD

@app.route("/test_postgresql")
def hello_postgresql():
    result = dp.dbSelect("*")
    return result


=======
'''
@app.route("/test_postgresql")
def hello_postgresql():pass
'''
>>>>>>> 0f8bc87b795508baea0258eedcf09fdf29b6aab7
if __name__ == "__main__":
    app.run()