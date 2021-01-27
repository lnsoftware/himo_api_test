from common.queries import *


# 常用post请求,仅判断返回信息中的success是否与预期一致
def _requests_post(url, result, json=None, headers=None):
    """
    :param url:  Api地址
    :param headers:  x-stream-id等请求头
    :param result:  断言结果
    :param json:  json参数,不传为空
    :return: res.json()
    """
    import requests
    res = requests.post(url=url, headers=headers, json=json)
    res = res.json()
    try:
        assert res['success'] == result
        return res
    except:
        import traceback
        print(res)
        print(traceback.format_exc())
        raise AssertionError


# 常用get请求,仅判断返回信息中的success是否与预期一致
def _requests_get(url, result, headers=None, params=None):
    """
    :param url:  Api地址
    :param headers:  x-stream-id等请求头
    :param result:  断言结果
    :param params:  params参数,不传为空
    :return: res.json()
    """
    import requests
    res = requests.get(url=url, headers=headers, params=params)
    res = res.json()
    try:
        assert res['success'] == result
        return res
    except:
        import traceback
        print(res)
        print(traceback.format_exc())
        raise AssertionError


def http_get(url, phone=13676561839, password=123456, result=1, params=None):
    """
    此处为判断get请求是否带有参数
    """
    if params:
        headers = get_x_stream_id(phone=phone, password=password)
        res = _requests_get(url=url, headers=headers, result=result, params=params)
        return res
    else:
        headers = get_x_stream_id(phone=phone, password=password)
        res = _requests_get(url=url, headers=headers, result=result)
        return res


def http_post(url, phone=13676561839, password=123456, result=1, json=None):
    """
    此处判断post请求是否带有json参数
    """
    if json is None:
        headers = get_x_stream_id(phone=phone, password=password)
        res = _requests_post(url=url, headers=headers, result=result)
        return res
    else:
        headers = get_x_stream_id(phone=phone, password=password)
        res = _requests_post(url=url, headers=headers, result=result, json=json)
        return res


def http_get_noToken(url, result=1, params=None):
    """
    此处为判断get请求是否带有参数
    """
    if params:
        res = _requests_get(url=url, result=result, params=params)
        return res
    else:
        res = _requests_get(url=url, result=result)
        return res


def http_post_noToken(url, result=1, json=None):
    """
    此处为判断post请求是否带有参数
    """
    if json:
        res = _requests_post(url=url, result=result, json=json)
        return res
    else:
        res = _requests_post(url=url, result=result)
        return res


if __name__ == '__main__':
    _params = {
        'storeId': 1051
    }
    _res = _requests_get(params=_params,
                         url='https://mainto-app-1-0.local.hzmantu.com/project_mainto_app/store/getStoreInfoById/v1',
                         result=1)
    print(_res)
