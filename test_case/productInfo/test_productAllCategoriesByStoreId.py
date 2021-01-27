from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure
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
@allure.story('通过门店id获得所有类目信息')
@allure.severity('blocker')
class Test_getAllCategoriesByStoreId:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.allCategoriesByStoreId

    @allure.title('获取1001门店所有类目信息')
    def test_get_store_all_categories_by_store_id(self):
        params = {"storeId": 1001}
        logger.info(f'获取1001门店所有类目信息,params:{params}')
        res = http_get(self.url, params=params)
        if check_result_is_true(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('获取多门店类目信息')
    def test_get_store_all_categories_by_stores(self):
        params = {"sotreId": [1001, 1002]}
        logger.info(f'获取多门店类目信息,params{params}')
        res = http_get(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('传空值获取类目信息')
    def test_get_store_all_categories_by_error_store_id(self):
        params = {"storeId": None}
        logger.info(f'传空值获取类目信息,params:{params}')
        res = http_get(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带参数获取类目信息')
    def test_get_store_all_categories_have_not_params(self):
        logger.info('不带参数获取类目信息')
        res = http_get(self.url, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带x-stream-id获取类目信息')
    def test_get_store_all_categories_not_x_stream_id(self):
        params = {"storeId": 1001}
        logger.info(f'不带x-stream-id获取类目信息,params:{params}')
        res = http_get(self.url, params=params)
        if check_result_is_true(res, logger) == 0:
            raise AssertionError(traceback.format_exc())