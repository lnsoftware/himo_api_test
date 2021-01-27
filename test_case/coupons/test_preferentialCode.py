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

caseName, casedata = GettingDate(
    'preferentialCode.yml').return_data()  # GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('优惠券信息', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@feature('优惠券信息')
@title('用户绑定优惠券')
def test_preferentialCard():
    '''
    headers = {'x-stream-id':}
    json 为传参
    '''
    import requests
    from common.get_X_Stream_Id import get_x_stream_id
    headers = get_x_stream_id()
    for i in range(1, len(caseName)):
        preferentialCode = casedata[i]['preferentialCode']  # 获取参数
        result = casedata[i]['assert']  # 验证结果是否一致
        json = {
            'preferentialCode': preferentialCode
        }
        res = requests.post(url=casedata[0], json=json, headers=headers)
        logger.info('{}'.format(caseName[i]))  # 记录当前用例名
        res = res.json()
        logger.info('返回信息{}'.format(res))
        try:
            assert res['success'] == result
            logger.info('{}通过'.format(caseName[i]))
        except:
            logger.error('{}失败,入参为{}'.format(caseName[i], json))
            raise AssertionError
