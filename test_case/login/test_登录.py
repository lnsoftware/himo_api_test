import requests
import pytest
import logging
import allure
import traceback
from common.readYaml import GettingDate
from common.logger import Logger
from common.queries import *

caseName, casedata = GettingDate('登录.yml').return_data()
logger = Logger('登录注册', FileLevel=logging.INFO, CmdLevel=logging.INFO).getlog()


@allure.feature('登录注册')
@allure.story('登录')
@allure.title('登录_失败后继续')
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
            logger.info('当前传入参数为{}'.format(params))
            res = res.json()
        except:
            logger.error('用例{}执行失败'.format(caseName[i]))
            logger.error('请求失败,入参为{}'.format(params))
            logger.error(traceback.format_exc())
        try:
            assert result == res['success']  # 判断结果是否与预期一致
            if result == 1:  # 若判断登录结果为True,则查询x-stream-id是否为32位,通过数据库对比id查询是否存在此账号
                try:
                    from common.get_X_Stream_Id import get_x_stream_id
                    id = get_x_stream_id(phone)
                    assert len(id['x-stream-id']) == 32
                    try:
                        get_user_id(phone)
                    except:
                        logger.error('获取用户ID失败,手机号为{}'.format(phone))
                except:
                    logger.error('获取到的x-stream-id有误,{}\n请求参数为{}'.format(get_x_stream_id(phone), params))
                    logger.error(traceback.format_exc())
            logger.info('用例{}通过'.format(caseName[i]))
        except:
            logger.error('用例{}执行失败'.format(caseName[i]))
            logger.error('请求失败,入参为{},返回的数据为{}'.format(params, res))
            logger.error(traceback.format_exc())
