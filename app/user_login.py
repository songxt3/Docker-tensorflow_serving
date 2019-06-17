# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, g, render_template, make_response, session, redirect, abort, url_for
from werkzeug.security import check_password_hash
from .models import *
from functools import wraps
import json
import os

user_login = Blueprint('user_login', __name__)

def verify_password(username, password):
    '''
    用户登录信息校验
    校验用户名存在行及用户名密码一致性
    '''
    user = User.query.filter_by(name=username).first()
    if user == None:
        return False
    if check_password_hash(user.hash_password, password):
        return True
    return False

@user_login.route('/login', methods=['GET', 'POST'])
def sign():
    '''
    用户登陆模块
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if verify_password(username, password):
            user = User.query.filter_by(name=username).first()
            session["userId"] = str(user.uid)
            # 登陆成功，重定向URL到’login/id={uid}‘用户历史记录界面
            return redirect('/login/id='+ str(user.uid))
        else:
            # 用户不存在
            return render_template('login.html', user_state = "fail")
    else:
        # 用户登陆界面
        return render_template('login.html', user_state = "success")

@user_login.route('/login/id=<userId>', methods=['GET', 'POST'])
def user_sign(userId):
    '''
    用户历史记录模块
    校验用户成功后可查看个人上传图片及预测信息
    '''
    # error = jsonify({'status_code': '401', 'error_message': 'Unauthorized'})
    db.session.commit()
    user = User.query.filter_by(uid = userId).first()
    images_info = Image.query.filter_by(uid = userId).all()
    # images_info_test = Image.query.filter_by(uid = userId).first()
    # print images_info_test.imgname.__class__
    img_name = []
    img_info = []
    if user == None:
        # 用户不存在
        abort(401)
    if session.get("userId") == userId: # 用户登陆状态校验
        print images_info
        if images_info != []:
            # 遍历用户历史记录
            for img in images_info:
                img_name.append(img.imgname)
                img_info.append(img.info)
            # 构造返回数据格式
            dictionary = dict(zip(img_name, img_info))

            return render_template('login_success.html', name = user.name, uid = user.uid, info_mapping = dictionary)
        else:
            # 无历史记录
            return render_template('login_success.html', name = user.name, uid = user.uid, info_mapping = "")
    else:
        # 用户校验失败
        return redirect('/login')
    abort(401)

@user_login.route('/logout', methods=['GET', 'POST'])
def login_out():
    '''
    用户退出模块
    '''
    # 更新session用户状态
    session.pop("userId", None)
    # 重定向URL到用户登录界面
    return redirect('login')

@user_login.route('/drop/<userId>/<ImgName>', methods=['GET', 'POST'])
def delete_file(userId, ImgName):
    '''
    删除历史记录模块
    通过此API删除指定用户历史记录
    '''
    img_list = Image.query.filter_by(uid = userId, imgname = ImgName).first()
    print img_list
    if img_list != None:
        name = img_list.imgname
        basepath = os.path.dirname(__file__)
        delete_path = os.path.join(basepath, 'static/images', name)
        # 删除图片
        os.remove(delete_path)
        # 删除数据库对应的历史记录条目
        db.session.delete(img_list)
        db.session.commit()
    # 更新历史记录页面
    return redirect("/login/id=" + str(userId))