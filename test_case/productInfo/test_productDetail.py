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
@allure.story('获取多个产品详情')
@allure.severity('blocker')
class Test_productDetail:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.productDetail
        self.data = {'storeId': 1001, "productIds": ['5443']}

    @allure.title('获取单个产品的详情')
    def test_get_one_product_detail(self):
        logger.info(f'获取单个产品的详情,data:{self.data}')
        res = http_post(self.url, json=self.data)
        data = get_product_info(self.data['productIds'])
        if check_result(
                res['msg']['data'][0]['name'],
                data['name'], logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带x-stream-id获取产品详情')
    def test_get_product_detail_not_x_stream_id(self):
        logger.info(f'不带x-stream-id获取产品详情,data:{self.data}')
        res = http_post_noToken(self.url, json=self.data)
        data = get_product_info(self.data['productIds'])
        if check_result(
                res['msg']['data'][0]['name'],
                data['name'], logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('获取多个产品详情')
    def test_get_product_detail(self):
        data = self.data
        data['productIds'].append('5600')
        logger.info(f'获取多个产品详情,data:{data}')
        res = http_post_noToken(self.url, json=data)
        data = get_product_info(data['productIds'])
        data.reverse()
        from jsonpath import jsonpath
        res = jsonpath(res, "$.msg.data.*.name")
        data = jsonpath(data, "$..name")
        if check_result(res, data[::-1], logger) == 0:
            raise AssertionError(traceback.format_exc())


    @allure.title('查询不存在的商品id')
    def test_check_error_product_id(self):
        data = {'storeId': 1001, "productIds": ['0']}
        logger.info(f'查询不存在的商品id,{data}')
        res = http_post_noToken(self.url, json=data)
        db_data = get_product_info(data['productIds'])
        if check_result(res['msg'], db_data, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('使用不存在的商店id查询')
    def test_get_product_detail_by_error_store_id(self):
        data = {'storeId': 0, "productIds": [5600]}
        logger.info(f'使用不存在的商品id查询,{data}')
        res = http_post_noToken(self.url, json=data, result=0)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带productIds获取商品详情')
    def test_get_product_detail_not_product_ids(self):
        data = self.data
        data.pop("productIds")
        logger.info(f'不带productIds获取商品详情,data:{data}')
        res = http_post_noToken(self.url, json=data, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带storeId获取商品详情')
    def test_get_product_detail_not_store_id(self):
        data = self.data
        data.pop("storeId")
        logger.info(f'不带productIds获取商品详情,data:{data}')
        res = http_post_noToken(self.url, json=data, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('storeId使用英文字母获取商品详情')
    def test_get_product_detail_use_english(self):
        data = self.data
        data['storeId'] = 'one'
        logger.info(f'storeId使用英文字母获取商品详情,data:{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('productIds使用英文字母获取商品详情')
    def test_get_product_detail_use_english_product(self):
        data = self.data
        data['productIds'] = 'one'
        logger.info(f'productIds使用英文字母获取商品详情,data:{data}')
        res = http_post(self.url, json=data, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())
