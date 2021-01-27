from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
from common.queries import *

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('产品卡信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('产品卡信息')
@allure.severity('blocker')
class Test_ProductCard:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    """

    def http_get(self, url, phone=13676561839, password=123456, result=1, params=None):
        from httpRequests._requests import _requests_get
        '''
        此处为判断get请求是否带有参数
        '''
        if params:
            headers = get_x_stream_id(phone=phone, password=password)
            res = _requests_get(url=url, headers=headers, result=result, params=params)
            return res
        else:
            headers = get_x_stream_id(phone=phone, password=password)
            res = _requests_get(url=url, headers=headers, result=result)
            return res

    def http_post(self, url, phone=13676561839, password=123456, result=1, json=None):
        '''
        此处判断post请求是否带有json参数
        '''
        from httpRequests._requests import _requests_post
        if json is None:
            headers = get_x_stream_id(phone=phone, password=password)
            res = _requests_post(url=url, headers=headers, result=result)
            return res
        else:
            headers = get_x_stream_id(phone=phone, password=password)
            res = _requests_post(url=url, headers=headers, result=result, json=json)
            return res

    def http_get_noToken(self, url, result=1, params=None):
        from httpRequests._requests import _requests_get
        '''
        此处为判断get请求是否带有参数
        '''
        if params:
            res = _requests_get(url=url, result=result, params=params)
            return res
        else:
            res = _requests_get(url=url, result=result)
            return res

    def http_post_noToken(self, url, result=1, json=None):
        from httpRequests._requests import _requests_post
        '''
        此处为判断post请求是否带有参数
        '''
        if json:
            res = _requests_post(url=url, result=result, json=json)
            return res
        else:
            res = _requests_post(url=url, result=result)
            return res

    @allure.story('获取用户产品卡信息')
    @allure.title('获取用户所有产品卡')
    def test_getUserAllProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        res = self.http_get(url=url)
        logger.info('获取用户所有产品卡')
        logger.info('返回数据为：{}'.format(res))
        api_len = len(res['msg']['data'])
        db_len = get_userAllProductCard('13676561839')
        try:
            assert api_len == db_len
            logger.info('返回产品卡数量{}与数据库返回的产品卡总数{}一致'.format(api_len, db_len))
        except:
            logger.error('返回产品卡数量{}与数据库返回的产品卡总数{}不一致'.format(api_len, db_len))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('不传入x-stream-id获取产品卡')
    def test_noToeknGetAllProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        logger.info('不传入x-stream-id获取产品卡')
        res = self.http_get_noToken(url=url, result=0)
        logger.info('返回的数据为{}'.format(res))
        try:
            assert res['error_code'] == 401
            logger.info('pass')
        except:
            logger.error('返回的错误码不为401，{}'.format(res['error_code']))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('传入错误的参数')
    def test_errorParamsGetUserAllProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": 123321312}
        headers = get_x_stream_id()
        logger.info('传入错误的参数获取用户产品卡信息')
        res = self.http_get(url=url, params=params, result=1)
        logger.info('传参{}'.format(params))
        try:
            logger.info('传入的参数为{}'.format(params))
            assert res['msg'] is None
            logger.info('pass,{}'.format(res))
        except:
            logger.error('传入错误的参数返回了意料之外的数据{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为inactivated状态的产品卡')
    def test_getUserInactivatedProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "inactivated"}
        headers = get_x_stream_id()
        logger.info('获取status为inactivated状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='inactivated')
        if result:
            try:
                assert len(res['msg']['data']) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为activated状态的产品卡')
    def test_getUserActivatedProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "activated"}
        headers = get_x_stream_id()
        logger.info('获取status为activated状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='activated')
        if result:
            try:
                assert len(res['msg']['data']) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为unused状态的产品卡')
    def test_getUserUnusedProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "unused"}
        headers = get_x_stream_id()
        logger.info('获取status为unused状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='unused')
        if result:
            try:
                assert len(res['msg']['data']) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为expired状态的产品卡')
    def test_getUserExpiredProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "expired"}
        headers = get_x_stream_id()
        logger.info('获取status为expired状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='expired')
        if result:
            try:
                assert len(res['msg']['data']) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为abolished状态的产品卡')
    def test_getUserAbolishedProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "abolished"}
        headers = get_x_stream_id()
        logger.info('获取status为abolished状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='abolished')
        if result:
            try:
                assert len(res['msg']["data"]) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取用户产品卡信息')
    @allure.title('获取status为used状态的产品卡')
    def test_getUserAbolishedProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/getUserProductCard/v1'
        params = {"status": "used"}
        headers = get_x_stream_id()
        logger.info('获取status为used状态的产品卡')
        res = self.http_get(url=url, params=params)
        logger.info('传参{}'.format(params))
        result = get_userAllProductCard(status='used')
        if result:
            try:
                assert len(res['msg']['data']) == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            try:
                assert res['msg'] == result
                logger.info('Pass,接口返回{},数据库返回{}'.format(res, result))
            except:
                logger.error('Fail,接口返回{},数据库返回{}'.format(res, result))
                logger.error(traceback.format_exc())
                raise AssertionError

    '''
    分割线，上半部分为获取用户所有产品卡接口
    下半部分为通过传入产品IDS和门店ID返回用户所有未失效产品卡
    '''

    @allure.story('获取用户未失效产品卡信息')
    @allure.title('获取用户下单可用产品券(含未失效但不可用)')
    def test_getUserProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/availableList/v1'
        json = {"productIds": [6881], "storeId": 1001}  # 账号内的优惠券只可用于大师店，为了方便测试尽量使用非大师店门店ID
        logger.info('获取用户下单可用产品券（含未失效但不可用)')
        logger.info('json:{}'.format(json))
        res = self.http_post(url=url, json=json)
        api_len = len(res['msg']['cannot_use'])
        db_len = get_userProductCard_unused(13676561839)
        try:
            assert api_len == db_len
            logger.info('返回产品卡数量{}与数据库返回的产品卡总数{}一致'.format(api_len, db_len))
        except:
            logger.error('返回产品卡数量{}与数据库返回的产品卡总数{}不一致'.format(api_len, db_len))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效产品卡信息')
    @allure.title('不传入x-stream-id获取用户下单可用产品券')
    def test_noTokenGetUserProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/availableList/v1'
        json = {"productIds": [6881], "storeId": 1001}  # 账号内的优惠券只可用于大师店，为了方便测试尽量使用非大师店门店ID
        logger.info('不带x-stream-id获取用户下单可用产品券（含未失效但不可用)')
        logger.info('json:{}'.format(json))
        res = self.http_post_noToken(url=url, json=json, result=0)
        logger.info('不传入x-stream-id获取产品卡')
        logger.info('返回的数据为{}'.format(res))
        try:
            assert res['error_code'] == 401
            logger.info('pass')
        except:
            logger.error('返回的错误码不为401，{}'.format(res['error_code']))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效产品卡信息')
    @allure.title('传入空值获取用户产品卡信息')
    def test_errorJsonGetUserProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/availableList/v1'
        headers = get_x_stream_id()
        json = {"productIds": None, "storeId": None}
        logger.info('传入空值获取用户产品卡信息')
        res = self.http_post(url=url, json=json, result=0)
        try:
            logger.info('传入空值获取用户产品卡信息')
            assert res['error_code'] == 422
            logger.info('pass,{}'.format(res))
        except:
            logger.error('传入空值返回信息有误{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效产品卡信息')
    @allure.title('只传productIds获取产品卡信息')
    def test_onlyProductIdsGetUserProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/availableList/v1'
        headers = get_x_stream_id()
        json = {"productIds": [6881]}
        logger.info('只传入productIds获取产品卡信息')
        logger.info('传参{}'.format(json))
        res = self.http_post(url=url, json=json, result=0)
        try:
            logger.info('只传productIds获取产品卡信息')
            assert res['error_code'] == 422
            logger.info('pass,{}'.format(res))
        except:
            logger.error('只传productIds获取产品卡信息返回有误{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取用户未失效产品卡信息')
    @allure.title('只传storeId获取产品卡信息')
    def test_onlyStoreIdGetUserProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/availableList/v1'
        headers = get_x_stream_id()
        json = {"storeId": 1001}
        logger.info('只传storeId获取产品卡信息')
        logger.info('传参{}'.format(json))
        res = self.http_post(url=url, json=json, result=0)
        try:
            logger.info('只传storeId获取产品卡信息')
            assert res['error_code'] == 422
            logger.info('pass,{}'.format(res))
        except:
            logger.error('只传storeId获取产品卡信息返回有误{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("绑定产品卡")
    @allure.title('不传入x-stream-id绑定产品卡')
    def test_bindingProductCard(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/productCard/bind/v1'
        json = {"code": "dsadsadsdsa"}
        logger.info('绑定错误的产品卡{}'.format(json))
        res = self.http_post_noToken(url=url, json=json, result=0)
        try:
            assert res['error_code'] == 401
            logger.info('pass,{}'.format(res))
        except:
            logger.info('绑定错误的产品卡返回信息有误{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError
