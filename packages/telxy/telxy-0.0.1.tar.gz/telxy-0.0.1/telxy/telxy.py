import urllib.request
import urllib.parse
import json
APPKEY='631c5a5b9992bd74'
APPSECRET='eS0iNTaMdI5mgRew8JkrVqUB7mG1MytS'
API_URL='http://api.jisuapi.com/shouji/query'

def get_tel_info(tel=''):
    data = {}
    data['appkey'] = APPKEY
    data['shouji'] = tel
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr = json.loads(result.read())
    return jsonarr['result']
