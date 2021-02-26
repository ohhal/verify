# -*- coding: utf-8 -*-
# @File: _validator.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/26
# @Desc: 参数验证

from flask_app.validator import Required, Not, Blank, Equals, In, Url, Length, If, Then, validate


def check_params(args):
    '''参数验证'''
    rules = {
        "task_id": [Length(10, maximum=100)],  # 任务 task_id
        "googlekey": [Length(30, maximum=50)],  # recaptcha的key
        "pageurl": [Url()],  # recaptcha的网页地址
        "action": [],  # recaptcha的行为
        "body": [],  # 验证码图片的base64
        "methods": [Required, In(['img', 'recaptchaV2', 'recaptchaV3', 'recaptchaEnterprise']),
                    If(Equals('img'), Then({'body': Not(Blank())})),
                    If(Equals('recaptchaV2'), Then({'pageurl': Required, 'googlekey': Required})),
                    If(Equals('recaptchaV3'),
                       Then({'pageurl': Required, 'googlekey': Required, 'action': Not(Blank())})),
                    If(Equals('recaptchaEnterprise'),
                       Then({'pageurl': Required, 'googlekey': Required, 'action': Not(Blank())}))],  # 待验证码的种类
    }
    return validate(rules, args)
