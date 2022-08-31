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