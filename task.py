# -*- coding: utf-8 -*-
# @File: task.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/26
# @Desc: 创建task id

from celery.exceptions import SoftTimeLimitExceeded

from Celery import verify_celery_app
from methods._verify import solver


@verify_celery_app.task
def add_task(platform, params):
    try:
        return solver(platform,params)
    except SoftTimeLimitExceeded:  # 任务超时
        return dict(
            code=-1,
            msg='解决验证码时超出任务执行设定的最大时间',
            text=None
        )


if __name__ == '__main__':
    add_task.apply_async()
