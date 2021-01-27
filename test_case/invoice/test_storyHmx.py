from common.readYaml import GettingDate
from common.assert_result import *
from common.logger import Logger
import traceback, logging, allure
from common.queries import *
from conf import Api_Url as c
from httpRequests._requests import *

"""
测试用例模板
不需读取用例文件的脚本将caseName,casedata行删除即可
Looger('')中的传参控制生成的日志文件名
FileLevel控制写入日志文件的日志等级
"""

# caseName, casedata = GettingDate('.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('电子发票', FileLevel=logging.INFO).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名


@allure.feature('电子发票')
@allure.story('开票主题门店')
@allure.severity('normal')
class Test_storyHmx:
    """
    测试手机号为隐形个人手机号，
    后期若需要更换账号进行测试只需要更改phone= 和 password=
    result是对返回的success进行断言，1为True， 0为False
    目前用例内需要准备url和参数
    noToken的请求是不带x-stream-id 非Token
    """

    def setup(self):
        self.url = c.release + c.invoiceHmx
        self.hmx = {
    "saletaxnums": {
      "91330104MA2AY90E4G": [
        1067
      ],
      "91130104MA0CP6AM40": [
        1145
      ],
      "91460100MA5T6JQN01": [
        1142
      ],
      "91330101MA2CFJJD26": [
        1001,
        1002,
        1004,
        1019,
        1074,
        1079,
        1095,
        1101,
        1159,
        1160,
        1190
      ],
      "91350503MA31XBAP1D": [
        1024
      ],
      "92130102MA090M7BXL": [
        1028
      ],
      "92220201MA1545L613": [
        1029
      ],
      "92330802MA2FRB0G25": [
        1031
      ]
    },
    "manual": [
      1067,
      1145,
      1142
    ],
    "hmx": "91330101MA2CFJJD26"
  }

    @allure.title('获取可开取主题发票门店')
    def test_get_invoice_hmx(self):
        logger.info('获取可开取主题发票门店')
        res = http_get(self.url)
        if check_result(res['msg'], self.hmx, logger) == 0:
            raise AssertionError(traceback.format_exc())

    @allure.title('不带x-stream-id获取可开取主题发票门店')
    def test_get_invoice_hmx_not_x_stream_id(self):
        logger.info('不带x-stream-id获取可开取主题发票门店')
        res = http_get_noToken(self.url)
        if check_result(res['msg'], self.hmx, logger) == 0:
            raise AssertionError(traceback.format_exc())