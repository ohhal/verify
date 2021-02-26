# -*- coding: utf-8 -*-
# @File: _aes.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/28
# @Desc: AES加密解密

import base64
import re

from Crypto.Cipher import AES


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


class AESCBC:
    '''AES加密解密'''
    key = 'DLxVsTyt~eJk/P#B'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = key

    # 加密函数
    def encrypt(self, text):
        text = add_to_16(text)
        cryptos = AES.new(self.key, self.mode, self.iv)
        cipher_text = cryptos.encrypt(text)
        encData = str(base64.b64encode(cipher_text), encoding='utf-8')
        return encData

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        text = base64.b64decode(text)
        cryptos = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptos.decrypt(text)
        decData = bytes.decode(plain_text)
        decData = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', decData)
        return decData


if __name__ == '__main__':
    # 加密解密
    e = AESCBC().encrypt("f32a7d01-8c1f-46e6-be5e-238f6314c4a5,3")  # 加密
    d = AESCBC().decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)
