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
logger = Logger('订单评分', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('订单评分')
@allure.severity('blocker')
class Test_submitNPS:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    def setup(self):
        # 提交nps问卷
        self.nps_creat = c.release + c.nps_creat
        # 查看nps状态
        self.nps_status = c.release + c.nps_status

    def nps_data(self):
        '''
        由于订单号只能使用一次,所以仅测试异常.正常流程手工测试
        :return: nps问卷测试数据
        '''
        data = {"npsAll": 10, "npsReceptionist": 10, "npsCameraman": 10, "npsDresser": 10, "npsRetoucher": 10,
                "npsNote": "", "isSn": 0, "isShare": 0, "orderNum": "T2020041062297444"}
        return data

    @allure.story('NPS问卷')
    @allure.title('无orderNum提交NPS问卷')
    def test_submitNPS_noOrderNum(self):
        data = self.nps_data()
        data.pop('orderNum')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无orderNum提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无npsAll提交NPS问卷')
    def test_submitNPS_noNpsAll(self):
        data = self.nps_data()
        data.pop('npsAll')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无npsAll提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无npsReceptionist提交NPS问卷')
    def test_submitNPS_noNpsReceptionist(self):
        data = self.nps_data()
        data.pop('npsReceptionist')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无npsReceptionist提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无npsCameraman提交NPS问卷')
    def test_submitNPS_noNpsCameraman(self):
        data = self.nps_data()
        data.pop('npsCameraman')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无npsCameraman提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无npsDresser提交NPS问卷')
    def test_submitNPS_noNpsDresser(self):
        data = self.nps_data()
        data.pop('npsDresser')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无npsDresser提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无npsRetoucher提交NPS问卷')
    def test_submitNPS_noNpsRetoucher(self):
        data = self.nps_data()
        data.pop('npsRetoucher')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无npsRetoucher提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无isShare提交NPS问卷')
    def test_submitNPS_noIsShare(self):
        data = self.nps_data()
        data.pop('isShare')
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("无isShare提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['success'] == 0
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('无x-stream-id提交NPS问卷')
    def test_submitNPS_noXSId(self):
        data = self.nps_data()
        res = http_post_noToken(url=self.nps_creat, json=data, result=0)
        logger.info("无isShare提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_code'] == 401
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('使用非此订单账号的x-stream-id提交NPS问卷')
    def test_submitNPS_errorXSId(self):
        data = self.nps_data()
        res = http_post(url=self.nps_creat, json=data, result=0)
        logger.info("使用非此订单账号的x-stream-id提交NPS问卷")
        logger.info(f'data,{data}')
        try:
            assert res['error_msg'] == "order not exist"
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    '''----------------------------'''

    @allure.story("NPS问卷")
    @allure.title('查看已提交nps问卷状态')
    def test_npsStatus(self):
        params = {'orderNum': 'T2020041062297444'}
        logger.info('查看已提交nps问卷状态')
        logger.info(f'params,{params}')
        res = http_get(url=self.nps_status, phone=13676564148, password=123321, params=params, result=0)
        try:
            assert res['success'] == 0
            logger.info(f'Pass,{res}')
        except:
            logger.info(f'Fail,{res}')
            logger.info(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('使用其他账号的x-stream-id查询订单状态')
    def test_npsStatus_otherXSId(self):
        url = self.nps_status
        params = {'orderNum': 'T2020041062297444'}
        logger.info('使用其他账号的x-stream-id查询订单状态')
        logger.info(f'params,{params}')
        res = http_get(url=url, params=params, result=0)
        try:
            assert res['error_msg'] == 'order not exist'
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('不传orderNum获取订单状态')
    def test_npsStatus_noOrderNum(self):
        logger.info('不传orderNum获取订单状态')
        res = http_get(url=self.nps_status, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("NPS问卷")
    @allure.title('不传x-stream-id获取订单状态')
    def test_npsStatus_noXSId(self):
        params = {'orderNum': 'T2020041062297444'}
        logger.info(f'不传x-stream-id获取订单状态,params:{params}')
        res = http_get_noToken(url=self.nps_status, params=params, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('NPS问卷')
    @allure.title('查询一个不存在的订单')
    def test_npsStatus_errorOrder(self):
        params = {'orderNum': "sdasdsa"}
        logger.info('查询一个不存在的订单')
        res = http_get(url=self.nps_status, params=params, result=0)
        try:
            assert res['error_msg'] == 'order not exist'
            assert res['error_code'] == 60179882249
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError
