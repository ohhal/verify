# -*- coding: utf-8 -*-
# @File: Celery.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/28
# @Desc: celery
from __future__ import absolute_import
from celery import Celery


verify_celery_app = Celery('verify_celery')
# 加载配置模块
verify_celery_app.config_from_object('config')

if __name__ == '__main__':
    verify_celery_app.start()
