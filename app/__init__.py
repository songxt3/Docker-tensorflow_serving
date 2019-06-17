# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, session, redirect
from others import others
from flower import flower
from user_login import user_login
from user_info import user_info
from datetime import timedelta
from .models import *
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import time

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode='utf8')
auth = HTTPBasicAuth()

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "songxt123456789"
app.send_file_max_age_default = timedelta(seconds=1)

app.register_blueprint(others)
app.register_blueprint(flower)
app.register_blueprint(user_login)
app.register_blueprint(user_info)

@app.route("/")
def home():
    '''
    用户匿名使用主页
    模型选择，用户注册和登录
    '''
    user_judge = False
    user_name = "" # 匿名用户
    url = request.url
    return render_template('home.html', others_url = url, user_judge = user_judge, user_name = user_name, uid = "")

@app.route("/id=<userID>")
def user_home(userID):
    '''
    已登陆用户使用系统主页
    模型选择
    '''
    user_judge = False
    user_name = ""
    if userID != session.get("userId"):
        time.sleep(3)
    if userID != session.get("userId"):
    	return redirect("/")
    else:
    	user_judge = True
    	user_name = User.query.filter_by(uid = userID).first().name
    url = request.url
    return render_template('home.html', others_url = url, user_judge = user_judge, user_name = user_name, uid = userID)



