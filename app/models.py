from app import db
from app import flask_login
from datetime import datetime
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
    
class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime)
    user = db.Column(db.String)
    action_taken = db.Column(db.String)

    def __init__(self,time_stamp,user,action_taken):
        self.time_stamp = time_stamp
        self.user = user
        self.action_taken = action_taken
    def __repr__(self):
        return "<Log %r>" % str(self.action_taken)


