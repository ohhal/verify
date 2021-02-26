# -*- coding: utf-8 -*-
# @File: _verify.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/26
# @Desc: 打码


import abc
import time

import requests
from retry import retry

from config import anti_key, confluence_key, Tcaptcha_key
from methods.errors import *

# 对应平台支持的识别方法
MethodEnum = dict(
    anti=['img', 'recaptchaV2', 'recaptchaV3', 'recaptchaEnterprise'],
    confluence=['img', 'recaptchaV2', 'recaptchaV3'],
    two_captcha=['img', 'recaptchaV2', 'recaptchaV3', 'recaptchaEnterprise']
)


class BaseVerify(object):
    '''打码基类'''

    def __init__(self, platform, params):
        self.platform = platform
        self.params = params
        self.msg = dict(
            code=-1,
            msg=None,
            text=None
        )
        self.overtime = 60 * 3

    def _platform(self):
        '''验证平台是否存在'''
        if self.platform not in MethodEnum.keys():
            self.msg['msg'] = f'Supported {self.platform}:{MethodEnum.keys()}'
            return False
        return True

    def _method(self):
        '''验证平台对应方法是否存在，对应平台入口函数是否存在'''
        self.verify_type = self.params['methods']
        self.entrance_platform = 'entrance_' + self.platform
        if self.verify_type not in MethodEnum[self.platform]:
            self.msg['msg'] = f'{self.platform} Supported methods:{MethodEnum[self.platform]}'
            return False
        if self.entrance_platform not in self.get_entrance_methods():
            self.msg['msg'] = f'There is no entry for the method supported by the {self.platform} '
            return False
        return True

    @retry(tries=2, delay=3)
    def anti(self, data):
        '''anti打码'''
        msg = requests.post('http://api.anti-captcha.com/createTask', json=data).json()
        start_time = 0
        if msg['errorId'] == 0:
            task_id = msg['taskId']
            while start_time <= self.overtime:
                try:
                    res = requests.post('https://api.anti-captcha.com/getTaskResult',
                                        json=dict(clientKey=anti_key, taskId=task_id)).json()
                    if res['status'] == 'processing':
                        time.sleep(2)
                        start_time += 2
                    else:
                        if res['errorId'] == 0:
                            self.msg['code'] = 0
                            try:
                                self.msg['text'] = res['solution']['text']
                            except Exception:
                                self.msg['text'] = res['solution']['gRecaptchaResponse']
                        else:
                            self.msg['msg'] = ErrorAnti(res['errorCode'])
                        break
                except:
                    time.sleep(2)
                    start_time += 60
        else:
            self.msg['msg'] = ErrorAnti(msg['errorCode'])

    @retry(tries=2, delay=3)
    def confluence(self, data):
        '''confluence打码'''
        msg = requests.post('https://api.capmonster.cloud/createTask', json=data).json()
        start_time = 0
        if msg['errorId'] == 0:
            task_id = msg['taskId']
            while start_time <= self.overtime:
                try:
                    res = requests.post('https://api.capmonster.cloud/getTaskResult',
                                        json=dict(clientKey=confluence_key, taskId=task_id)).json()
                    if res['status'] == 'processing':
                        time.sleep(2)
                        start_time += 2
                    else:
                        if res['errorId'] == 0:
                            self.msg['code'] = 0
                            try:
                                self.msg['text'] = res['solution']['text']
                            except Exception:
                                self.msg['text'] = res['solution']['gRecaptchaResponse']
                        else:
                            self.msg['msg'] = ErrorConfluence(res['errorCode'])
                        break
                except:
                    time.sleep(2)
                    start_time += 60
        else:
            self.msg['msg'] = ErrorConfluence(msg['errorCode'])

    @retry(tries=2, delay=3)
    def two_captcha(self, data):
        '''two_captcha打码'''
        res_id = requests.post('https://2captcha.com/in.php', data=data).json()
        if res_id.get('status') == 1:
            get_id = res_id.get('request')
            start_time = time.time()
            while True:
                data_id = {
                    'key': Tcaptcha_key,
                    'action': 'get',
                    'json': '1',
                    'id': get_id
                }
                try:
                    res_json = requests.get(
                        f'https://2captcha.com/res.php', params=data_id).json()
                    status = res_json.get("status")
                    if status == 0:
                        if "NOT_READY" in status.get("request"):
                            time.sleep(5)
                            continue
                        else:
                            self.msg['msg'] = 'Recaptcha Token无法处理:{}'.format(Error2Captcha(res_json.get('request')))
                            break
                    elif status == 1:  # 成功
                        self.msg['code'] = 0
                        self.msg['text'] = res_json.get("request")
                        break
                    else:
                        self.msg['msg'] = Error2Captcha(res_json.get('request'))
                    if time.time() - start_time > self.overtime:
                        self.msg['msg'] = f'获取识别结果超时,id为{get_id},当前最大等待时长{self.overtime}s'
                        break
                except Exception:
                    time.sleep(2)
                    start_time += 60
        else:
            self.msg['msg'] = Error2Captcha(res_id.get('request'))

    @abc.abstractmethod
    def entrance_anti(self):
        pass

    @abc.abstractmethod
    def entrance_confluence(self):
        pass

    @abc.abstractmethod
    def entrance_two_captcha(self):
        pass

    def get_entrance_methods(self):
        '''获取当前类的entrance_函数'''
        return filter(lambda x: x.startswith('entrance_') and callable(getattr(self, x)), dir(self))

    def solver(self):
        '''解决验证码'''
        if self._platform() is False or self._method() is False:
            return self.msg
        try:
            data = getattr(self, self.entrance_platform)()
            getattr(self, self.platform)(data)
        except Exception as e:
            self.msg['msg'] = f'验证码识别失败：{str(e.args)}'
        finally:
            return self.msg


class Verify(BaseVerify):
    '''打码预设参数'''

    def __init__(self, platform, params):
        super().__init__(platform, params)

    def entrance_anti(self):
        '''anti打码 预设参数 https://anticaptcha.atlassian.net/wiki/spaces/API/pages'''
        data = dict(
            clientKey=anti_key,
            task=dict()
        )
        if self.verify_type == 'img':
            base64_img = self.params['body']
            data['task'] = {
                "type": "ImageToTextTask",
                "body": base64_img,
                "phrase": False,
                "case": False,
                "numeric": 0,
                "math": False,
                "minLength": 0,
                "maxLength": 0
            }
        else:
            key = self.params['googlekey']
            url = self.params['pageurl']
            if self.verify_type == 'recaptchaV2':
                data['task'] = {
                    "type": "RecaptchaV2TaskProxyless",
                    "websiteURL": url,
                    "websiteKey": key,
                }
            elif self.verify_type == 'recaptchaV3':
                action = self.params['action']
                data['task'] = {
                    "type": "RecaptchaV3TaskProxyless",
                    "websiteURL": url,
                    "websiteKey": key,
                    "minScore": 0.3,
                    "pageAction": action,
                    "isEnterprise": False
                }
            elif self.verify_type == 'recaptchaEnterprise':
                action = self.params['action']
                data['task'] = {
                    "type": "RecaptchaV3TaskProxyless",
                    "websiteURL": url,
                    "websiteKey": key,
                    "minScore": 0.7,
                    "pageAction": action,
                    "isEnterprise": True
                }
            else:
                raise Exception(f'{self.platform}没有该方法:{self.verify_type}')
        return data

    def entrance_confluence(self):
        '''confluence打码 预设参数 https://zennolab.atlassian.net/wiki/spaces/APIS/pages'''
        data = dict(
            clientKey=confluence_key,
            task=dict()
        )
        if self.verify_type == 'img':
            base64_img = self.params['body']
            data['task'] = dict(
                type='ImageToTextTask',
                body=base64_img,
            )
        else:
            key = self.params['googlekey']
            url = self.params['pageurl']
            if self.verify_type == 'recaptchaV2':
                data['task'] = dict(
                    type='NoCaptchaTaskProxyless',
                    websiteURL=url,
                    websiteKey=key,
                )
            elif self.verify_type == 'recaptchaV3':
                action = self.params['action']
                data['task'] = dict(
                    type='RecaptchaV3TaskProxyless',
                    websiteURL=url,
                    websiteKey=key,
                    minScore=0.3,
                    pageAction=action
                )
            else:
                raise Exception(f'{self.platform}没有该方法:{self.verify_type}')
        return data

    def entrance_two_captcha(self):
        '''two_captcha打码 预设参数 https://2captcha.com/2captcha-api'''
        if self.verify_type == 'img':
            base64_img = self.params['body']
            data = dict(method='base64', key=Tcaptcha_key, body=base64_img, json='1')
        else:
            key = self.params['googlekey']
            url = self.params['pageurl']
            if self.verify_type == 'recaptchaV2':
                data = dict(
                    googlekey=key,
                    pageurl=url,
                    key=Tcaptcha_key,
                    method='userrecaptcha',
                    json='1'
                )
            elif self.verify_type == 'recaptchaV3':
                action = self.params['action']
                data = dict(
                    googlekey=key,
                    pageurl=url,
                    version='v3',
                    action=action,
                    key=Tcaptcha_key,
                    method='userrecaptcha',
                    json='1'
                )
            elif self.verify_type == 'recaptchaEnterprise':
                action = self.params['action']
                data = dict(
                    method='userrecaptcha',
                    googlekey=key,
                    pageurl=url,
                    version='enterprise',
                    action=action,
                    min_score='0.3',
                    key=Tcaptcha_key,
                    json='1'
                )
            else:
                raise Exception(f'{self.platform}没有该方法:{self.verify_type}')
        return data


def solver(platform, params):
    return Verify(platform, params).solver()


if __name__ == '__main__':
    import base64

    with open(r"C:\Users\404\Desktop\get_cookie\login_tools\google_img\1606873379_sesserynab.png", 'rb') as f:
        body = base64.b64encode(f.read())
        # test_flask_img(body)
        data = dict(
            # task_id='93d15904-085b-487d-a77d-530b564e17a0',
            # googlekey="6LdLK0EUAAAAAOW4sWFiUm0FspjiEjX0pfhojEBt",
            # pageurl="https://www.discuss.com.hk/register.php",
            # action='',
            body=body,
            methods='img'
        )

        a = solver('two_captcha', data)
        print(a)
