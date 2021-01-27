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
@allure.story('用户意见反馈')
@allure.severity('blocker')
class Test_feedBack:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.feedback

    @allure.title('用户反馈信息为空')
    def test_user_feed_back_is_none(self):
        data = {'content': None}
        logger.info(f'用户反馈信息为空,data:{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result(res['error_code'], 422, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('用户反馈信息字数破千')
    def test_user_feed_back_loog(self):
        data = {'content':str([x for x in range(1000)])}
        logger.info(f'用户反馈信息字数长度超过100,data:{data}')
        res = http_post(self.url, json=data)
        if check_result(res['msg'], 1, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带x-stream-id反馈信息')
    def test_user_feed_back_no_x_stream_id(self):
        logger.info('不带x-stream-id反馈信息')
        res = http_post_noToken(self.url, result=0)
        if check_result(res['error_code'], 401, logger) == 0:
            raise AssertionError(traceback.format_exc())
