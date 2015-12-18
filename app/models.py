from app import db
from app import flask_login

class User(flask_login.UserMixin):
    pass

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean,default=False)

    def __init__(self,email,password,authenticated=False):
        self.email = email
        self.password = password
        self.authenticated = authenticated
    def __repr__(self):
        return "<Users %r>" % str(self.email)
    
