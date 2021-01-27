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
@allure.story('通过门店id获得商品折扣信息')
@allure.severity('blocker')
class Test_getProductDiscountDetailByStoreId:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.productDiscountDetailByStoreId

    @title('获取一线蓝标店商品折扣信息')
    def test_get_product_discount_detail_by_blue(self):
        params = {"storeId": 1051}
        logger.info(f'获取一线蓝标店商品折扣信息,params:{params}')
        res = http_get(self.url, params=params)
        num = get_area_classification_id(params['storeId'])
        if check_result(len(res['msg']['data']), len(num['num']), logger) == 0:
            raise AssertionError(traceback.format_exc())
        for i in res['msg']['data']:
            if check_res_in(i['store_classification_id'], num['area_id'], logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('获取二线蓝标店商品折扣信息')
    def test_get_product_discount_detail_by_blue_2(self):
        params = {"storeId": 1001}
        logger.info(f'获取二线蓝标店商品折扣信息,params:{params}')
        res = http_get(self.url, params=params)
        num = get_area_classification_id(params['storeId'])
        if check_result(len(res['msg']['data']), len(num['num']), logger) == 0:
            raise AssertionError(traceback.format_exc())
        for i in res['msg']['data']:
            if check_res_in(i['store_classification_id'], num['area_id'], logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('获取大师店商品折扣信息')
    def test_get_product_discount_detail_by_gold(self):
        params = {"storeId": 1169}
        logger.info(f'获取大师店商品折扣信息,params:{params}')
        res = http_get(self.url, params=params)
        num = get_area_classification_id(params['storeId'])
        if check_result(len(res['msg']['data']), len(num['num']), logger) == 0:
            raise AssertionError(traceback.format_exc())
        for i in res['msg']['data']:
            if check_res_in(i['store_classification_id'], num['area_id'], logger) == 0:
                raise AssertionError(traceback.format_exc())

    @title('传递不存在的门店id')
    def test_get_product_discount_detail_by_error_store_id(self):
        params = {'storeId': 0}
        logger.info(f'传递不存在的门店id,params:{params}')
        res = http_get(self.url, params=params, result=0)
        if check_result_is_500(res, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @title('不带参数获取折扣信息')
    def test_get_product_discount_detail_not_params(self):
        logger.info('不带参数获取折扣信息')
        res = http_get_noToken(self.url, result=0)
        if check_result_is_422(res, logger) == 0:
            raise AssertionError(traceback.format_exc())