from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

all = ['app', 'db', 'mananger']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

from rest.api import UserAPI
