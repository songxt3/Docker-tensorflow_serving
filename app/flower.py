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
import time
import cv2
import sys

flower = Blueprint('flower_',__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])

def allowed_file(filename):
    '''
    控制文件上传类型
    只允许图片上传
    return 文件名称
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def read_image(filename, resize_height, resize_width, normalization=False):
    '''
    图片预处理
    resize至299*299后归一化
    return 处理后的图片
    '''
    bgr_image = cv2.imread(filename)
    if len(bgr_image.shape)==2:
        print("Warning:gray image",filename)
        bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_GRAY2BGR)

    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    if resize_height>0 and resize_width>0:
        rgb_image=cv2.resize(rgb_image,(resize_width,resize_height))
    rgb_image=np.asanyarray(rgb_image)
    if normalization:
        rgb_image=rgb_image/255.0
    return rgb_image

@flower.route('/flower', methods=['POST', 'GET'])
def upload():
    '''
    匿名用户使用inception_v3训练的花卉模型
    可对17种花卉进行细分
    '''
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Error file type, only for: 'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'"})

        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)

        fname = secure_filename(f.filename)

        ext = fname.rsplit('.',1)[1]

        # 使用系统时间命名图片，解决图片重名问题
        new_file = str(int(time.time())) + '.' + ext
 
        upload_path = os.path.join(basepath, 'static/images', new_file)
        f.save(upload_path)

        img = read_image(upload_path, 299, 299, normalization=True)
        img = img[np.newaxis, :]

        # simple_save保存的传入格式
        payload = {
        "inputs": {"input": img.tolist(), "keep_prob": 1.0, "is_training": False}
        }

        # 向TensorFlow-Serving发送Post请求
        r = requests.post('http://localhost:8501/v1/models/ImageClassifier2:predict', json=payload)

        ################################################################################
        # 此模块用来测试系统响应速度

        # model_url = 'http://imgsort.natapp1.cc' # 测试URL
        # start_time = time.time()
        # r = requests.post('http://localhost:8501/v1/models/ImageClassifier2:predict', json=payload)
        # end_time = time.time()
        # interval = end_time-start_time
        # print "TF-Silm Time Use:",interval
        ################################################################################

        pres_pos = json.loads(r.content)

        pres_list = pres_pos['outputs'][0]

        flower_name = ['Daffodil', 'Snowdrop', 'LilyValley', 'Bluebell', 'Crocus', 'Iris', 'Tigerlily', 'Tulip', 'Fritillary', 'Sunflower', 'Daisy', 'Colts Foot', 'Dandelion', 'Cowslip', 'Buttercup', 'Windflower', 'Pansy']

        # 构造Json数据
        predicit_info = []
        for i in range(0, 5): # 原数据解码过程，提取Top-5可能性
            max_num = max(pres_list)
            max_index = pres_list.index(max(pres_list))
            img_pre_data = {
                'id': max_index,
                'name': flower_name[max_index],
                'acc': max_num
            }
            predicit_info.append(img_pre_data)
            pres_list[max_index] = -sys.maxint - 1

        json_info = json.dumps(predicit_info)

        upload_url = url_for('static', filename= './images/' + new_file)

        # 动态渲染upload_v2.html，前端显示图片预测信息
        return render_template('upload_v1.html',flag = "success", upload_pa = upload_url, info = predicit_info, home_url = request.url[:-6], uid = "", action_opt = "flower")
 
    # 无预测信息或预测失败时传入参数flag = "fail"
    return render_template('upload_v1.html', flag = "fail", home_url = request.url[:-6], uid = "", action_opt = "flower")

@flower.route('/flower/id=<userId>', methods=['POST', 'GET'])
def user_upload(userId):
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

            # 使用系统时间命名图片，解决图片重名问题
            new_file = str(int(time.time())) + '.' + ext
     
            upload_path = os.path.join(basepath, 'static/images', new_file)
            f.save(upload_path)

            img = read_image(upload_path, 299, 299, normalization=True)
            img = img[np.newaxis, :]

            # simple_save保存的传入格式
            payload = {
            "inputs": {"input": img.tolist(), "keep_prob": 1.0, "is_training": False}
            }

            # 向TensorFlow-Serving发送Post请求
            r = requests.post('http://localhost:8501/v1/models/ImageClassifier2:predict', json=payload)

            pres_pos = json.loads(r.content)

            pres_list = pres_pos['outputs'][0]

            flower_name = ['Daffodil', 'Snowdrop', 'LilyValley', 'Bluebell', 'Crocus', 'Iris', 'Tigerlily', 'Tulip', 'Fritillary', 'Sunflower', 'Daisy', 'Colts Foot', 'Dandelion', 'Cowslip', 'Buttercup', 'Windflower', 'Pansy']

            # 构造Json数据
            predicit_info = []
            for i in range(0, 5): # 原数据解码，提取Top-5可能性
                max_num = max(pres_list)
                max_index = pres_list.index(max(pres_list))
                img_pre_data = {
                    'id': max_index,
                    'name': flower_name[max_index],
                    'acc': max_num
                }
                predicit_info.append(img_pre_data)
                pres_list[max_index] = -sys.maxint - 1

            # 提交此次图片预测历史到服务器
            image_info = Image(uid = userId, imgname = new_file, info = predicit_info[0]['name'])
            db.session.add(image_info)
            db.session.commit()

            json_info = json.dumps(predicit_info)

            upload_url = url_for('static', filename= './images/' + new_file)

            # 动态渲染upload_v2.html，前端显示图片预测信息
            return render_template('upload_v1.html',flag = "success", upload_pa = upload_url, info = predicit_info, home_url = request.url[:-6], uid = userId, action_opt = "flower")
    else:
        print "fail"
        # 用户登录校验失败，重定向URL到"/flower"匿名使用
        return redirect("/flower")
    
    # 无预测信息或预测失败时传入参数flag = "fail"
    return render_template('upload_v1.html', flag = "fail", home_url = request.url[:-6], uid = userId, action_opt = "flower")


