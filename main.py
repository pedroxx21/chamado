from flask import Flask

app = Flask(__name__)

@app.route("/")
def login():
    return 'Tela de login'

