# -*- coding: utf-8 -*-
# @File: verify_app.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/26
# @Desc: flask接口

import uuid

from flask import Flask, request, jsonify

from Celery import verify_celery_app
from flask_app._aes import AESCBC
from flask_app._token import Auth, AuthRequired
from flask_app._validator import check_params
from methods._verify import MethodEnum
from utils.app_tools import get_balance, get_platform, getkey, get_tibe_key, platformEnum
from utils.log_tools import VerifyLogger as logger
from verify_sql.platform_sql import modify
from verify_sql.task_sql import insert_task, select_task
from verify_sql.log_sql import logsql, select_log, select_log_id
import json

app = Flask(__name__)


@app.route('/verify/create', methods=['GET', 'POST'])
@AuthRequired
def creat_task():
    '''创建打码任务'''
    if request.method == 'POST':
        _args = request.get_json()
    else:
        _args = request.args
    # 参数验证
    flag = check_params(_args)
    if flag.valid is False:
        logger.error(str(flag.errors))
        return jsonify(status=0, request=str(flag.errors))
    param = _args
    # 无task_id时创建task_id
    task_id: str = str(uuid.uuid4())
    if 'task_id' not in param.keys():
        enter_task_id = ''
    else:
        enter_task_id = param['task_id']
    ped_key = ''
    logsql(task_id, '/verify/create/', f'传入参数：[{json.dumps(dict(param))}]')
    # 如果存在web_key 先查询库中是否有待识别
    if 'googlekey' in param.keys() and 'recaptcha' in param['methods']:
        ped_key = param['googlekey']
        app_task_id = select_task(ped_key)
        if isinstance(app_task_id, str):
            app_task_id = AESCBC().encrypt(app_task_id)  # 本次任务返回的task_id
            logsql(task_id, '/verify/create/', f'success:取待识别区域的task_id')
            logger.info(f'[/verify/create/{app_task_id}][param:{param}]: sql success')
            return jsonify(status=1, request=app_task_id)
    if param['methods'] == 'img':  # img 应该为单平台识别
        platforms = [get_platform()]
    else:
        platforms: list = MethodEnum.keys()
    task_platform = list()
    # 根据平台创建任务
    for platform in platforms:
        platform_task_id = task_id + platform  # 与get_state中的get_task_id相同
        try:
            verify_celery_app.send_task(name='task.add_task', args=[platform, param], task_id=platform_task_id)
            logsql(task_id, '/verify/create/', f'任务创建成功:任务id：[{platform_task_id}] 传入id：{enter_task_id}')
            logger.info(f'success:[/verify/create/{platform_task_id}][enter_task_id:{enter_task_id}]')
            task_platform.append(platform)
        except Exception as e:
            logsql(task_id, '/verify/create/', f'任务创建失败:任务id：[{platform_task_id}] 传入id：{enter_task_id} 失败详情:{e}')
            logger.warn(f'failure:[/verify/create/{platform_task_id}][enter_task_id:{enter_task_id}] 失败详情:{e}')
    if len(task_platform) == 0:
        logsql(task_id, '/verify/create/', 'failure:创建解决验证码任务时异常，任务创建失败')
        logger.error(f'[/verify/create/{task_id}]: failure:创建解决验证码任务时异常，任务创建失败')
        return jsonify(status=0, request='创建解决验证码任务时异常，任务创建失败')
    task_platform_id = getkey(task_platform)
    app_task_id = f"{task_id};{task_platform_id};{ped_key}"
    app_task_id = AESCBC().encrypt(app_task_id)  # 本次任务返回的task_id
    logsql(task_id, '/verify/create/', f'success:返回id:{app_task_id}')
    logger.info(f'success:[/verify/create/{app_task_id}]')
    return jsonify(status=1, request=app_task_id)


@app.route('/verify/result', methods=['GET', 'POST'])
@AuthRequired
def get_state():
    '''根据任务id获取打码任务结果'''
    if request.method == 'POST':
        _args = request.get_json()
    else:
        _args = request.args
    if 'id' not in list(_args.keys()):
        logger.error('您提供的关键参数值格式错误: id 字段缺失')
        return jsonify(status=0, request='您提供的关键参数值格式错误: id 字段缺失')
    if _args['id'] == '':
        logger.error('您提供的关键参数值格式错误: id 字段不能为空')
        return jsonify(status=0, request='您提供的关键参数值格式错误: id 字段不能为空')
    _id = _args['id']
    # 将task_id进行解密
    try:
        app_task_data = AESCBC().decrypt(_id)  # 本次任务返回的task_id
        task_id, platform_id, ped_key = app_task_data.split(';')
        platforms = platformEnum[platform_id]
    except Exception:
        logger.warn(f'{_id}:您提供的关键参数值格式错误: 请检查是否id字段是否有效')
        return jsonify(status=0, request='您提供的关键参数值格式错误: 请检查是否id字段是否有效')
    logsql(task_id, '/verify/result/', f'传入参数：[{_id}]: ')
    result_tasks = list()
    # 开始查看任务结果
    for platform in platforms:
        get_task_id = task_id + platform  # 与creat_task中的platform_task_id相同
        result_task = dict(
            platform=platform,
            task_id=get_task_id,
            status=0,
            request=None
        )
        try:
            async_result = verify_celery_app.AsyncResult(get_task_id)
            if async_result.state == 'PENDING':
                result_task['status'] = 0
                result_task['request'] = 'CAPCHA_NOT_READY'
            elif async_result.state == 'FAILURE':  # 失败 failure
                result_task['status'] = 0
                result_task['request'] = '解决验证码任务执行时异常'
            else:
                res = async_result.result
                if res['code'] == 0:  # 成功
                    result_task['status'] = 1
                    result_task['request'] = res['text']
                else:
                    result_task['status'] = 0
                    result_task['request'] = res['msg']
        except Exception as e:
            result_task['status'] = 0
            result_task['request'] = f'解决验证码任务获取结果时发生异常:{e}'
        finally:
            result_tasks.append(result_task)
    # 只要有任务完成直接返回将剩余任务放置到待识别数据库
    for result_task in result_tasks:
        if result_task['status'] == 1:
            if ped_key != '':  # googlekey存在，则将其他平台任务加入到待识别区域，设置超时
                result_tasks.remove(result_task)
                task_platform_id = get_tibe_key(result_tasks)
                app_task_id = f"{task_id};{task_platform_id};"
                insert_task(app_task_id, ped_key)
                logger.info(f'[{app_task_id};{ped_key}]进入等待区')
            logsql(task_id, '/verify/result', f'success:成功返回结果:{json.dumps(result_task)}')
            logger.info(f'[/verify/result{app_task_data}][task_id:{task_id}]: success[result:{result_task}]')
            return jsonify(status=1, request=result_task['request'])
    # 全部等待或者部分等待没有成功直接返回等待
    for result_task in result_tasks:
        if result_task['request'] == 'CAPCHA_NOT_READY':
            logsql(task_id, '/verify/result', f'notReady:[CAPCHA_NOT_READY]')
            logger.info(f'[/verify/result{app_task_data}]: CAPCHA_NOT_READY')
            return jsonify(status=0, request='CAPCHA_NOT_READY')
    # 全部失败返回全部失败的结果
    errormsg = ';'.join([result_task['request'] for result_task in result_tasks])
    logsql(task_id, '/verify/result', f'failure:[{errormsg}]')
    logger.info(f'failure:[/verify/result{app_task_data}]')
    return jsonify(status=0, request=errormsg)


@app.route('/verify/platform', methods=['POST'])
@AuthRequired
def set_platform():
    '''设置打码所在的平台'''
    params = request.get_json()
    platform = params['platform']
    logger.info(f'/task/platform platform:{platform}')
    msg = modify(platform)
    if msg['code'] == 0:
        logger.info(f'/verify/platform/ platform:{platform} success')
        return jsonify(status=1, request=f'切换{platform}成功')
    else:
        logger.error(f'/verify/platform/ platform:{platform} failure')
        return jsonify(status=0, request=f'切换{platform}失败')


@app.route('/verify/balance')
def platform_balance():
    '''获取打码平台的费用信息'''
    try:
        return jsonify(status=1, request=get_balance())
    except Exception:
        return jsonify(status=0, request='获取平台余额失败')


@app.route('/verify/log', methods=['GET', 'POST'])
def show_log():
    if request.method == 'POST':
        _args = request.get_json()
    else:
        _args = request.args
    search = None
    date = None
    type = None
    if 'search' in _args.keys():
        search = _args['search']
        type = 'search'
    if 'id' in _args.keys():
        search = _args['id']
        type = 'id'
    if 'date' in _args.keys():
        date = _args['date']
    result = select_log(timestamp=date, search=search, type=type)
    return jsonify(result)


@app.route('/verify/log/serach', methods=['GET', 'POST'])
def show_log_id():
    if request.method == 'POST':
        _args = request.get_json()
    else:
        _args = request.args
    search = None
    date = None
    type = None
    if 'search' in _args.keys():
        search = _args['search']
        type = 'search'
    if 'id' in _args.keys():
        search = _args['id']
        type = 'id'
    if 'date' in _args.keys():
        date = _args['date']
    result = select_log_id(timestamp=date, search=search, type=type)
    return jsonify(result)


@app.route('/verify/token/create', methods=['GET', 'POST'])
def create_token():
    '''生成认证Token'''
    if request.method == 'POST':
        _args = request.get_json()
    else:
        _args = request.args
    try:
        username = _args['username']
        password = _args['password']
    except Exception:
        logger.warn('[/verify/token/create]异常的参数')
        return jsonify(status=0, request='异常的参数')
    res = Auth().encode_auth_token(username, password)
    logger.info(f'[/verify/token/create]{res}')
    return res


@app.route('/verify/test')
@AuthRequired
def test_api():
    return jsonify(code=1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=False)
