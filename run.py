from flask import Flask,render_template
from modules import Modules

app = Flask(__name__)

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

'''
@app.route("/test_postgresql")
def hello_postgresql():pass
'''
if __name__ == "__main__":
    app.run()