from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure, pytest
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
@allure.story('获得套餐推荐')
@allure.severity('normal')
class Test_getHotProduct:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """
    def setup(self):
        self.url = c.release + c.hotProducts
        self.params = {"rootNodeId": 5442, "storeId": 1019, "type": "blue"}

    @title("获得套餐推荐")
    def test_get_hot_product(self):
        logger.info(f'获得套餐推荐,Params:{self.params}')
        res = http_get(self.url, params=self.params)
        if check_result_is_true(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('无x-stream-id获取套餐推荐')
    def test_get_hot_product_not_x_stream_id(self):
        logger.info(f'无x-stream-id获取套餐推荐,params:{self.params}')
        res = http_get_noToken(self.url, params=self.params)
        if check_result_is_true(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('storeid为空获取套餐推荐')
    def test_get_hot_product_not_store_id(self):
        params = self.params
        params['storeId'] = None
        logger.info(f'storeid为空获取套餐推荐,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('rootNodeId为空获取套餐推荐')
    def test_get_hot_product_not_root_node_id(self):
        params = self.params
        params['rootNodeId'] = None
        logger.info(f'rootNodeId为空获取套餐推荐,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('type为空获取套餐推荐')
    def test_get_hot_product_not_type(self):
        params = self.params
        params['type'] = None
        logger.info(f'type为空获取套餐推荐,params{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @pytest.mark.skip('接口暂时没做限制')
    @title('使用不存在的storeId获取套餐推荐')
    def test_get_hot_product_error_storeId(self):
        params = self.params
        params['storeId'] = 0
        logger.info(f'使用不存在的storeId获取套餐推荐, params:{params}')
        res = http_get_noToken(self.url, params=params)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @pytest.mark.skip('接口暂时没做限制')
    @title("使用不存在的type获取套餐推荐")
    def test_get_hot_product_error_type(self):
        params = self.params
        params['type'] = 0
        logger.info(f'使用不存在的type获取套餐推荐, params:{params}')
        res = http_get_noToken(self.url, params=params)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @pytest.mark.skip('接口暂时没做限制')
    @title('使用不存在的rootNodeId获取套餐推荐')
    def test_get_hot_product_error_root_node_id(self):
        params = self.params
        params['rootNodeId'] = 0
        logger.info(f'使用不存在的rootNodeId获取套餐推荐, params:{params}')
        res = http_get_noToken(self.url, params=params)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

