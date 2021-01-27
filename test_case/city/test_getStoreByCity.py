from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
from allure import feature, story, title
import allure

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

logger = Logger('城市门店相关', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.severity('critical')
@feature('城市门店相关')
@story('城市')
@title('通过城市ID获取门店列表数量')
def test_get_store_by_city():
    import requests
    from common.queries import get_city_id, get_store_by_city
    id = get_city_id()  # 获取所有城市id
    url = 'https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getStoresByCity/v1'
    for i in id:  # 获取单个城市下的门店列表
        # 通过for循环读取城市列表,放入json
        json = {
            'cityIds': [
                i
            ]
        }
        logger.info('本次传入的城市ID为{}'.format(i))
        res = requests.post(url=url, json=json)
        assert res.status_code == 200
        res = res.json()
        assert res['success'] == 1  # 判断请求是否成功
        logger.info('获取城市门店列表成功')
        assert len(res['msg']['data']) == get_store_by_city(i)  # 判断返回的门店数量是否与数据库中的门店数量一致
        logger.info('用例通过')
    # 获取所有城市下的门店数量
    json = {
        'cityIds': id
    }
    logger.info('本次传入的城市ids:{}'.format(id))
    res = requests.post(url=url, json=json)
    assert res.status_code == 200
    from common.queries import get_all_store_by_city
    res = res.json()
    assert res['success'] == 1  # 判断请求是否成功
    assert len(res['msg']['data']) == get_all_store_by_city()  # 判断返回的门店数量与数据库中是否一致
    logger.info('用例通过')
