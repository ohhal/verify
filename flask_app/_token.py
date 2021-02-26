# -*- coding: utf-8 -*-
# @File: _token.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/27
# @Desc: 简单接口鉴权


import datetime
from functools import wraps

import jwt
from flask import jsonify, request
from config import SECRET_KEY


def check(username, password):
    return True


class Auth():
    @staticmethod
    def encode_auth_token(username, password):
        """
        生成认证Token
        :param username: 账号
        :param password: 密码
        :return: string
        """
        try:
            exp_time = 60 * 30  # token过期时间，半小时
            if check(username, password) is False:
                return jsonify(status=0, request='无效的账号')
            headers = {
                "typ": "JWT",
                "alg": "HS256",
            }
            payload = {
                "headers": headers,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=exp_time),
                'iat': datetime.datetime.utcnow(),
                'iss': 'djjlb',
                'data': {
                    'username': username,
                    'password': password,
                }
            }
            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jsonify(status=1, request=token)
        except Exception:
            return jsonify(status=0, request='生成token时遇到错误')

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithm='HS256', options={'verify_exp': True})
            if payload:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.DecodeError:
            return 'token认证失败'
        except jwt.InvalidTokenError:
            return '无效Token'


def AuthRequired(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header == 'root2021ubuntu':  # 测试toke
            return func(*args, **kwargs)
        if auth_header:
            payload = Auth().decode_auth_token(auth_header)
            if isinstance(payload, dict):
                username = payload['data']['username']
                password = payload['data']['password']
                if check(username, password) is True:
                    return func(*args, **kwargs)
                else:
                    return jsonify(status=0, request='认证失败')
            else:
                return jsonify(status=0, request=payload)
        else:
            return jsonify(status=0, request='认证失败')
    return decorated
