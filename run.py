# -*- coding: UTF-8 -*-
from app import app
if __name__ == '__main__':
    '''
    开启 debug模式
    # 设置 host='0.0.0.0'
    '''
    app.run(debug=True, host='0.0.0.0')