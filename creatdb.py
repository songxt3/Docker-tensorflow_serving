from app import db
from app.models import *
if __name__ == '__main__':
	'''
	使用此文件创建数据库
	只需在第一次部署未创建数据库的情况下使用
	'''
    db.create_all()