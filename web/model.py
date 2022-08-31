from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model) :
    __tablename__ = 'user'
    index = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password) :
        self.username = username
        self.password = password

class board(db.Model) :
    __tablename__ = 'board'
    index = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32))
    filename = db.Column(db.Text)
    word1 = db.Column(db.Text)
    word2 = db.Column(db.Text)
    word3 = db.Column(db.Text)
    labeling = db.Column(db.Integer)
