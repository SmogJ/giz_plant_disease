from flask import Flask
apps = Flask(__name__)

@apps.route('/')
def hello_world():
    return "hello world"


if __name__=="__main__":
    apps.run()