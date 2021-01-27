from common.readYaml import GettingDate
from common.assert_result import *
from allure import title
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
@allure.story('通过门店和类目id获得商品信息')
@allure.severity('blocker')
class Test_getProductCategoryByStoreIdAndCatId:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.productCategoryByStoreIdAndCatId
        self.params = {"storeId": 1001, "categoryId": 5498}

    @title('获取某个门店下的某个类目的商品信息')
    def test_get_product_category_by_store_id_and_cat_id(self):
        logger.info(f'获取某个门店下的某个类目的商品信息,params:{self.params}')
        res = http_get(self.url, params=self.params, result=0)
        category = get_product_category_by_store_id_and_cat_id(self.params['categoryId'])
        try:
            res = len(res['msg']['children'])
            if check_result(res, len(category), logger) == 0:
                raise AssertionError(traceback.format_exc())
        except:
            if check_result_is_500(res, logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title("不带x-stream-id获取某个门店下的某个类目的商品信息")
    def test_get_product_category_by_store_id_and_cat_id_not_x_stream_id(self):
        logger.info(f'不带x-stream-id获取某个门店下的某个类目的商品信息,params:{(self.params)}')
        res = http_get_noToken(self.url, params=self.params, result=0)
        category = get_product_category_by_store_id_and_cat_id(self.params['categoryId'])
        try:
            res = len(res['msg']['children'])
            if check_result(res, len(category), logger) == 0:
                raise AssertionError(traceback.format_exc())
        except:
            if check_result_is_500(res, logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('categoryId为空')
    def test_get_product_category_by_store_id(self):
        params = self.params
        params.pop('categoryId')
        logger.info(f'categoryId为空,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('storeId为空')
    def test_get_product_category_by_category_id(self):
        params = self.params
        params.pop('storeId')
        logger.info(f'storeId为空,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('不带参数获取商品信息')
    def test_get_product_category_by_none_params(self):
        logger.info('不带参数获取商品信息')
        res = http_get_noToken(self.url, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('传递不存在的categoryId')
    def test_get_product_category_by_error_category_id(self):
        params = self.params
        params['categoryId'] = 0
        logger.info(f'传递不存在的categoryId,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result(res['error_code'], 500, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('传递不存在的storeId')
    def test_get_product_category_by_error_store_id(self):
        params = self.params
        params['storeId'] = 0
        logger.info(f'传递不存在的storeId,params:{params}')
        res = http_get_noToken(self.url, params=params, result=0)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())