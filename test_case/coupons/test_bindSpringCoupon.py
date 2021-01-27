from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure, pytest
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
logger = Logger('', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@pytest.mark.skip('app暂时无该功能')
@allure.feature('优惠券信息')
@allure.story('春暖花开')
@allure.severity('blocker')
class Test_springCoupon:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        # 领取春暖花开优惠券
        self.spring_coupons = c.release + c.spring_coupons
        # 春暖花开优惠券领取信息
        self.spring_status = c.release + c.spring_status

    '''-----------------------------------------------'''

    @allure.title('正常领取春暖花开优惠券')
    def test_bindSpringCoupon(self):
        logger.info('正常领取春暖花开优惠券')
        logger.info(f'json:{self.spring_coupons_data}')
        deleteUserSpringCoupons()  # 先把账号中的春暖花开优惠券删掉
        res = http_post(url=self.spring_coupons, json=self.spring_coupons_data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('多次领取春暖花开优惠券')
    def test_bindSpringCoupon_repeatToReceive(self):
        deleteUserSpringCoupons()
        res = http_post(url=self.spring_coupons, json=self.spring_coupons_data)
        for i in range(3):
            res = http_post(url=self.spring_coupons, json=self.spring_coupons_data, result=0)
            try:
                assert res['error_msg'] == "cant receive twice"
            except:
                logger.error(f'Pass,{res}')
                logger.error(traceback.format_exc())
                raise AssertionError
        logger.info(f'Pass,{res}')

    @allure.title('不带x-stream-id领取春暖花开优惠券')
    def test_bindSpringCoupon_noXSId(self):
        logger.info('不带x-stream-id领取春暖花开优惠券')
        res = http_post_noToken(url=self.spring_coupons, json=self.spring_coupons_data, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('不传index领取春暖花开优惠券')
    def test_bindSpringCoupon_noIndex(self):
        logger.info('不传index领取春暖花开优惠券')
        res = http_post(url=self.spring_coupons, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('传负数领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIsNegative(self):
        data = self.spring_coupons_data
        data['index'] = -1
        logger.info(f'传负数领取春暖花开优惠券,{data}')
        deleteUserSpringCoupons()
        res = http_post(url=self.spring_coupons, json=data, result=0)
        try:
            assert res['error_code'] == 500
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('index为1领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIs1(self):
        data = self.spring_coupons_data
        data['index'] = 6
        deleteUserSpringCoupons()
        logger.info(f'index为1领取春暖花开优惠券,{data}')
        res = http_post(url=self.spring_coupons, json=data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('index为6领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIs6(self):
        data = self.spring_coupons_data
        data['index'] = 6
        deleteUserSpringCoupons()
        logger.info(f'index为6领取春暖花开优惠券,{data}')
        res = http_post(url=self.spring_coupons, json=data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('index为7领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIs7(self):
        data = self.spring_coupons_data
        data['index'] = 7
        deleteUserSpringCoupons()
        logger.info(f'index为7领取春暖花开优惠券,{data}')
        res = http_post(url=self.spring_coupons, json=data)
        try:
            assert res['msg'] == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('index为8领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIs8(self):
        data = self.spring_coupons_data
        data['index'] = 8
        deleteUserSpringCoupons()
        logger.info(f'index为8领取春暖花开优惠券,{data}')
        res = http_post(url=self.spring_coupons, json=data, result=0)
        try:
            assert res['error_code'] == 500
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('index为小数领取春暖花开优惠券')
    def test_bindSpringCoupon_indexIsFloat(self):
        data = self.spring_coupons_data
        data['index'] = 0.1
        deleteUserSpringCoupons()
        logger.info(f'index为8领取春暖花开优惠券,{data}')
        res = http_post(url=self.spring_coupons, json=data)
        try:
            assert res['error_code'] == 500
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    '''-------------------------------------------------------'''

    @allure.title('查询已领取春暖花开优惠券用户信息')
    def test_springCouponsStatus(self):
        logger.info('查询已领取春暖花开优惠券用户信息')
        res = http_get(url=self.spring_status, phone=13676564148, password=123321)
        try:
            assert res['msg'] is not None
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('查询未领取春暖花开优惠券用户信息')
    def test_springCouponsStatus_haveNot(self):
        logger.info('查询未领取春暖花开优惠券用户信息')
        res = http_get(url=self.spring_status)
        try:
            assert res['msg'] is None
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('不传x-stream-id获取春暖花开优惠券信息')
    def test_springCouponsStatus_noXSId(self):
        logger.info('不传x-stream-id获取春暖花开优惠券信息')
        res = http_get_noToken(url=self.spring_status, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError
