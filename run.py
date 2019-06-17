# -*- coding: UTF-8 -*-
from app import app
from waitress import serve

if __name__ == '__main__':
    '''
    开启 debug模式
    # 设置 host='0.0.0.0'
    '''
    app.run(debug=True, host='0.0.0.0')


# 模型部署
# serve(app, host='0.0.0.0', port=5000)
    