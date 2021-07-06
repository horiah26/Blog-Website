from flask import Flask, render_template
import quoteGenerator
app = Flask(__name__)

@app.route("/")
def index():
    return "Index"

@app.route("/hello/<name>")
def hello(name):

    quote = quoteGenerator.quote()
    return render_template(
    'test.html',**locals())

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/members/<string:username>")
def getMember(username):
    return username

if __name__ == "__main__":
    app.run()


