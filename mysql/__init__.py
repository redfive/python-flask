from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

all = ['app', 'db']

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from mysql import views

