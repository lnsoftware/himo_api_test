from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure, pytest
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
logger = Logger('登录注册', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('登录注册')
@allure.severity('blocker')
class Test_loginByToken():
    def setup_class(self):
        url = c.release + 'user_auth/getTokenFromApp'
        data = {"brand": "mantu_app", "deviceToken": "12345"}
        http_get(url=url, params=data)

    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

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

    ''' 获取Token '''

    @allure.story('获取Token')
    @allure.title('带x-stream-id获取Token')
    def test_getToken(self):
        url = c.release + c.app_get_token
        params = {'brand': 'mantu_app', "deviceToken": get_userDevices()}
        logger.info('带x-stream-id获取Token')
        logger.info('传参{}'.format(params))
        res = self.http_get(url=url, result=1, params=params)
        try:
            assert len(res['msg']) == 48
            logger.info('pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取Token')
    @allure.title('不带x-stream-id获取Token')
    def test_getToeknNoXSId(self):
        url = c.release + c.app_get_token
        params = {'brand': 'mantu_app'}
        logger.info('不带x-stream-id获取Token')
        logger.info('传参{}'.format(params))
        res = self.http_get_noToken(url=url, result=0, params=params)
        try:
            assert res['error_code'] == 401
            logger.info('pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取Token')
    @allure.title('传空值获取Token')
    def test_goTokenNoParams(self):
        url = c.release + c.app_get_token
        logger.info('不带参数获取Token')
        res = self.http_get(url=url, result=0)
        try:
            assert res['error_code'] == 422
            logger.info('传空值时会默认带brand=mantu_app')
            logger.info('pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    ''' Token登录 '''

    @allure.story('Token登录')
    @allure.title('使用Token和x-stream-id进行登录')
    def test_loginByToken(self):
        url = c.release + c.login_by_token
        params = {'token': get_token_by_xsid(), 'brand': 'mantu_app'}
        logger.info('使用Token和x-stream-id进行登录')
        logger.info('传参{}'.format(params))
        res = self.http_get(url=url, params=params)
        try:
            assert res['msg'] == 'login success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token登录')
    @allure.title('不带x-stream-id登录')
    def test_loginByTokenNoXSId(self):
        url = c.release + c.login_by_token
        params = {'token': get_token_by_xsid(), 'brand': 'mantu_app'}
        logger.info('不带x-stream-id使用token登录')
        logger.info('传参{}'.format(params))
        res = self.http_get_noToken(url=url, params=params)
        try:
            assert res['msg'] == 'login success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token登录')
    @allure.title('不带Token登录')
    def test_loginByTokenNoToken(self):
        url = c.release + c.login_by_token
        params = {'brand': 'mantu_app'}
        logger.info('不带Token进行登录')
        logger.info('传参{}'.format(params))
        res = self.http_get_noToken(url=url, params=params, result=0)
        try:
            assert 'validation.required' in str(res['error_msg'])
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token登录')
    @allure.title('不带brand登录')
    def test_loginByTokenNoBrand(self):
        url = c.release + c.login_by_token
        params = {'token': get_token_by_xsid()}
        logger.info('不带brand登录')
        logger.info('传参{}'.format(params))
        res = self.http_get_noToken(url=url, params=params, result=0)
        try:
            assert 'validation.required' in str(res['error_msg'])
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token登录')
    @allure.title('传空值登录')
    def test_loginByTokenNoBrand(self):
        url = c.release + c.login_by_token
        logger.info('传空值登录')
        res = self.http_get_noToken(url=url, result=0)
        try:
            assert 'validation.required' in str(res['error_msg'])
            assert len(res['error_msg']) == 2
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token登录')
    @allure.title('使用退出的Token进行登录')
    def test_loginByLogOutToken(self):
        url = c.release + c.logout
        token = get_token_by_xsid()
        params = {'token': token, "brand": 'mantu_app'}
        res = self.http_get(url=url, params=params)
        try:
            assert res['msg'] == 'logout success'
        except:
            logger.error('Token退出失败，{}'.format(res))
            raise AssertionError
        url = c.release + c.login_by_token
        params = {'token': token, "brand": 'mantu_app'}
        res = self.http_get(url=url, params=params, result=0)
        try:
            assert res['error_msg'] == 'the token is invalid'
            logger.info('使用退出的Token进行Token登录Pass,{}'.format(res))
        except:
            logger.error('使用退出的Token进行Token登录Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    ''' Token退出 '''

    @allure.story('Token退出')
    @allure.title('不带x-stream-id与Token退出')
    def test_logOutNoXSIdToken(self):
        url = c.release + c.logout
        logger.info('不带x-stream-id与Token退出')
        res = self.http_get_noToken(url=url)
        try:
            assert res['msg'] == 'logout success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error("Fail，{}".format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token退出')
    @allure.title('带x-stream-id不带Token退出')
    def test_logOutByXSIdNoToken(self):
        url = c.release + c.logout
        logger.info('带x-stream-id不带Token退出登录')
        res = self.http_get(url=url)
        try:
            assert res['msg'] == 'logout success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error("Fail，{}".format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token退出')
    @allure.title('带x-stream-id与Token退出')
    def test_logoutByTokenXSId(self):
        url = c.release + c.logout
        params = {'token': get_token_by_xsid()}
        logger.info('带x-stream-id与Token退出')
        logger.info('传参，{}'.format(params))
        res = self.http_get(url=url, params=params)
        try:
            assert res['msg'] == 'logout success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error("Fail，{}".format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('Token退出')
    @allure.title('带Token不带X-stream-id退出')
    def test_logoutByTokenNoXSId(self):
        url = c.release + c.logout
        params = {'token': get_token_by_xsid()}
        logger.info('带Token不带x-stream-id退出登录')
        res = self.http_get_noToken(url=url, params=params)
        try:
            assert res['msg'] == 'logout success'
            logger.info('Pass,{}'.format(res))
        except:
            logger.error("Fail，{}".format(res))
            logger.error(traceback.format_exc())
            raise AssertionError
