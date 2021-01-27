from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
from allure import feature, story, title
import allure
from common.queries import *
from httpRequests._requests import _requests_get, _requests_post

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

logger = Logger('礼品卡信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@feature('礼品卡信息')
@story('获取用户余额')
@allure.severity('minor')  # 一共5个等级，blocker，critical，normal，minor，trivial
class Test_giftCardBalance():
    '''
    传入用户的x-stream-id获取用户余额
    '''

    def get_id(self):
        # 获取x-stream-id
        id = get_x_stream_id()
        return id

    @title('传入正确的x-stream-id')
    def test_balance(self):
        headers = self.get_id()
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/giftCard/balance/v1'
        logger.info('title: 传入正确的x-stream-id')
        logger.info('传入的x-stream-id为:%s' % headers)
        try:
            res = _requests_get(url=url, result=1, headers=headers)
            logger.info('返回信息:%s' % res)
        except:
            logger.error(traceback.format_exc())
            raise AssertionError
        logger.info('')
        try:
            assert float(get_user_gift_card_balance(13676561839)) == float(res['msg'])
            logger.info('查询余额正确')
        except:
            logger.error('Api查询余额{},与数据库查询到的余额{}不一致'.format(res['msg'], get_user_gift_card_balance(13676561839)))
            logger.error(traceback.format_exc())
            raise AssertionError

    @title('传入空的x-stream-id查询余额')
    def test_noXSIBalance(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/user/giftCard/balance/v1'
        logger.info('不传入x-stream-id查询余额')
        try:
            res = _requests_get(url=url, result=0)
            logger.info('不传入x-stream-id返回信息{}'.format(res))
        except:
            logger.error('传入空的x-stream-id返回True')
            raise AssertionError
