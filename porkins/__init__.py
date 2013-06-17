from flask import Flask

all = ['app', 'hostname']

app = Flask('porkins', static_folder='static')

# TODO: handle production, staging, test, develop configurations
app.config.from_pyfile('config.py')

# used for Mozilla Persona - should probably come from app.config
hostname = 'http://localhost:5000'

# import this after creating the app as the views use app
from porkins import views

