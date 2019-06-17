# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, g, render_template, session, redirect
from werkzeug.security import generate_password_hash
from .models import *
import time
import hashlib
user_info = Blueprint('user_info',__name__)

def valid_sign_up(username, password):
    '''
    对用户注册信息合法性进行判断
    不允许有相同用户名的用户
    '''
    if username is None or password is None:
        return False
    if User.query.filter_by(name=username).first() is not None:
        return False
    return True

@user_info.route('/sign_up', methods=['GET', 'POST'])
def sign():
    '''
    注册api,创建用户，并将用户的信息存入数据库
    在数据库中查找手机号，存在则非法，返回失败信息
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        # password = request.form.get('password')

        if valid_sign_up(username, password):
            user1 = User(name = username, hash_password = password)
            db.session.add(user1)
            db.session.commit()
            uid = User.query.filter_by(name=username).first().uid
            session["userId"] = str(uid)
            # 注册成功后重定向URL到"/id={uid}"用户个人主页
            return redirect("/id=" + str(uid))
        else:
            # 注册失败返回错误提示信息并刷新页面
            return render_template('sign_up.html', user_state = "fail")

    # 渲染用户注册页面
    return render_template('sign_up.html', user_state = "success")