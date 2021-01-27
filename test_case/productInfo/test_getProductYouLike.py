from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure
from allure import title
from common.queries import *
from conf import Api_Url as c
from httpRequests._requests import *

"""
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
"""

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('商品信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('商品信息')
@allure.story('猜你喜欢')
@allure.severity('normal')
class Test_getProductYouLike:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.youLike

    @title('获得蓝标店猜你喜欢产品')
    def test_get_product_you_like_blue(self):
        data = {'brand': 'blue'}
        logger.info(f'获得蓝标点猜你喜欢产品,data{data}')
        res = http_post(self.url, json=data)
        if check_result_is_true(res['msg']['data'], logger) == 0:
            raise AssertionError(traceback.format_exc())
        import requests
        for i in range(len(res['msg']['data'])):
            response = requests.get(url=res['msg']['data'][i]['img_path'])
            if check_result(response.status_code, 200, logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('获得大师店猜你喜欢产品')
    def test_get_product_you_like_gold(self):
        data = {'brand': 'gold'}
        logger.info(f'获得大师店猜你喜欢产品,data{data}')
        res = http_post(self.url, json=data)
        if check_result_is_true(res['msg']['data'], logger) == 0:
            raise AssertionError(traceback.format_exc())
        import requests
        for i in range(len(res['msg']['data'])):
            response = requests.get(url=res['msg']['data'][i]['img_path'])
            if check_result(response.status_code, 200, logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('传递不存在的brand获取猜你喜欢')
    def test_get_product_you_like_error_brand(self):
        data = {"brand":'dasdas'}
        logger.info(f'传递不存在的brand获取猜你喜欢,data{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())