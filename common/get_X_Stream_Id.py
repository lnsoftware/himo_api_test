import requests
import json

data = {
    'phone': 13676561839,
    'pass': 123456,
    "brand": "mainto_app",
    "temp_token": ""
}
url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/login/pass'


def get_x_stream_id(phone=13676561839, password=123456):
    url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/login/pass'
    data = {
        'phone': phone,
        'pass': password,
        'brand': 'mainto_app',
        'temp_token': ''
    }
    res = requests.get(url=url, params=data)
    res = res.headers
    return {'x-stream-id': res['X-Stream-Id']}


if __name__ == '__main__':
    res = requests.get(url=url, params=data)
    res = res.headers
    print(res)
    print({'x-stream-id': res['X-Stream-Id']})
