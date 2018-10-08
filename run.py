from flask import Flask,render_template
# aaaaaa
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/python")
def hello_python():
    message = "Hello Python!"
    return render_template("test.html", message = message)

if __name__ == "__main__":
    app.run()