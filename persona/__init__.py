from flask import Flask

all = ['app']

app = Flask(__name__, static_folder='static')

# set the secret key to be used with sessions
app.secret_key = '\xdfR\xd7.U%%T\x89hL\xc1\t\xd6D\xc8t\xe2]*\xa13\xf2\xd9'
