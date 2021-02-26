import time

import requests

Url = 'http://127.0.0.1:9999'
header = {'Authorization': 'root2021ubuntu'}


def test_add(body=None):
    if body:
        data = dict(
            task_id='54we5904-asdsa085b-487d-a7we-530bweee17a0sad884a',
            # googlekey="",
            # pageurl="",
            action='',
            body=body,
            methods='img'
        )
    else:
        data = dict(
            task_id='54we5904-asdsa085b-487d-a7we-530bweee17a0sad884a',
            googlekey="6LdLK0EUAAAAAOW4sWFiUm0FspjiEjX0pfhojEBt",
            pageurl="https://www.discuss.com.hk/register.php",
            action='',
            body='',
            methods='recaptchaV2'
        )
    res = requests.get(f'{Url}/verify/create', params=data, headers=header).json()
    return res


def test_result(id):
    data = dict(
        id=id
    )
    res = requests.get(f'{Url}/verify/result', params=data, headers=header).json()
    print(res)
    return res


def test_paltform():
    d = dict(
        platform='anti'
    )
    s = requests.post(f'{Url}/verify/platform', json=d)
    print(s.json())


def test_flask_recaptcha():
    r1 = test_add()
    rid = r1.get('request')
    print(rid)
    for i in range(30):
        r2 = test_result(rid)
        if r2.get("status") == 1:
            print("验证码获取成功，正在提交。")
            form_tokon = r2.get("request")
            print(r2)
            break
        if r2.get("request") == 'CAPCHA_NOT_READY':
            print("验证码尚未返回，请等待。")
            time.sleep(5)
        else:
            print("验证码获取失败，请重启。")
            print(r2)
            break


def test_flask_img(body):
    r1 = test_add(body)
    rid = r1.get('request')
    print(rid)
    for i in range(30):
        r2 = test_result(rid)
        if r2.get("status") == 1:
            print("验证码获取成功，正在提交。")
            form_tokon = r2.get("request")
            print(r2)
            break
        if r2.get("request") == 'CAPCHA_NOT_READY':
            print("验证码尚未返回，请等待。")
            time.sleep(5)
        else:
            print("验证码获取失败，请重启。")
            print(r2)
            break


def test_token():
    data = dict(
        username='asdasd',
        password='asdwdda'
    )
    r = requests.get(f'{Url}/verify/token/create', params=data).json()
    return r['request']


def test_token_v():
    # token = test_token()
    # print(token)
    # time.sleep(3)
    token = 'root'
    header = {
        'Authorization': token
    }
    s = requests.get(f'{Url}/verify/test', headers=header).json()
    print(s)


if __name__ == '__main__':
    # import base64
    # with open(r"C:\Users\404\Desktop\get_cookie\login_tools\google_img\1606873379_sesserynab.png",'rb') as f:
    #     body = base64.b64encode(f.read())
    #     test_flask_img(body)
    test_flask_recaptcha()
    # test_result('MbF5NflSZd7VWD2jhcc0ZmAITucCRQVvky3/mmwanh+DMFto5WN0JnCU9ro61RApYloklQ9NsVUHfA7+R+kpamBqpVisBPtx3w5EDwH79Qg=')
    # test_token()
    # test_token_v()
