# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, make_response, session
import os
from werkzeug.utils import secure_filename
import argparse
import json
import numpy as np
import requests
from .models import *
from keras.applications import inception_v3
from keras.preprocessing import image
import urllib
import time

others = Blueprint('others_',__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])

def allowed_file(filename):
    '''
    对用户上传文件类别进行校验
    只允许图片上传
    return 文件名称
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@others.route('/others', methods=['POST', 'GET'])
def upload():
    '''
    匿名用户使用inception_v3模型
    可对1000种事物进行粗分类
    '''
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Error file type, only for: 'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'"})

        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)

        fname = secure_filename(f.filename)

        ext = fname.rsplit('.',1)[1]

        # 使用系统时间命名图片，解决重名问题
        new_file = str(int(time.time())) + '.' + ext
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(new_file))
        f.save(upload_path)

        img = image.img_to_array(image.load_img(upload_path, target_size=(229, 229))) / 255.
        img = img.astype('float16')
 
        # 通过Simple_save构造的模型接口传输数据
        payload = {
        "instances": [{'input_image': img.tolist()}]
        }

        # 向TensorFlow-Serving发送Post请求
        r = requests.post('http://localhost:8501/v1/models/ImageClassifier1:predict', json=payload)
        pred = json.loads(r.content.decode('utf-8'))

        ################################################################################
        # 此模块用来对系统响应进行测试

        # start_time = time.time() 
        # r = requests.post(''http://localhost:8501/v1/models/ImageClassifier1:predict', json=payload)
        # end_time = time.time()
        # interval = end_time-start_time
        # print "Keras Time Use:",interval

        ###############################################################################

        # 对返回数据进行解码
        raw_info = inception_v3.decode_predictions(np.array(pred['predictions']))[0]

        # 构造json数据
        predicit_info = []
        for pre_info in raw_info:
            img_pre_data = {
                'id' : pre_info[0],
                'name' : pre_info[1],
                'acc' : pre_info[2] 
            }
            predicit_info.append(img_pre_data)

        json_info = json.dumps(predicit_info)

        upload_url = url_for('static', filename= './images/' + new_file)

        # 动态渲染upload_v2.html，前端显示图片预测信息
        return render_template('upload_v2.html',flag = "success", upload_pa = upload_url, info = predicit_info, home_url = request.url[:-6], uid = "", action_opt = "others")
    
    # 无预测信息或预测失败时传入参数flag = "fail"
    return render_template('upload_v2.html', flag = "fail", home_url = request.url[:-6], uid = "", action_opt = "others")

@others.route('/others/id=<userId>', methods=['POST', 'GET'])
def user_upload(userId):
    '''
    已登录用户使用inception_v3模型
    可对1000种事物进行粗分类
    记录用户图片上传及预测信息存入数据库
    '''
    if session.get("userId") == userId: # 用户登录状态校验
        # user = User.query.filter_by(uid=userId).first()
        # user.imgname = user.imgname + ",image2.jpg"
        # user.pre_info = user.pre_info + ",kite"
        # db.session.commit()
        if request.method == 'POST':
            f = request.files['file']
     
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "Error file type, only for: 'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'"})

            user_input = request.form.get("name")
     
            basepath = os.path.dirname(__file__)

            fname = secure_filename(f.filename)

            ext = fname.rsplit('.',1)[1]

            # 使用系统时间命名图片，解决重名问题
            new_file = str(int(time.time())) + '.' + ext
     
            upload_path = os.path.join(basepath, 'static/images', new_file)
            f.save(upload_path)

            img = image.img_to_array(image.load_img(upload_path, target_size=(229, 229))) / 255.
            img = img.astype('float16')
     
            # simple_save保存的传入格式
            payload = {
            "instances": [{'input_image': img.tolist()}]
            }

            # 向TensorFlow-Serving服务器发送Post请求
            r = requests.post('http://localhost:8501/v1/models/ImageClassifier1:predict', json=payload)
            pred = json.loads(r.content.decode('utf-8'))

            # 对原数据解码
            raw_info = inception_v3.decode_predictions(np.array(pred['predictions']))[0]

            # 构造Json返回值
            predicit_info = []
            for pre_info in raw_info:
                img_pre_data = {
                    'id' : pre_info[0],
                    'name' : pre_info[1],
                    'acc' : pre_info[2] 
                }
                predicit_info.append(img_pre_data)

            # 添加此图片预测历史到数据库
            image_info = Image(uid = userId, imgname = new_file, info = predicit_info[0]['name'])
            db.session.add(image_info)
            db.session.commit()

            json_info = json.dumps(predicit_info)

            upload_url = url_for('static', filename= './images/' + new_file)

            # 动态渲染upload_v2.html，显示图片分类成功信息
            return render_template('upload_v2.html',flag = "success", upload_pa = upload_url, info = predicit_info, home_url = request.url[:-6], uid = userId, action_opt = "others")
    else:
        print "fail"
        # 用户登陆校验失败是重定向URL到"/others"
        return redirect("/others")
 
    # 无预测信息或预测失败时传入参数flag = "fail"
    return render_template('upload_v2.html', flag = "fail", home_url = request.url[:-6], uid = userId, action_opt = "others")



