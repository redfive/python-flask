#!/usr/bin/env python

from rest import app
from flask import render_template
from rest.models import User


@app.route("/")
def index():
    return "Welcome to my site."

@app.route("/hello/<user>")
def hello_user(user):
    result = User.query.filter_by(username=user).first()
    if result:
        return render_hello(result.username + '@' + result.email)
    else:
        return render_hello(None)

def render_hello(name):
    response =  render_template('hello.html', name=name)
    print response
    return response

if __name__ == "__main__":
    app.debug = True
    app.run()
