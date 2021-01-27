from common.readYaml import GettingDate
from common.assert_result import check_result
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
@allure.story('获得会员卡列表权益')
@allure.severity('normal')
class Test_userWalfareList:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup(self):
        self.url = c.release + c.userWalfare

    @allure.title('获取会员卡列表权益')
    def test_get_user_walfare_list(self):
        logger.info('获取会员卡列表权益')
        res = http_get(self.url)
        if check_result(data=len(res['msg']['data']), result=7, logger=logger) == 0:
            raise AssertionError(f'返回信息：{res}', traceback.format_exc())

    @allure.title('不带x-stream-id获取会员卡列表权益')
    def test_get_user_walfrae_list_no_x_stream_id(self):
        logger.info('不带x-stream-id获取会员卡列表权益')
        res = http_get_noToken(self.url)
        if check_result(data=len(res['msg']['data']), result=7, logger=logger) == 0:
            raise AssertionError(f'返回信息：{res}', traceback.format_exc())
