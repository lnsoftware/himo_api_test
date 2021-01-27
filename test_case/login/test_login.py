from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
from common.queries import get_user_id
from common.get_X_Stream_Id import get_x_stream_id

'''
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
'''

caseName, casedata = GettingDate('登录.yml').return_data()  # GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('登录注册', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('登录注册')
@allure.story('登录')
@allure.title('登录_失败后停止')
@allure.severity('blocker')
def test_login():
    import requests
    '''
        通过读取登录.yml配置文件获取[url,username,password,brand,temp_token]
        result为断言内容
        仅判断最后返回的success是否一致
        params为入参
        '''
    for i in range(0, len(caseName)):
        url = casedata[i]['url']
        phone = casedata[i]['phone']
        password = casedata[i]['pass']
        brand = casedata[i]['brand']
        temp_token = casedata[i]['temp_token']
        result = casedata[i]['assert']
        params = {
            'phone': phone,
            'pass': password,
            'brand': brand,
            'temp_token': temp_token
        }
        try:  # 发起请求
            res = requests.get(url=url, params=params)
            logger.info('当前测试用例名称为：%s' % caseName[i])
            res = res.json()
        except:
            logger.error('用例{}执行失败'.format(caseName[i]))
            logger.error('请求失败,入参为{}'.format(params))
            logger.error(traceback.format_exc())
            raise TypeError('发起请求失败')
        try:
            assert result == res['success']  # 判断结果是否与预期一致
            if result == 1:  # 若判断登录结果为True,则查询x-stream-id是否为32位,通过数据库对比id查询是否存在此账号
                try:
                    id = get_x_stream_id(phone)
                    assert len(id['x-stream-id']) == 32
                    try:
                        get_user_id(phone)
                    except:
                        logger.error('获取用户ID失败,手机号为{}'.format(phone))
                        raise AssertionError
                except:
                    logger.error('获取到的x-stream-id有误,{}\n请求参数为{}'.format(get_x_stream_id(phone), params))
                    logger.error(traceback.format_exc())
                    raise AssertionError
            logger.info('用例{}通过'.format(caseName[i]))
        except:
            logger.error('用例{}执行失败'.format(caseName[i]))
            logger.error('请求失败,入参为{},返回的数据为{}'.format(params, res))
            logger.error(traceback.format_exc())
            raise AssertionError
