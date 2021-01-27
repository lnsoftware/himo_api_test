from common.db_utils import DBM, check_db_connect
from conf import DataBaseConfig as dbc


# 通过手机号获取用户id
def get_user_id(phone=13676561839):
    tb_name = dbc.himo_micro_user
    check_db_connect(tb_name)
    try:
        return DBM.query_one(tb_name, "select id from users where phone = '{}'".format(phone))['id']
    except:
        return 'Null'


# 通过用户id获取用户订单数量
def get_user_order(id):
    tb_name = dbc.new_himo_micro_order
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, "select * from orders where user_id='{}' and deleted_at is NULL".format(id)))


# 获取城市列表数量
def get_city_list():
    tb_name = dbc.himo_micro_store
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, "SELECT DISTINCT areas.id FROM areas,stores "
                                      "WHERE areas.id = stores.area_id and stores.deleted_at is NULL "))


# 获取城市ID
def get_city_id():
    tb_name = dbc.himo_micro_store
    check_db_connect(tb_name)
    id = DBM.query_all(tb_name, "select distinct areas.id from areas,stores where areas.id = stores.area_id"
                                " and stores.deleted_at is null ")
    list_id = []
    for i in range(len(id)):
        list_id.append(id[i]['id'])
    return list_id


# 通过城市ID获取对应城市下的门店数量(蓝标,金标)
def get_store_by_city(city_id):
    tb_name = dbc.himo_micro_store
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, "SELECT stores.id,stores.name from areas,stores "
                                      "where areas.id = stores.area_id and areas.id = {} and "
                                      "(stores.store_type = 'gold' or stores.store_type = 'blue') and "
                                      "stores.deleted_at is NULL".format(city_id)))


# 获取所有门店数量
def get_all_store_by_city() -> int:
    # def get_all_store_by_city(cityIds:list) -> int:
    tb_name = dbc.himo_micro_store
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, "select distinct stores.id from areas,stores where areas.id = stores.area_id and "
                                      "(stores.store_type = 'blue' or stores.store_type = 'gold') and stores.deleted_at is null"))


# 获取城市门店ID
def get_store_id(city_id):
    tb_name = dbc.himo_micro_store
    check_db_connect(tb_name)
    return DBM.query_all(tb_name, "SELECT stores.id from areas,stores "
                                  "where areas.id = stores.area_id and areas.id = {} and "
                                  "(stores.store_type = 'gold' or stores.store_type = 'blue') and "
                                  "stores.deleted_at is NULL".format(city_id))


# 通过用户手机号返回用户礼品卡余额
def get_user_gift_card_balance(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    return DBM.query_one(tb_name, "select SUM(balance) from user_gift_cards where status = 'used'"
                                  "and stop_usage > now() and user_id = {} and "
                                  "(give_status is null or give_status != 'giving') and "
                                  "deleted_at is null".format(id))['SUM(balance)']


# 获取用户x-stream-id
def get_x_stream_id(phone=13676561839, password=123456):
    url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/login/pass'
    data = {
        'phone': phone,
        'pass': password,
        'brand': 'mainto_app',
        'temp_token': ''
    }
    import requests
    res = requests.get(url=url, params=data)
    res = res.headers
    return {'x-stream-id': res['X-Stream-Id']}


# 获取用户app端内token
def get_token_by_xsid(phone=13676561839, password=123456):
    headers = get_x_stream_id(phone, password)
    params = {'brand': 'mantu_app', "deviceToken": get_userDevices()}
    url = 'https://mainto-app-1-0.local.hzmantu.com/user_auth/getTokenFromApp'
    import requests
    res = requests.get(url=url, headers=headers, params=params)
    res = res.json()
    return res['msg']


# 通过用户手机号获取返回用户未失效的体验券数量
def get_userProductCard_unused(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, 'select id from product_cards where status = "unused" '
                                      'and user_id = {} and stop_usage > now()'
                                      'and deleted_at is null and order_num is null'.format(id)))


# 通过用户手机号获取用户未失效的优惠券数量
def get_userVaildCoupons(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    return len(DBM.query_all(tb_name, f'SELECT * from coupons where user_id = {id} '
                                      f'and stop_usage > now() '
                                      f'and deleted_at is null and order_num is null'
                                      f' and apply_in="himo"'))
print(get_userVaildCoupons())

# 通过用户手机号返回用户所有产品卡信息
def get_userAllProductCard(phone=13676561839, status=None):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    status_list = ['unused', 'used', 'abolished', 'expired', 'activated', "inactivated"]
    if status is None:
        num = len(DBM.query_all(tb_name, "select id from product_cards where user_id = {} ".format(id)))
        if num == 0:
            return None
        return num
    elif status in status_list:
        num = len(DBM.query_all(tb_name, f"select id from product_cards where user_id = {id} and status = '{status}'"))
        if num == 0:
            return None
        return num
    else:
        return None


# 获取用户设备号
def get_userDevices(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.himo_micro_user_auth
    check_db_connect(tb_name)
    return DBM.query_one(tb_name, f"select device_token from user_devices where user_id = {id}")['device_token']


# 获取用户优惠券数量
def get_userCouponsInfo(phone=13676561839, status=None):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    status_list = ['unused', 'used', 'abolished', 'expired', 'activated']
    if status is None:
        num = len(DBM.query_all(tb_name, f"select * from coupons where user_id = {id} "
                                         f"and apply_in='himo' and deleted_at is null"))
        if num == 0:
            return None
        return num
    elif status in status_list:
        num = len(DBM.query_all(tb_name, f"select * from coupons where user_id = {id} and status = '{status}' "
                                         f"and apply_in='himo' and deleted_at is null"))
        if num == 0:
            return None
        return num
    else:
        return None


# 判断用户优惠券模板是否可用于门店下产品
def get_userUnusedCouponsAndProductCard(tempId=1625, storeId=1001, productId=8000):
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    result = DBM.query_one(tb_name, f"select * from coupon_templates where id = {tempId} "
                                    f"and JSON_CONTAINS(`limit`, '{productId}', '$.product_ids') "
                                    f"and JSON_CONTAINS(`limit`, '{storeId}','$.store_ids') ")
    if result is None:
        return False
    return True


# 删除用户春暖花开优惠券
def deleteUserSpringCoupons(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_preferential
    check_db_connect(tb_name)
    result = DBM.execute_one(tb_name, f'delete from coupons where user_id={id} and '
                                      f'(template_id=1448 or template_id=1449 or template_id=1450 or template_id=1451 '
                                      f'or template_id=1452 or template_id=1453 or template_id=1454 '
                                      f'or template_id=1455)')
    return result


# 获取用户信息
def get_user_info(phone=13676561839):
    id = get_user_id(phone)
    tb_name = dbc.himo_micro_user
    check_db_connect(tb_name)
    return DBM.query_one(tb_name, f"select * from users where id={id}")


# 获取用户开票历史
def get_user_invoice_history(phone=18888888888):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_order
    check_db_connect(tb_name)
    return len(
        DBM.query_all(tb_name, f'select * from orders where user_id={id} and '
                               f'deleted_at is null and invoice_id is not null')
    )


def get_user_invoice_list(phone=18888888888):
    id = get_user_id(phone)
    tb_name = dbc.new_himo_micro_order
    check_db_connect(tb_name)
    order_list = DBM.query_all(tb_name, f'select * from orders where user_id={id} and '
                                        f'deleted_at is null and invoice_id is null and status="finished"')

    # return order_list

    def real_money():
        money_list = []
        for li in order_list:
            money_list.append(DBM.query_all(tb_name, f'select * from sub_orders where order_id={li["id"]}'))

        return money_list

    money_list = real_money()

    def money_is_not_zero():
        invoice_list = []
        for i in range(len(money_list)):
            for li in money_list[i]:
                if li['real_money'] > 0.00:
                    invoice_list.append(li)
                    '''
                    if li['gift_card_paymen_no']is None:
                            invoice_list.append(li)
                    else:
                        gcp = li['gift_card_paymen_no']
                        db_name = dbc.new_himo_micro_preferential
                        check_db_connect(db_name)
                        id = DBM.query_one(db_name, f"select * from gift_card_payments where payment_no={gcp}")["id"]
                        card_id = DBM.query_one(db_name, f"select * from gift_card_payment_items where payment_id={id}")
                        undetermined = DBM.query_one(db_name, f"select * from user_gift_cards where id={card_id['card_id']}")
                        if undetermined['refund_id'] != None:
                            '''
        return invoice_list

    invoice_list = money_is_not_zero()
    if len(invoice_list) < 1:
        return None
    return invoice_list


# 获取产品信息
def get_product_info(product_id: list):
    db_name = dbc.new_himo_micro_product_v3
    check_db_connect(db_name)
    if len(product_id) == 1:
        return DBM.query_one(db_name, f"select * from products where id={product_id[0]} "
                                      f"and deleted_at is null")
    elif len(product_id) > 1:
        product_list = []
        for i in range(len(product_id)):
            product_list.append(DBM.query_one(db_name, f"select * from products where id={product_id[i]}"
                                                       f" and deleted_at is null"))
        return product_list
    else:
        return None


# 获取类目id下的商品详情数
def get_product_category_by_store_id_and_cat_id(cat_id, store_id=1001):
    db_name = dbc.new_himo_micro_product
    check_db_connect(db_name)
    category = DBM.query_all(db_name,
                             f"select * from products where category_id={cat_id} and c_hidden=0 and is_entity=0")
    # return category
    for i in category:
        if DBM.query_one(db_name,
                         f"select * from product_store where product_id={i['id']} and store_id={store_id}") is None:
            return None
    return category


# 通过门店id获取对应的优惠及分组id
def get_area_classification_id(store_id):
    db_name = dbc.himo_micro_store
    check_db_connect(db_name)
    area_dict = {"area_id": [], "num": []}
    area = (DBM.query_all(db_name, f"select * from area_classification_store "
                                   f"where store_id={store_id}"))
    for a in area:
        area_dict["area_id"].append(a['area_classification_id'])

    tb_name = dbc.new_himo_micro_product_v3
    check_db_connect(tb_name)
    for i in area_dict['area_id']:
        area = DBM.query_all(tb_name,
                             f"select * from discount_rules where store_classification_id={i} "
                             f"and deleted_at is null")
        for a in area:
            if a:
                area_dict['num'].append(a)

    return area_dict


if __name__ == '__main__':
    # print(get_product_category_by_store_id_and_cat_id(5839, 1001))
    print(get_user_invoice_list(17107769767))
