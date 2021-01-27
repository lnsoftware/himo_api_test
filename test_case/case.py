import requests
from common.get_X_Stream_Id import get_x_stream_id

# headers = get_x_stream_id(phone=17600203061,password=123456)
# 优惠券
headers = get_x_stream_id(phone=13676561839, password=123456)
i = ['C8E8QEDCA7', '85S2A84E86', '762CH77L35', 'QD2T67AGB6', '8ST8RBPRBC']
for preferentialCode in i:
    json = {
        'preferentialCode': preferentialCode
    }
    res = requests.post(url='https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/preferentialCard/bind/v1',
                        json=json, headers=headers)
    print(res.json())

# 产品卡
json = {
    'code': 'djZbYITrD'
}
res = requests.post(url='https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/bind/v1',
                    json=json, headers=headers)
print(res.json())

# 礼品卡
id = get_x_stream_id(phone=19111111111, password=123456)
json = {
    "code": "88P5EM26U8576M6"
}
res = requests.post(url='https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/giftCard/charge/v1',
                    headers=id, json=json)
print(res.json())
