# -*- coding: utf-8 -*-
# @File: sql_config.py
# @Author: https://github.com/ohhal
# @Date: 2021/02/03
# @Desc: sql装饰器及sql
import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

flask_app_db_name = 'flask_app.db'

flask_app_db = os.path.join(BASE_DIR, flask_app_db_name)

tobe_verify_db_name = 'tobe_verify.db'

tobe_verify_db = os.path.join(BASE_DIR, tobe_verify_db_name)

verify_log_db_name = 'verify_log.db'

verify_log_db = os.path.join(BASE_DIR, verify_log_db_name)


# sql错误装饰器
def exception_handler(func):
    def wrapper(*args, **kwargs):
        result = {'code': 0, 'msg': None}
        try:
            result['msg'] = func(*args, **kwargs)
        except Exception as e:
            print(e)
            result['code'] = -1
        finally:
            return result

    wrapper.__name__ = func.__name__
    return wrapper
