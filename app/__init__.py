# -*- coding: utf-8 -*-
from flask import Flask
from up_photo import up_photo
from datetime import timedelta

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.send_file_max_age_default = timedelta(seconds=1)

app.register_blueprint(up_photo)