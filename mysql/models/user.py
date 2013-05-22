from mysql import db

class User(db.Model):
    username = db.Column(db.String(80), unique=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__ (self, username, email):
        self.validate(email)
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def validate(self, data):
        pass

