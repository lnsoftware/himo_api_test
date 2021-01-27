from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
from common.queries import *
from conf import Api_Url as c
from httpRequests._requests import *

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('用户信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('用户信息')
@allure.story('记录预约协议版本')
@allure.severity('normal')
class Test_protocolVersion:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup(self):
        self.url = c.release + c.protocolVersion

    @allure.title("获取版本为0的协议")
    def test_get_protocol_version_zero(self):
        data = {"protocolVersion": 0}
        logger.info(f'获取版本为0的协议，{data}')
        res = http_post(url=self.url, json=data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())

    @allure.title("不带x-stream-id获取协议")
    def test_get_protocol_version_no_x_stream_id(self):
        logger.info('不带x-stream-id获取协议')
        res = http_post_noToken(url=self.url, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())

    @allure.title('获取含有小数的协议版本')
    def test_get_protocol_version_data_is_decimal(self):
        data = {'protocolVersion': 0.01}
        logger.info(f'获取含有小数的协议版本,{data}')
        res = http_post(url=self.url, json=data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())

    @allure.title('获取版本为负数的协议')
    def test_get_protocol_version_data_is_negative(self):
        data = {'protocolVersion': -1}
        logger.info(f'获取版本为负数的协议,{data}')
        res = http_post(url=self.url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())

    @allure.title('传递字符串获取版本协议')
    def test_get_protocol_version_data_is_string(self):
        data = {"protocolVersion": 'asdsad'}
        logger.info(f'传递字符串获取版本协议,{data}')
        res = http_post(url=self.url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())

    @allure.title('不传递参数获取协议版本')
    def test_get_protocol_version_data_no_data(self):
        logger.info('不传递参数获取协议版本')
        res = http_post(url=self.url, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except AssertionError:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError(traceback.format_exc())
