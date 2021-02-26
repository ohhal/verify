# -*- coding: utf-8 -*-
# @File: config.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/28
# @Desc: 配置文件
from __future__ import absolute_import

# broker
BROKER_URL = 'redis://127.0.0.1:6379/0'
# backen
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# 导入任务，如tasks.py
CELERY_IMPORTS = ('task',)
# 列化任务载荷的默认的序列化方式
CELERY_TASK_SERIALIZER = 'json'
# 结果序列化方式
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'

# 任务过期时间,celery任务执行结果的超时时间 15 min
CELERY_TASK_RESULT_EXPIRES = 60 * 15

# celery worker的并发数，默认是服务器的内核数目,也是命令行-c参数指定的数目
CELERYD_CONCURRENCY = 4
# celery worker 每次去redis预取任务的数量
CELERYD_PREFETCH_MULTIPLIER = 10
# 让每个worker执行n个任务，就销毁。防止内存泄漏。
CELERYD_MAX_TASKS_PER_CHILD = 100
CELERYD_FORCE_EXECV = True

# 规定完成任务的时间
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 5  # 300秒超时

##  下面是服务的所有配置
# 勿修改
anti_key = ''
confluence_key = ''
Tcaptcha_key = ''
SECRET_KEY = ")6p!>0t2r(<9L*:Y"
