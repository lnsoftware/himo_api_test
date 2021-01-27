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
@allure.severity('blocker')
class Test_userInfo:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup_class(self):
        # 获取用户信息
        self.userInfo = c.release + c.userInfo

    @allure.story('获取用户信息')
    @allure.title('正常获取用户信息')
    def test_getUserInfo(self):
        res = http_get(url=self.userInfo)
        balance = str(get_user_gift_card_balance())
        logger.info('正常获取用户信息')
        try:
            assert res['msg']['gift_card_money'] == balance
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户信息')
    @allure.title('不传x-stream-id获取用户信息')
    def test_getUserInfo_noXSId(self):
        logger.info('不传x-stream-id获取用户信息')
        res = http_get_noToken(url=self.userInfo, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError
