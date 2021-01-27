from common.readYaml import GettingDate
from common.logger import Logger
import traceback
import logging
import allure
import requests
from common.get_X_Stream_Id import get_x_stream_id

'''
测试用例模板
'''

caseName, casedata = GettingDate('getOrderList.yml').return_data()  #GettingDate中输入yml配置文件名，可读取文件中数据，返回两组数据（用例标题，用例数据）
logger = Logger('获取列表', FileLevel=logging.ERROR).getlog()  # FileLevel设置写入log日志中的等级，第一个参数是生成的日志文件名

def orderList(phone=13676561839,password=123456):
    #获取 x-stream-id
    id = get_x_stream_id(phone,password)
    logger.info('获取的x-stream-id为：%s' %id)
    for i in range(0,len(caseName)):
        url = casedata[i]['url']            #获取请求地址
        logger.info('获取到的请求url:%s'%url)
        data = casedata[i]['data']          #获取请求数据
        logger.info('获取到的请求参数:%s'%data)
        res = requests.post(url=url,json=data,headers=id)       #获取用户所有订单列表
        if res.status_code ==200:
            res = res.json()
            logger.info('获取订单列表成功',res)
            try:
                total = res['msg']['total']     #总订单数量
                logger.info('总订单数量为：%s'%total)
                data = res['msg']['data']       #订单列表
                logger.info('所有订单信息:%s'%data)
                if total == 0:                  #如果订单总数为0则返回-1
                    return -1
                elif total == 1:                #订单数量为1返回单个订单号
                    data = data[0]['order_no']
                    logger.info('订单号：%s'%data)
                    return data
                else:                           #订单大于1返回订单号列表
                    order_list = []
                    for i in range (0,total):
                        order_list.append(data[i]['order_no'])
                    return order_list
            except Exception as ex:
                logger.error('失败原因：',traceback.format_exc())
        else:
            logger.error('请求失败',traceback.format_exc())
            raise Exception



if __name__ == '__main__':
    # data = orderList()
    # print(data)

    for i in range(0,len(caseName)):
        url = casedata[i]['url']
        data = casedata[i]['data']
        id = get_x_stream_id(phone=13676564148,password=1234567)
        res = requests.post(url=url,json=data,headers=id)
        res = res.json()

        print(res['msg'])
        print(res['msg']['data'])
        for i in res['msg']['data']:
            if i['status'] !='wait_shooting' and i['status'] != 'closed_by_refund':
                print(i)


        '''
        try:
            total = res['msg']['total']     #总订单数量
        except Exception as ex:
            print(ex)
        # print(res['msg']['data'])
        data = res['msg']['data']       #订单列表
        if total == 1:
            data = data[0]['order_no']
            print(data)
            # return data
        else:
            order_list = []
            for i in range (0,total):
                order_list.append(data[i]['order_no'])
                # return order_list
    print(order_list)
'''
