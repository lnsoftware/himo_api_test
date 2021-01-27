from common.readYaml import GettingDate
from common.logger import Logger
from common.get_X_Stream_Id import get_x_stream_id
import traceback
import logging
import allure
import requests

'''
测试用例模板
'''

caseName, casedata = GettingDate('createOrder.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('创建订单', FileLevel=logging.ERROR).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('创建订单')
def test_create_order():
    for i in range(0,len(caseName)):
        url = casedata[i]['url']
        data = casedata[i]['data']
        result = casedata[i]['assert']
        try:
            headers = get_x_stream_id()
        except:
            logger.error('获取x-stream-id失败')
            logger.error(traceback.format_exc())
            raise Exception
        logger.info('x-stream-id为：',id)
        res = requests.post(url=url,json=data,headers=headers)
        # assert res.status_code == 200 ,'访问失败:%s'% traceback.format_exc()
        logger.info('访问成功')
        res = res.json()
        try:
            assert res['success'] == result
            logger.info('用例|%s|通过',caseName[i])
        except:
            logger.error('用例|%s|失败',caseName[i])
            logger.error(res)
            logger.error(traceback.format_exc())
            raise Exception

