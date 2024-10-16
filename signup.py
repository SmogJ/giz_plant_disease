from flask import Flask
from flask import render_template

signup = Flask(__name__)

@signup.route("/")
def index():
    return render_template("signup.html")

if __name__=="__main__":
    signup.run()

