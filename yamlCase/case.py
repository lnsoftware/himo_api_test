from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure

'''
测试用例模板
'''

caseName, casedata = GettingDate('登录.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('', FileLevel=logging.ERROR).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名

for i in range(1):
    url = casedata[i]['url']
    phone = casedata[i]['phone']
    password = casedata[i]['pass']
    brand = casedata[i]['brand']
    temp_token = casedata[i]['temp_token']
    result = casedata[i]['assert']
    nowCaseName = caseName[i]
    params = {
        'phone': phone,
        'pass': password,
        'brand': brand,
        'temp_token':temp_token
    }
    import requests
    res = requests.get(url=url,params=params)
    print(len(res.headers['x-stream-id']))
    res = res.json()
    print(res)
    print(res['success'])
    print(result)
    if result == 1:
        assert result == res['success']
        print('assert successs')
