# -*- coding: utf-8 -*-
from datetime import datetime, date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, use_native_unicode='utf8')

class User(db.Model):
    '''
    定义用户Model
    '''
    __tablename__ = 'User'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), doc='姓名', nullable=False, unique=True)
    hash_password = db.Column(db.String(128), doc='密码', nullable=False)

class Image(db.Model):
    '''
    定义图片历史记录Model
    '''
    __tablename__ = 'Image'
    __table_args__ = {'mysql_engine': 'InnoDB'}  # 支持事务操作和外键
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)
    imgname = db.Column(db.String(20), doc='姓名', nullable=False, unique=True)
    info = db.Column(db.String(128), doc='密码', nullable=False)