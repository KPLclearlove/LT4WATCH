import  requests
url = 'https://club.m.autohome.com.cn/frontapi/getUserInfoByIds'
param = {
    'userids': '247301085'
}
resp = requests.get(url, params= param)
print(resp.status_code)
print(resp.content.decode("utf-8"))