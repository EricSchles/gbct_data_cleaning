from flask import render_template, redirect,request,url_for,g,send_from_directory
from flask.ext.login import current_user,logout_user
from app import app
from app.models import *
from datetime import datetime
import json
import math
from app import flask_login,login_manager
import bcrypt
import os
from app.validation import *
from werkzeug import secure_filename
from logger import *
from upload_check import *

####################################
# Splash Page and General Resources
####################################

@app.route("/splash_page",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def splash_page():
    return render_template("splash_page.html",current_user=current_user)

######################
#upload files section
######################

ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS = set(['csv','xlsx','xls'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/ingestion_engine",methods=["GET","POST"])
@flask_login.login_required
def ingestion_engine():
    remove_bad_files()
    if request.method == 'POST':
        file = request.files['file']
        errors = []
        if file and allowed_file(file.filename):
            filename = file.filename #was using secure_filename but this isn't standard naming convention and I have no good solution at present
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            local_file = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            error = perform_checks(filename,local_file)
            if not check_for_all_files():
                return render_template("ingestion_engine.html",error=error,
                                       files_are_missing="files are missing",
                                       missing_files=get_missing_files())
            else:
                return render_template("ingestion_engine.html",
                                       files_are_missing=None,
                                       missing_files=get_missing_files())
        
    if not check_for_all_files():
        return render_template("ingestion_engine.html",
                               files_are_missing="files are missing",
                               missing_files=get_missing_files())
    else:
        return render_template("ingestion_engine.html",
                               files_are_missing=None,
                               missing_files=get_missing_files())

                               
@app.route("/download_file",methods=["GET","POST"])
@flask_login.login_required
def download_files():
    if check_for_all_files():
        return redirect(url_for('uploaded_file',
                                filename="data.csv"))
    else:
        return redirect(
            url_for("ingestion_engine.html",
                    files_are_missing="files are missing",
                    missing_files=get_missing_files()
            ))
                        
                        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

######################
# Login section
######################

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

@app.route("/logout")
@flask_login.login_required
def logout():
    logout_user()
    return redirect(url_for("splash_page"))

######################
# Logging section
######################

@app.route("/logs",methods=["GET","POST"])
@flask_login.login_required
def logs_console():
    if current_user.id == "admin":
        #To Do:
        #Make this more granular allow for querying by log type
        #All for querying by time stamp
        return render_template("logs_console.html",logs=Logs.query.all())
    else:
        return """
        <!doctype html>
        <head></head>
        <body>
        <p> You are not an admin user, only admin's may see this page</p>
        </html>
        """
