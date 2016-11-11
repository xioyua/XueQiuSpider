import urllib
import http.cookiejar
import gzip
import myCookieGhost
import re
import json
import time

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

opener = urllib.request.build_opener()
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
connection = "keep-alive"
host = "xueqiu.com"
upgrade = "1"
headers = {'User-Agent': user_agent,
            'Accept': accept,
            'Connection': connection,
            'Host': host,
            'Upgrade-Insecure-Requests': upgrade
            }
header = []
for key, value in headers.items():
    elem = (key, value)
    header.append(elem)
print("开始")
opener.addheaders = header
cookie = myCookieGhost.Cookie('https://xueqiu.com/2431057144').getCookie()
print("cookie获取完毕")
opener.addheaders.append(('Cookie',cookie))
response = opener.open("https://xueqiu.com/cubes/list.json?user_id=5842900570&_=0")
data = response.read()
#data = ungzip(data)
data = data.decode()
data = json.loads(data)
print("页面读取完毕")

#持有组合数 count
count = data['totalCount']
#各组合信息
if count>0:
    print('count:' ,count)
    name = []
    gain=[]
    symbol = []
    updatetime = []
    createtime = []
    for each in data['list']:
        name.append(each['name'])
        gain.append(each['total_gain'])
        symbol.append(each['symbol'])
        updatetime.append(each['updated_at'])
        createtime.append(each["created_at"])
    # 得到所有组合总收益
    totalgain = sum(gain)
    print(totalgain)
    roles = []
    # 把所有表中的信息意义匹配,并放入roles总列表中
    # 把组合信息的名称、收益、标志、更新时间、建立时间存储
    for (n, g, s, u, c) in zip(name, gain, symbol, updatetime, createtime):
        role = [n, float(g), s, int(u), int(c)]
        roles.append(role)
    print(roles)








