from flask import render_template, redirect,request,url_for,g,send_from_directory
from flask.ext.login import current_user,logout_user
from app import app
from app.models import *
from datetime import datetime
import json
import scipy as sp
from scipy import stats
import math
from app import flask_login,login_manager
import bcrypt
import os
from werkzeug import secure_filename


ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@login_manager.user_loader
def user_loader(email):
    users = Users.query.all()
    for user_obj in users:
        if email == user_obj.email:
            user = User()
            user.id = email
            return user
    return 

@login_manager.request_loader
def request_loader(request):
    users = Users.query.all()
    email = request.form.get("email")
    for user_obj in users:
        if email == user_obj.email:
            user = User()
            user.id = email
            user.is_authenticated = request.form.get("password") == user_obj.password
            return user
    return


def check_password(email,password):
    user_pw = str(Users.query.filter_by(email=email).first().password)
    print user_pw
    print password
    if bcrypt.hashpw(password,user_pw) == user_pw:
        return True
    else:
        return False
    
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    #explicitly force string type because of demands from bcrypt
    email = str(request.form.get("email"))
    password = str(request.form.get("password"))
    if check_password(email,password):
        user = User()
        user.id = email
        flask_login.login_user(user)
        
        return redirect(url_for("splash_page"))
    return render_template("login.html",error="username or password was incorrect, please try again")
    
@app.route("/splash_page",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def splash_page():
    return render_template("splash_page.html",current_user=current_user)


@app.route("/ingestion_engine",methods=["GET","POST"])
@flask_login.login_required
def ingestion_engine():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("ingestion_engine.html")



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/logout")
@flask_login.login_required
def logout():
    logout_user()
    return redirect(url_for("splash_page"))
