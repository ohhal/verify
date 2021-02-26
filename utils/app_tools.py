# -*- coding: utf-8 -*-
# @File: app_tools.py
# @Author: 张爱灵
# @Date: 2021/01/26
# @Desc: flask 中的工具类

import requests
from retry import retry

from config import anti_key, confluence_key, Tcaptcha_key
from verify_sql.platform_sql import select

platformEnum = {
    '1': ['anti'],
    '2': ['confluence'],
    '3': ['two_captcha'],
    '4': ['anti', 'confluence'],
    '5': ['anti', 'two_captcha'],
    '6': ['confluence', 'two_captcha'],
    '7': ['anti', 'confluence', 'two_captcha']
}


def get_tibe_key(result_task):
    platforms = list()
    for task in result_task:
        platforms.append(task['platform'])
    return getkey(platforms)


def getkey(x):
    for (key_str, value) in platformEnum.items():  # 根据x查找所对应的key value值
        if x == value:
            return key_str


def get_platform():
    '''获取当前平台'''
    msg = select()
    if msg['code'] == 0:
        platform = msg['msg']
    else:
        platform = ''
    return platform


@retry(tries=3, delay=2)
def get_balance():
    '''获取平台余额'''
    res = dict(
        anti=-1,
        confluence=-1,
        twocaptcha=-1
    )
    d = dict(
        clientKey=confluence_key
    )
    d2 = dict(
        clientKey=anti_key
    )
    r = requests.post('https://api.capmonster.cloud/getBalance', json=d).json()
    if r['errorId'] == 0:
        res['confluence'] = float(r['balance'])
    r1 = requests.get(f'https://2captcha.com/res.php?key={Tcaptcha_key}&action=getbalance&json=1').json()
    if r1()['status'] == 1:
        res['twocaptcha'] = float(r1['request'])
    r2 = requests.get('https://api.anti-captcha.com/getBalance', json=d2).json()
    if r2['errorId'] == 0:
        res['anti'] = float(r2['balance'])
    return res


if __name__ == '__main__':
    print(get_balance())
