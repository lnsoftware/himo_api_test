from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging, allure, pytest
from common.queries import *
from conf import Api_Url as c
from httpRequests._requests import *
from common.assert_result import *

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('优惠券信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('优惠券信息')
@allure.severity('blocker')
class Test_coupons:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup(self):
        # 获取用户未失效优惠券(包括不可用)
        self.unusedCoupons = c.release + c.unusedCoupons
        # 获取用户所有优惠券信息
        self.couponsStatus = c.release + c.getUserPreferentialCard
        # 获取用户下单可用优惠券和产品体验券集合
        self.couponsProductCard = c.release + c.coupons_productCard

        # 获取用户未失效优惠券(包括不可用)初始数据
        self.unused_data = {"productIds": [8000], "storeId": 1001}
        # 获取用户所有优惠券信息参数
        self.status_data = {'status': None}
        # 获取用户下单可用优惠券和产品体验券集合
        self.couponsSet = {'productIds': [8000], 'storeId': 1001}
        # 领取春暖花开优惠券
        self.spring_coupons_data = {'index': 0}

        # 删除春暖花开券
        deleteUserSpringCoupons()

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获得用户所有优惠券数据')
    def test_getUserCouponsStatus(self):
        logger.info('获得用户所有优惠券数据')
        logger.info(f'Params,{self.status_data}')
        res = http_get(url=self.couponsStatus, params=self.status_data)
        num = get_userCouponsInfo()
        try:
            assert len(res['msg']['data']) == num
            logger.info(f'Pass,{res},数据库中查询结果{num}')
        except:
            logger.error(f'Fail,{res},数据库中查询结果{num}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获取用户所有unused状态优惠券')
    def test_getUnusedCoupons(self):
        params = self.status_data
        params['status'] = 'unused'
        logger.info('获取用户所有unused状态优惠券')
        logger.info(f'Params,{params}')
        res = http_get(url=self.couponsStatus, params=params)
        num = get_userCouponsInfo(status='unused')
        if res['msg'] is not None:
            try:
                assert len(res['msg']['data']) == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获取activated状态优惠券')
    def test_getActivatedCoupons(self):
        params = self.status_data
        params['status'] = 'activated'
        logger.info('获取用户所有activated状态优惠券')
        logger.info(f'Params,{params}')
        res = http_get(url=self.couponsStatus, params=params)
        num = get_userCouponsInfo(status='activated')
        if res['msg'] is not None:
            try:
                assert len(res['msg']['data']) == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获取used状态优惠券')
    def test_getUsedCoupons(self):
        params = self.status_data
        params['status'] = 'used'
        logger.info('获取用户所有used状态优惠券')
        logger.info(f'Params,{params}')
        res = http_get(url=self.couponsStatus, params=params)
        num = get_userCouponsInfo(status='used')
        if res['msg'] is not None:
            try:
                assert len(res['msg']['data']) == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获取abolished状态优惠券')
    def test_getAbolishedCoupons(self):
        params = self.status_data
        params['status'] = 'abolished'
        logger.info('获取用户所有abolished状态优惠券')
        logger.info(f'Params,{params}')
        res = http_get(url=self.couponsStatus, params=params)
        num = get_userCouponsInfo(status='abolished')
        if res['msg'] is not None:
            try:
                assert len(res['msg']['data']) == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('获取expired状态优惠券')
    def test_getExpiredCoupons(self):
        params = self.status_data
        params['status'] = 'expired'
        logger.info('获取用户所有expired状态优惠券')
        logger.info(f'Params,{params}')
        res = http_get(url=self.couponsStatus, params=params)
        num = get_userCouponsInfo(status='expired')
        if res['msg'] is not None:
            try:
                assert len(res['msg']['data']) == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == num
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('不传x-stream-id获取优惠券状态')
    def test_getCouponsByNoXSId(self):
        logger.info('不传x-stream-id获取优惠券状态')
        res = http_get_noToken(url=self.couponsStatus, params=self.status_data, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户所有优惠券信息')
    @allure.title('无参数获取用户优惠券信息')
    def test_getCouponsInfo_noParams(self):
        logger.info('无参数获取用户优惠券信息')
        para = self.status_data
        res = http_get(url=self.couponsStatus, params=para)
        num = get_userCouponsInfo()
        if res['msg'] is not None:
            length = len(res['msg']['data'])
            try:
                assert length == num
                logger.info(f'Pass,{length},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] is None
                logger.info(f'Pass,{res},数据库中查询结果{num}')
            except:
                logger.error(F'Fail,{res},数据库中查询结果{num}')
                logger.error(traceback.format_exc())
                raise AssertionError

    '''---------------------------------'''

    def assert_res_num(self, res, num, name):
        '''
        :param res:  接口返回消息
        :param num:  数据查询结果
        :param name:  用例名称
        :return:
        '''
        if res['msg'] is not None:
            if 'can_use' in res['msg'] and 'cannot_use' in res['msg']:
                can_use = len(res['msg']['can_use'])
                cannot_use = len(res['msg']['cannot_use'])
                count = int(can_use) + int(cannot_use)
                logger.info(f'当前用例名,{name}')
                logger.info(f'返回的优惠券数量{count},数据库中优惠券数量{num}')
                try:
                    assert count == num
                    logger.info(f'Pass,{res}')
                except:
                    logger.error(f'Fail,{res}')
                    logger.error(traceback.format_exc())
                    raise AssertionError
            elif 'can_use' in res['msg']:
                can_use = len(res['msg']['can_use'])
                logger.info(f'当前用例名,{name}')
                logger.info(f'返回的优惠券数量{can_use},数据库中优惠券数量{num}')
                try:
                    assert can_use == num
                    logger.info(f'Pass,{res}')
                except:
                    logger.error(f'Fail,{res}')
                    logger.error(traceback.format_exc())
                    raise AssertionError
            elif 'cannot_use' in res['msg']:
                cannot_use = len(res['msg']['cannot_use'])
                logger.info(f'当前用例名,{name}')
                logger.info(f'返回的优惠券数量{cannot_use},数据库中优惠券数量{num}')
                try:
                    assert cannot_use == num
                    logger.info(f'Pass,{res}')
                except:
                    logger.error(f'Fail,{res}')
                    logger.error(traceback.format_exc())
                    raise AssertionError
        else:  # 若res['msg']为空代表目前用户无优惠券,直接与数据库中查询数据进行判断
            logger.info(f'当前用例名,{name}')
            logger.info(f'返回的优惠券数量{res["msg"]},数据库中优惠券数量{num}')
            try:
                assert res['msg'] == None
                logger.info(f'Pass,{res}')
            except:
                logger.error(f'Fail,{res}')
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('获取用户未失效优惠券(包括不可用)初始数据')
    def test_getUserValidCoupons(self):
        res = http_post(url=self.unusedCoupons, json=self.unused_data)
        num = get_userVaildCoupons()
        self.assert_res_num(res, num, name='获取用户未失效优惠券(包括不可用)初始数据')

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('传递一个不存在的产品id')
    def test_getUserValidCoupons_errorPorductId(self):
        data = self.unused_data
        data['productIds'] = [1]
        num = get_userVaildCoupons()
        res = http_post(url=self.unusedCoupons, json=data)
        self.assert_res_num(res, num, name='传递一个不存在的产品id')

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('传递一个不存在的商铺id')
    def test_getUserValidCoupons_errorStoreId(self):
        data = self.unused_data
        data['storeId'] = 1
        num = get_userVaildCoupons()
        res = http_post(url=self.unusedCoupons, json=data)
        self.assert_res_num(res, num, name='传递一个不存在的商铺id')

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('不传storeId获取优惠券信息')
    def test_getUserValidCoupons_noStoreId(self):
        data = self.unused_data
        data.pop('storeId')
        logger.info(f'不传storeId获取优惠券信息,data{data}')
        res = http_post(url=self.unusedCoupons, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('不传productIds获取优惠券信息')
    def test_getUserValidCoupons_noProductIds(self):
        data = self.unused_data
        data.pop('productIds')
        logger.info(f'不传productId获取优惠券信息,data{data}')
        res = http_post(url=self.unusedCoupons, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('不传参数获取优惠券信息')
    def test_getUserValidCoupons_noData(self):
        logger.info('不传参数获取优惠券信息')
        res = http_post(url=self.unusedCoupons, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效优惠券(包括不可用)')
    @allure.title('不传x-stream-id获取优惠券信息')
    def test_getUserValidCoupons_noStoreId(self):
        logger.info(f'不传x-stream-id获取优惠券信息')
        res = http_post_noToken(url=self.unusedCoupons, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    '''-----------------------------------------'''

    def assert_coupons_productCard_true(self, res, name, productid=None, storeid=None):
        '''
        :param res: 接口请求返回数据
        :param productid: 产品id
        :param storeid: 店铺id
        :param name: 用例名
        :return: 返回None或者True
        如果res为空，返回None；
        res不为空，判断传递的productId及storeId是否在res中，若在返回true，不存在则报错
        '''
        logger.info(name)
        logger.info(f'返回数据:{res}')
        if res['msg'] is None:
            return None
        data = res['msg']['data']
        for i in range(len(data)):
            if "lower_limit" in data[i]['template']['limit'].keys():
                continue
            # if data[i]['template']['limit']['store_ids'] is not None or data[i]['template']['limit']['product_ids']:
            if data[i]['template']['limit']['store_ids'] is None:
                continue
            try:
                assert productid in data[i]['template']['limit']['product_ids'] and storeid in \
                       data[i]['template']['limit']['store_ids']
            except:
                logger.error(f'Fail,{res}')
                logger.error(f'productId,{productid},storeId,{storeid}')
                logger.error(traceback.format_exc())
                raise AssertionError

            logger.info(f'productId,{productid},storeId,{storeid}')
            logger.info(f'Pass,{res}')
            return 1

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('获取下单可使用优惠券和产品体验券')
    def test_getCouponsProductCard_canuse(self):
        res = http_post(url=self.couponsProductCard, json=self.couponsSet)
        self.assert_coupons_productCard_true(res=res,
                                             productid=self.couponsSet['productIds'][0],
                                             name='获取下单可使用优惠券和产品体验券',
                                             storeid=self.couponsSet['storeId'])

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('不传递x-stream-id获取可使用优惠券和产品体验券')
    def test_getCouponsProductCard_noXSId(self):
        logger.info('不传递x-stream-id获取可使用优惠券和产品体验券')
        res = http_post_noToken(url=self.couponsProductCard, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('不传productIds获取优惠券和产品体验券')
    def test_getCouponsProductCard_noProductIds(self):
        logger.info('不传productIds获取优惠券和产品体验券')
        data = self.couponsSet
        data.pop('productIds')
        res = http_post(url=self.couponsProductCard, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('不传storeIds获取优惠券和产品体验券')
    def test_getCouponsProductCard_noStoreIds(self):
        logger.info('不传productIds获取优惠券和产品体验券')
        data = self.couponsSet
        data.pop('storeId')
        res = http_post(url=self.couponsProductCard, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('传递不存在的productIds')
    def test_getCouponsProductCard_errorProductIds(self):
        data = self.couponsSet
        data['productIds'] = [0]
        res = http_post(url=self.couponsProductCard, json=data)
        self.assert_coupons_productCard_true(res=res,
                                             name='传递不存在的productIds',
                                             productid=data['productIds'],
                                             storeid=data['storeId'])

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('传递不存在的storeId')
    def test_getCouponsProductCard_errorStoreIds(self):
        data = self.couponsSet
        data['storeId'] = 0
        res = http_post(url=self.couponsProductCard, json=data)
        self.assert_coupons_productCard_true(res=res,
                                             name='传递不存在的storeId',
                                             productid=data['productIds'],
                                             storeid=data['storeId'])

    @allure.story('获取用户下单可用优惠券和产品体验券集合')
    @allure.title('不传参数获取用户可使用优惠券信息')
    def test_getCouponsProductCard_noData(self):
        logger.info('不传参数获取用户可使用优惠券信息')
        res = http_post(url=self.couponsProductCard, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError
