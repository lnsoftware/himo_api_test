from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
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
logger = Logger('用户信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('用户信息')
@allure.story('编辑用户信息')
@allure.severity('blocker')
class Test_editUserInfo:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup(self):
        self.url = c.release + c.editUserInfo

    @allure.title('修改用户性别')
    def test_edit_user_sex(self):
        logger.info('修改用户性别')
        userinfo = http_get(url=c.release + c.userInfo)
        if userinfo['msg']['sex'] == "male":
            data = {"sex": "female"}
        elif userinfo['msg']['sex'] == "female":
            data = {'sex': "male"}
        logger.info(f'data,{data}')
        res = http_post(url=self.url, json=data)
        userinfo_after = http_get(url=c.release + c.userInfo)
        try:
            assert res['msg'] == 1
            assert userinfo_after['msg']['sex'] == data['sex'] and userinfo_after['msg']['sex'] != userinfo['msg'][
                'sex']
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('不带参数修改用户信息')
    def test_edit_user_info_no_data(self):
        logger.info('不带参数修改用户信息')
        userinfo_before = http_get(url=c.release + c.userInfo)
        res = http_post(url=self.url)
        userinfo_after = http_get(url=c.release + c.userInfo)
        try:
            assert res['msg'] == 1
            assert userinfo_before == userinfo_after
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError('response msg is : ', res['msg'])

    @allure.title('修改用户名')
    def test_edit_user_name(self):
        logger.info('修改用户名')
        data = {'name': 'xxx'}
        logger.info(f'data:{data}')
        res = http_post(url=self.url, json=data)
        userInfo = get_user_info()
        try:
            assert res['msg'] == 1
            assert userInfo['name'] == data['name']
            logger.info(f'Pass,{res},修改后返回的用户信息：{userInfo}')
        except:
            logger.error(f'Fail,{res},修改后返回的用户信息：{userInfo}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('修改用户生日')
    def test_edit_user_birth(self):
        data = {'birth': '2010-12-12'}
        logger.info('修改用户生日')
        logger.info(f'data,{data}')
        res = http_post(url=self.url, json=data, result=0)
        try:
            assert res['error_msg'] == "Once edit birth"
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('不带x-stream-id修改用户信息')
    def test_edit_user_no_x_stream_id(self):
        logger.info('不带x-stream-id修改用户信息')
        res = http_post_noToken(url=self.url, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('使用不合理的参数修改用户性别')
    def test_edit_user_sex_error_data(self):
        data = {'sex': "jkjdal"}
        res = http_post(url=self.url, json=data, result=0)
        logger.info(f'使用不合理的参数修改用户性别,{data}')
        try:
            assert res['error_code'] == 1000
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.title('使用非日期格式修改用户生日')
    def test_edit_user_birth_error_data(self):
        data = {'birth': "asd"}
        logger.info(f'使用非日期格式修改用户生日,{data}')
        res = http_post(url=self.url, json=data, result=0)
        try:
            assert res['error_msg'] == "Once edit birth"
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError
