# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, make_response
import os
from werkzeug.utils import secure_filename
import argparse
import json
import numpy as np
import requests
from keras.applications import inception_v3
from keras.preprocessing import image

up_photo = Blueprint('upphoto',__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@up_photo.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Error file type, only for: 'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'"})

        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(upload_path)

        img = image.img_to_array(image.load_img(upload_path, target_size=(224, 224))) / 255.
        img = img.astype('float16')
 
        payload = {
        "instances": [{'input_image': img.tolist()}]
        }

        # sending post request to TensorFlow Serving server
        r = requests.post('http://localhost:8501/v1/models/ImageClassifier:predict', json=payload)
        pred = json.loads(r.content.decode('utf-8'))

        # Decoding the response
        # decode_predictions(preds, top=5) by default gives top 5 results
        # You can pass "top=10" to get top 10 predicitons

        raw_info = inception_v3.decode_predictions(np.array(pred['predictions']))[0]

        predicit_info = []
        for pre_info in raw_info:
            img_pre_data = {
                'id' : pre_info[0],
                'name' : pre_info[1],
                'acc' : pre_info[2] 
            }
            predicit_info.append(img_pre_data)

        json_info = json.dumps(predicit_info)

        print predicit_info

        upload_url = url_for('static', filename= './images/' + f.filename)
        flag = "success"

        print redirect(upload_url)

        return render_template('upload_v2.html',flag = "success", upload_pa = upload_url, info = predicit_info)
 
    return render_template('upload_v2.html', flag = "fail")