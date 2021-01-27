def dataToTest():
    data = {"date": "2030-03-06", "cityId": 330100000,
            "productGroup": [{"id": 5499, "people": 1, "num": 1, "services": [{"id": 5501, "people": 1, "num": 1}]}]}
    '''默认返回的城市Id为杭州'''
    return data
data = dataToTest()
print(data)
import datetime
data['productGroup'][0]['people'] = 10000
print(data)
import time
yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
data['date'] = yesterday[0:10]
print(data)
print(yesterday)
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
print(tomorrow)
H = int(datetime.datetime.now().strftime("%H"))
if H > 22:
    print(1)