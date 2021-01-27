from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure

'''
测试用例模板
'''

logger = Logger('城市门店相关', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('城市门店相关')
@allure.story('城市')
@allure.title('获取城市列表')
def test_get_city_list():
    import requests
    url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getCityInBlueAndGold/v1'
    res = requests.get(url=url)
    logger.info('当前测试用例名称|获取城市列表|')
    try:
        assert res.status_code == 200  # 判断是否请求成功
    except:
        logger.error('请求失败,响应码为:{}'.format(res.status_code))
        logger.error(traceback.format_exc())
        raise AssertionError
    res = res.json()  # 获取返回值
    try:
        assert res['success'] == 1  # 判断是否为True
    except:
        logger.error('查询失败,查询结果为:')
        logger.error(res)
        raise AssertionError
    try:
        from common.queries import get_city_list as g
        assert len(res['msg']['data']) == g()  # 判断获取的城市列表数量是否与数据库城市数量一致
        logger.info('通过,数据库中城市列表数量为{},获取到的城市列表数量{}'.format(g(), len(res['msg']['data'])))
    except:
        logger.error('获取城市列表数量有误,数据库中城市列表数量为{},获取到的城市列表数量{}'.format(g(), len(res['msg']['data'])))
        raise AssertionError
