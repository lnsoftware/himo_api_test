import requests
from common.queries import *
from common.get_X_Stream_Id import get_x_stream_id
headers = get_x_stream_id()
url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/getTokenFromApp'
params = {"deviceToken":get_userDevices()}
res = requests.get(url=url,headers=headers,params=params)
res = res.json()
print(res)

url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/login/token'
params = {'token':res['msg'],'brand':'mantu_app'}
# params = {'brand':'mantu_app'}
res = requests.get(url=url,params = params)
res = res.json()
print(res)
# assert 'validation.required' in str(res['error_msg'])