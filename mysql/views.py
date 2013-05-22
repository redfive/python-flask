from mysql import app
from flask import render_template, request
from mysql.models import User

@app.route("/")
def index():
    return render_hello(None)

@app.route("/hello/<user>")
def hello_user(user):
    result = User.query.filter_by(username=user).first()
    if result:
        return render_hello(result.username + '@' + result.email)
    else:
        return render_hello(None)

@app.route('/register')
def register_user():
    print request
    return 'hello'

def render_hello(name):
    response =  render_template('hello.html', name=name)
    return response

