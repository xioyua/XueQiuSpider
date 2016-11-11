import urllib
import urllib.error
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup
import re
import lxml
import MySQLdb
from MySql import XueQiuSql
import time
import gzip

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

def getOpener(head):
    # deal with the Cookies
    pass


def getOpener2():
    pass

def openURL(url):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    acceptE = "gzip, deflate, br"
    acceptL = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    connection = "keep-alive"
    host = "xueqiu.com"
    upgrade = "1"
    headers = {'User-Agent': user_agent,
               'Accept': accept,
               'Accept-Encoding': acceptE,
               'Accept-Language': acceptL,
               'Connection': connection,
               'Host': host,
               'Upgrade-Insecure-Requests': upgrade
               }
    header = []
    for key, value in headers.items():
        elem = (key, value)
        header.append(elem)
    print(header)


    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.addheaders = header

    try:
        response = opener.open(url)
        page = response.read()
        data = ungzip(page).decode()
        # print(page)
    except urllib.error.URLError as e:
        print(e.code, ':', e.reason)

    cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
    print(cookie)
    for item in cookie:
        print('Name = ' + item.name)
        print('Value = ' + item.value)
    return data

url = "https://xueqiu.com/2431057144"
data = openURL(url)
url = "https://xueqiu.com/friendships/groups/members.json?page=1&uid=2431057144&gid=0&_=1476324083653"
data = openURL(url)
print(data)
