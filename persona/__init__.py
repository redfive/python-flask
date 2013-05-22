from flask import Flask

all = ['app']

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py')

# import this after creating the app as the views use app
from persona import views

