from common.readYaml import GettingDate
from common.logger import Logger
import logging
import requests
from common.get_X_Stream_Id import get_x_stream_id
from common.order.getOrderList import orderList
'''
测试用例模板
'''

caseName, casedata = GettingDate('delete_order.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
# logger = Logger('删除订单', FileLevel=logging.ERROR).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名

def deleteOrder(length=1,headers=None):
    headers = {
        'x-stream-id':headers
    }
    orderList(headers)







if __name__ == '__main__':
    for i in range(0,len(caseName)):
        headers = get_x_stream_id()             #获取用户的x-stream-id
        url = casedata[i]['url']
        orderNum = orderList()                  #获取用户的订单列表
        if len(orderNum) == 1:
            data = {
                'orderNum':orderNum
            }
            print('删除的订单号：%s'%orderNum)
            res = requests.delete(url=url,json=data,headers=headers)        #传入订单号进行删除
            if res.status_code == 200:
                print(res.json())                                           #打印成功信息
            else:
                print(res.json())                                           #打印失败信息
        elif len(orderNum) > 1:
            for i in range(0,len(orderNum)):
                data = {
                    'orderNum':orderNum[i]
                }
                print('删除的订单号：%s'%orderNum[i])
                res = requests.delete(url=url,params=data,headers=headers)
                if res.status_code == 200:
                    print(res.json())
                else:
                    print(res.status_code)
                    print(res.json())
        else:
            print('delete over')
