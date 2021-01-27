from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure
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
@allure.story('修改密码')
@allure.severity('blocker')
class Test_changPassword:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.changeUserPassword

    @allure.title('修改密码为5位数')
    def test_change_password_five(self):
        data = {'password': '123456', 'passwordNew': '12345'}
        logger.info(f'修改密码为5位数,{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result(res['error_code'], 422, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('修改密码输入错误的原密码')
    def test_change_password_use_error_old_password(self):
        data = {'password': '1234566789', "passwordNew": "123456"}
        logger.info(f'修改密码输入错误的原密码，{data}')
        res = http_post(self.url, json=data, result=0)
        result = 'old password error'
        if check_result(res['error_msg'], result, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('原密码为空修改密码')
    def test_change_password_none_password(self):
        data = {"passwordNew": "123456"}
        logger.info(f'原密码为空修改密码,{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result(res['error_code'], 422, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('修改密码为原密码')
    def test_change_password_the_same_as_old_password(self):
        data = {'password': "123456", "passwordNew": "123456"}
        logger.info(f'修改密码为原密码{data}')
        res = http_post(self.url, json=data)
        if check_result(res['msg'], 1, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('使用int类型参数修改密码')
    def test_change_password_use_int(self):
        data = {'password': 123456, "passwordNew": 123456}
        logger.info(f'使用int类型参数修改密码,{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result(res['error_code'], 422, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('使用float类型参数修改密码')
    def test_change_password_use_float(self):
        data = {'password': 123.123, "passwordNew": 123.321}
        logger.info(f'使用float类型参数修改密码,{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result(res['error_code'], 422, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带x-stream-id修改密码')
    def test_change_password_no_x_stream_id(self):
        logger.info('不带x-stream-id修改密码')
        res = http_post_noToken(self.url, result=0)
        if check_result(res['error_code'], 401, logger) == 0:
            raise AssertionError(traceback.format_exc())
