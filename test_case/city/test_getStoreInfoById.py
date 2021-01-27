from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
from allure import feature, story, title
import allure
from common.queries import *

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

logger = Logger('城市门店相关', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@feature('城市门店相关')
@story('城市')
@allure.severity('minor')
class Test_get_storeInfo_by_id():
    '''
    先获取所有有门店的城市ID,
    通过城市ID获取所有门店ID
    最后通过门店ID查询门店信息
    '''

    def getCityList(self):
        # 获取所有城市ID
        from httpRequests._requests import _requests_get
        get_city_url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getCityInBlueAndGold/v1'
        res = _requests_get(url=get_city_url, result=1)
        res = res['msg']['data']  # 获取返回的的json串中的['data']
        cityId = []
        for i in range(len(res)):
            cityId.append(res[i]['id'])
        return cityId  # 循环读取保存下来的城市id列表

    def getStoreId(self):
        # 获取城市id列表
        cityId = self.getCityList()
        sbc_url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getStoresByCity/v1'
        from httpRequests._requests import _requests_post
        storeId = []
        json = {'cityIds': cityId}
        res = _requests_post(url=sbc_url, json=json, result=1, headers=None)
        res = res['msg']['data']
        for a in range(len(res)):
            storeId.append(res[a]['id'])
        from common.queries import get_all_store_by_city
        assert len(storeId) == get_all_store_by_city()
        return storeId

    @title('获取门店信息')
    def test_getStoreInfoById(self):
        sid = self.getStoreId()
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getStoreInfoById/v1'
        for i in range(len(sid)):
            params = {
                'storeId': sid[i]
            }
            # 通过门店id获取门店信息判断返回的门店id是否与传入的门店id一致
            logger.info('获取门店信息')
            logger.info('入参:{}'.format(params))
            from httpRequests._requests import _requests_get
            try:
                res = _requests_get(url=url, params=params, result=1)
                assert res['msg']['id'] == sid[i]
                logger.info('Pass')
            except:
                logger.error('获取门店信息失败')
                raise AssertionError

    @title('不传入门店is获取信息')
    def test_NoStoreIdGetStoreInfo(self):
        url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getStoreInfoById/v1'
        params = {
            'storeId': []
        }
        logger.info('获取门店信息')
        logger.info('入参:{}'.format(params))
        from httpRequests._requests import _requests_get
        res = _requests_get(url=url, params=params, result=0)
        try:
            assert res['error_code'] == 422
            logger.info('pass')
        except:
            logger.error('传入空值返回正常数据{}'.format(res))
            raise AssertionError
