from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Index"

@app.route("/hello/<name>")
def hello(name):
    return render_template(
    'test.html',name=name)

@app.route("/members")
def members():
    return "Members"

@app.route("/members/<string:username>")
def getMember(username):
    return username

if __name__ == "__main__":
    app.run()