from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.login as flask_login
import pickle
from tools import Anonymous
import os


UPLOAD_FOLDER = os.getcwd()+"/uploads"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" #os.environ["DATABASE_URL"]
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = pickle.load(open("secret_key.pickle","r"))
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
db = SQLAlchemy(app)

from app import views, models
