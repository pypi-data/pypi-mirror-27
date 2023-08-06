import urllib.request
import urllib.parse
import json
APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/car/brand'

def carslist():
    data = {}
    data['appkey'] = APPKEY
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    if jsonarr['status'] != '0':
        print(jsonarr['msg'])
        exit()
    result = jsonarr['result']
    cars = []
    for val in result:
        cars.append(val['name'])
        cars.append(val['initial'])
        cars.append(val['logo'])
    return cars
