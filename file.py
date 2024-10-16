from flask import Flask
from flask import render_template

file = Flask(__name__)

@file.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    file.run()

