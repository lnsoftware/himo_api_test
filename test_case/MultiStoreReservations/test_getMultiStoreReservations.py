from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
from common.queries import *
from conf import Api_Url as c

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('排单表', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('排单表')
@allure.severity('blocker')
class Test_getMultiStoreReservations:
    '''
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    '''

    # setup做的是生成接口地址
    def setup(self):
        self.MultiStoreReservationsUrl = c.release + c.getMultiStoreReservations
        self.getReservationListurl = c.release + c.getReservationList

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

    # 这里的数据是给获取多门店预约时间段信息准备的
    def dataToTest(self):
        data = {"date": "2030-03-06", "cityId": 330100000, "productGroup": [
            {"id": 5499, "people": 1, "num": 1, "services": [{"id": 5501, "people": 1, "num": 1}]}]}
        '''默认返回的城市Id为杭州'''
        return data

    def assert_reservation_is0(self, data):
        a = data['msg']['data']
        for i in range(len(a)):
            try:
                assert a[i]['reservation_reserve'] == 0
                return True
            except:
                return False

    '''
    此处两个接口对people/num后台已写死,暂不做等价类测试(如传0)
    为了方便测试,传入的门店都只有一家
    '''

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('获取杭州今日或之后所有门店可预约时间段信息')
    def test_getHZAllStore(self):
        import datetime
        data = self.dataToTest()
        url = self.MultiStoreReservationsUrl
        H = int(datetime.datetime.now().strftime("%H"))
        # 当日时间不能大于22点或小于9点
        if H >= 22 or H <= 10:
            tomorrow = str(datetime.datetime.now() + datetime.timedelta(days=1))
            data['date'] = tomorrow[0:10]
            logger.info('获取明天所有门店可预约时间段信息')
            logger.info('data:{}'.format(data))
            res = self.http_post(url=url, json=data)
            try:
                assert res['msg'] is not None
                logger.info('Pass,{}'.format(res))
            except:
                logger.error('Fail,{}'.format(res))
                logger.error(traceback.format_exc())
                raise AssertionError
        else:
            today = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            data['date'] = today
            logger.info('获取杭州今日所有门店可预约时间段信息')
            logger.info('data:{}'.format(data))
            res = self.http_post(url=url, json=data)
            try:
                assert res['msg'] is not None
                logger.info('Pass,{}'.format(res))
            except:
                logger.error('Fail,{}'.format(res))
                logger.error(traceback.format_exc())
                raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('获取昨天所有门店可预约时间段信息')
    def test_getHZAllStoreByYesterday(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        import datetime
        yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
        data['date'] = yesterday[0:10]
        logger.info('获取昨天所有门店可预约时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        result = self.assert_reservation_is0(res)
        try:
            assert result == 1
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('获取明天天所有门店可预约时间段信息')
    def test_getHZAllStoreByTomorrow(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        import datetime
        tomorrow = str(datetime.datetime.now() + datetime.timedelta(days=1))
        data['date'] = tomorrow[0:10]
        logger.info('获取明天所有门店可预约时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('不传入x-stream-id获取时间段信息')
    def test_getAllStoreNoXSId(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        logger.info('不传入x-stream-id获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post_noToken(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 401
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('不传入productGroup获取时间段信息')
    def test_getAllStoreNoProductGroup(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data.pop('productGroup')
        logger.info('不传入productGroup获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('不传入services获取时间段信息')
    def test_getAllStoreNoServices(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0].pop('services')
        logger.info('不传入services获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入错误的productGroup获取时间段信息')
    def test_getAllStoreErrorProductGroup(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0]['id'] = 12312321
        logger.info('传入错误的productGroup获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        result = self.assert_reservation_is0(res)
        try:
            assert result == 1
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入错误的services获取时间段信息')
    def test_getAllStoreErrorServices(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0]['services'][0]['id'] = 12312321
        logger.info('传入错误的services获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入错误的cityId获取时间段信息')
    def test_getAllStoreErrorCityId(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['cityId'] = 72167218787218721
        logger.info('传入错误的cityId获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data)
        try:
            assert res['msg'] is None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('不传入cityId获取时间段信息')
    def test_getAllStoreNoCityId(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data.pop('cityId')
        logger.info('不传入cityId获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('不传入date获取时间段信息')
    def test_getAllStoreNoDate(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data.pop('date')
        logger.info('不传入date获取时间段信息')
        logger.info('data:{}'.format(data))
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入不合理的people')
    def test_getAllStoreByErrorPeople(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0]['people'] = 10000
        logger.info('传入不合理的people')
        logger.info('data,{}'.format(data))
        res = self.http_post(json=data, url=url)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback)
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入不合理的num')
    def test_getAllStoreByErrorNum(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0]['num'] = 10000
        logger.info('传入不合理的num')
        logger.info('data,{}'.format(data))
        res = self.http_post(json=data, url=url)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback)
            raise AssertionError

    @allure.story('获取多门店可预约时间段信息')
    @allure.title('传入不合理的people和num')
    def test_getAllStoreByErrorPeopleAndNum(self):
        url = self.MultiStoreReservationsUrl
        data = self.dataToTest()
        data['productGroup'][0]['people'] = 10000
        data['productGroup'][0]['num'] = 10000
        logger.info('传入不合理的people和num')
        logger.info('data,{}'.format(data))
        res = self.http_post(json=data, url=url)
        try:
            assert res['msg'] is not None
            logger.info('Pass,{}'.format(res))
        except:
            logger.error('Fail,{}'.format(res))
            logger.error(traceback)
            raise AssertionError

    '''------------------------------------------------------'''

    # 这里的数据是给获取排单表准备的
    def makeDataToTest(self):
        data = {"dateStart": "2020-03-23", "dateEnd": "2020-03-24", "storeId": 1004, "productGroup": [
            {"id": 5499, "people": 1, "num": 1, "services": [{"id": 5501, "people": 1, "num": 1}]}]}
        return data

    def assertReserveIs0(self, data):
        if len(data['msg']['data']) == 1:
            morning = data['msg']['data'][0]['reservation_list']["morning"]
            for i in range(len(morning)):
                assert morning[i]['reserve'] == 0
            afternoon = data['msg']['data'][0]['reservation_list']["afternoon"]
            for i in range(len(afternoon)):
                assert afternoon[i]['reserve'] == 0
            night = data['msg']['data'][0]['reservation_list']["night"]
            for i in range(len(night)):
                assert night[i]['reserve'] == 0
        else:
            ''' 传递日期时,不要传那么多天数,昨天,今天,明天即可 '''
            return None

    @allure.story("获取排单表数据")
    @allure.title("获取今日排单表数据")
    def test_getReservationListFromToday(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        data['dateStart'] = today
        data['dateEnd'] = today
        logger.info('获取今日排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data)
        try:
            assert len(res['msg']['data']) == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("获取昨天排单表数据")
    def test_getReservationListFromToday(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
        data['dateStart'] = yesterday[0:10]
        data['dateEnd'] = yesterday[0:10]
        logger.info('获取昨天排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data)
        try:
            self.assertReserveIs0(res)
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story('获取排单表数据')
    @allure.title("获取明天排单表数据")
    def test_getReservationListFromTomorrow(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        tomorrow = str(datetime.datetime.now() + datetime.timedelta(days=1))
        data['dateStart'] = tomorrow[0:10]
        data['dateEnd'] = tomorrow[0:10]
        logger.info('获取明天排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data)
        try:
            assert len(res['msg']['data']) == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("传入错误的dateStart")
    def test_getReservationList_errorDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['dateStart'] = 'asd'
        logger.info('传入错误的dateStart')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("传入错误的dateEnd")
    def test_getReservationList_errorDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['dateEnd'] = 'asd'
        logger.info('传入错误的dateEnd')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("传入不存在的stroeId")
    def test_getReservationList_errorDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['storeId'] = 1
        logger.info('传入不存在的stroeId')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 500
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("dateEnd<dateStart")
    def test_getReservationList_dateEndLessDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        tomorrow = str(datetime.datetime.now() + datetime.timedelta(days=1))
        data['dateStart'] = tomorrow[0:10]
        yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
        data['dateEnd'] = yesterday[0:10]
        logger.info('dateEnd<dateStart')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data)
        try:
            assert res['msg'] == None
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传x-stream-id获取排单表数据")
    def test_getReservationListNoXSId(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        data['dateStart'] = today
        data['dateEnd'] = today
        logger.info('不传x-stream-id获取排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post_noToken(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 401
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传dateStart字段获取排单表数据")
    def test_getReservationListNoDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data.pop('dateStart')
        logger.info('不传dateStart字段获取排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传dateEnd字段获取排单表数据")
    def test_getReservationListNoDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data.pop('dateEnd')
        logger.info('不传dateEnd字段获取排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传storeId字段获取排单表数据")
    def test_getReservationListNoDateStart(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data.pop('storeId')
        logger.info('不传storeId字段获取排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传services获取排单表数据")
    def test_getReservationListNoServices(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        import datetime
        tomorrow = str(datetime.datetime.now() + datetime.timedelta(days=1))
        data['dateStart'] = tomorrow[0:10]
        data['dateEnd'] = tomorrow[0:10]
        data['productGroup'][0].pop("services")
        logger.info('不传services字段获取排单表数据')
        logger.info(f'data:{data}')
        res = self.http_post(url=url, json=data)
        try:
            assert len(res['msg']['data']) == 1
            logger.info(f'Pass,{res}')
        except:
            logger.error(f'Fail,{res}')
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传productGroup获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data.pop('productGroup')
        logger.info('不传productGroup获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传productGroup中的Id获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0].pop('id')
        logger.info('不传productGroup中的ID获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传productGroup中的people获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0].pop('people')
        logger.info('不传productGroup中的people获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传productGroup中的num获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0].pop('num')
        logger.info('不传productGroup中的num获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传services中的id获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0]['services'][0].pop('id')
        logger.info('不传services中的id获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传services中的people获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0]['services'][0].pop('people')
        logger.info('不传services中的people获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError

    @allure.story("获取排单表数据")
    @allure.title("不传services中的num获取排单表数据")
    def test_getReservationListNoProductGroup(self):
        url = self.getReservationListurl
        data = self.makeDataToTest()
        data['productGroup'][0]['services'][0].pop('num')
        logger.info('不传services中的num获取排单表数据')
        logger.info(f'data,{data}')
        res = self.http_post(url=url, json=data, result=0)
        try:
            assert res['error_code'] == 422
            logger.info(f"Pass,{res}")
        except:
            logger.error(f"Fail,{res}")
            logger.error(traceback.format_exc())
            raise AssertionError
