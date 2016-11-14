import urllib
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import re
import lxml
import sys
import os
from MySql import XueQiuSql
import time
import myCookieGhost
import gzip
import json
import traceback
from tqdm import tqdm


class XueQiuSpider:
    '''专为爬雪球所打包的类'''

    def __init__(self):
        '''设置头，cookie'''
        self.Datab = XueQiuSql()
        self.players = []
        self.opener = urllib.request.build_opener()
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
        print(header)
        self.opener.addheaders = header
        # 得到cookie
        cookie = myCookieGhost.Cookie('https://xueqiu.com/2431057144').getCookie()
        # 在opener中加入cookie
        self.opener.addheaders.append(('Cookie', cookie))

    def restart_program(self):
        '''重启本程序'''
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def getRoleFirst(self):
        '''从people页面获得第一批用户信息，通过扫描关注列表，得到大量用户信息'''
        url = "https://xueqiu.com/people"
        try:
            request = urllib.request.Request(url)
            response = self.opener.open(url)
            html = response.read()
            html = self.ungzip(html)
            # print (html)
            soup = BeautifulSoup(html, 'lxml')
        except urllib.error.URLError as e:
            print("有错误")
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        # 从人物搜索页面上获得要存储的信息
        for tag in soup.find_all('a', href=re.compile("^/(?!(people))"), target="_blank", class_="name"):
            # 得到href地址
            href = tag.get("href")
            # 得到该人物的首页地址
            url2 = "https://xueqiu.com" + href
            # 得到该人物的userid
            id = self.getUserId(url2)
            # 存储userid
            player = [tag.get("data-name"), id]
            # 进行延迟，防止阅览网页过快被封禁
            time.sleep(0.2)
            self.players.append(player)
        # 存储到数据库
        self.Datab.addPlayer(self.players)
        # self.Datab.showTable()
        print(self.players)
        #获得所有关注对象
        self.getRoleFromList(self.players, 3)

    def getUserId(self, url):
        '''通过用户链接得到用户ID'''
        response = self.opener.open(url)
        html = response.read()
        html = self.ungzip(html)
        # print (html)
        soup = BeautifulSoup(html, 'lxml')
        tag = soup.find('a', class_="setRemark")
        id = tag.get("data-user-id")
        match = re.match(r'\d+', id)
        if match:
            return id
        else:
            print("没有抓取到id")
            return None

    def getRoleFromList(self, roleList, iterationNum):
        '''将传递列表中的所有角色的关注对象存储'''
        # 遍历每一个角色
        for role in roleList:
            # getAllAttentionList(role,3)
            print(role)
            self.getAllAttentionList(role[0], role[1], 1)

    def getAllAttentionList(self, name, addr, iterationNum):
        '''用递归穷举所有关注对象'''
        # 获得该角色的关注列表
        players = self.getAttentionList(name, addr)
        print(players)
        # 存储该角色的关注列表
        self.Datab.addPlayer(players)
        # 如果迭代层数未达到，则继续获得该关注列表中所有角色的关注列表
        if (iterationNum > 0):
            for role in players:
                print(role)
                self.getAllAttentionList(role[0], role[1], iterationNum - 1)
        else:
            if (iterationNum == 0):
                print("One Finish")

    def getAttentionList(self, name, addr):
        '''得到关注列表'''
        roles = []
        uid = addr;
        page = 1
        while True:
            url = "https://xueqiu.com/friendships/groups/members.json?page=" + str(
                page) + "&uid=" + uid + "&gid=0&_=1476323849724"
            print(url)
            try:
                # 打开关注网页
                response = self.opener.open(url)
                data = response.read()
                data = self.ungzip(data)
                # 找到页码信息
                pa_page = re.compile(r'"maxPage":(\d+)')
                maxpage = pa_page.findall(data)[0]
                maxpage = int(maxpage)
                # 找到关注信息
                pn_name = re.compile(r'"screen_name":"(.+?)",')
                pn_id = re.compile(r'"id":(\d+?),')
                allname = pn_name.findall(data)
                allid = pn_id.findall(data)
                #如果找到匹配信息，则把name列表和id列表匹配
                if pn_name:
                    for (name, id) in zip(allname, allid):
                        player = [name, id]
                        roles.append(player)
                else:
                    print("没匹配到")
                # 延迟
                time.sleep(0.2)
                # 返回roles
                if maxpage <= page:
                    return roles
                else:
                    page = page + 1
            except urllib.error as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)

    def ungzip(self, data):
        try:  # 尝试解压
            data = gzip.decompress(data).decode()
        except:
            print('未经压缩, 无需解压')
        return data

    def getRoleCharacter(self,iscontinue = True):
        '''从用户信息库中取出用户ID,并通过id得到用户的组合信息'''
        process = 0
        if(iscontinue == True):
            sp = self.Datab.getSP()
            print(sp)
        else:
            sp = 0

        totalofRoles = self.Datab.getTotalOfRoles()
        print(totalofRoles)
        bar = tqdm(initial=sp,total = totalofRoles)
        try:
            # 连接数据库
            self.Datab.gConnectDB()
            self.Datab.gConnectDB2()
            # 得到雪球库数据
            self.Datab.gExcuteCmd2("SELECT * FROM XUEQIU WHERE (SELECT COUNT(1) AS NUM FROM XUEQIU_GROUP WHERE XUEQIU.ADDR = XUEQIU_GROUP.USERID) = 0")
            # 移动指针
            self.Datab.gScroll2(sp)
            while True:

                #取出50个数据
                roles = self.Datab.gFetch2(50)
                #遍历这50个用户数据
                for role in roles:
                    #取出用户id
                    id = role[1]
                    #得到用户股票组合的总收益和组合信息
                    totalgain, ZH = self.dealRoleInfo(id)
                    self.Datab.gExcuteCmd("UPDATE XUEQIU SET GAIN = %s WHERE ADDR = %s " % (totalgain, id), commit=1)
                    bar.update(1)
                    if ZH:
                        self.Datab.gExcuteCmd(
                            "REPLACE INTO XUEQIU_GROUP(USERID,GROUPNAME,GAIN,SYMBOL,CREATE_TIME,UPDATE_TIME) VALUES(%s,%s,%s,%s,%s,%s)" \
                            , repeatParam=ZH, commit=1)

                # 过程计数
                length = len(roles)
                sp = sp + length
                process = process + length

                #移动工作指针
                self.Datab.gExcuteCmd("UPDATE READSP SET SP = %s,CHANGEDATE = CURRENT_DATE " % sp, commit=1)
                if length < 50:
                    print("完成,共完成%d位用户" % process )
                    break
            # 断开数据库
            self.Datab.gCloseDB2()
            self.Datab.gCloseDB()
        except SystemExit:
            self.Datab.gCloseDB()
            self.Datab.gCloseDB2()
            print("中途退出，断开数据库连接")
            print("本次完成了%d个用户数据" % process)
        except :
            self.Datab.gCloseDB()
            self.Datab.gCloseDB2()
            print("出现错误，断开数据库连接")
            print("本次完成了%d个用户数据" % process)
            traceback.print_exc()
            print("10s后重启程序")
            time.sleep(10)
            self.restart_program()

    exceptionNum = 0
    def dealRoleInfo(self,id):
        '''提取用户的组合json信息，返回这个用户的组合信息'''
        url = "https://xueqiu.com/cubes/list.json?user_id="+id+"&_=0"
        #url =  'https://xueqiu.com/cubes/list.json?user_id=6205861642&_=0'
        #连接网站读取信息
        try:
            response = self.opener.open(url)
            data = response.read()
        except urllib.request.HTTPError as e:
            print(e)
            print("读取网页有错误，2S后重启程序")
            time.sleep(2)
            self.restart_program()
        time.sleep(0.1)     #避免采集太频繁的延迟
        try:
            data = data.decode()
            dataj = json.loads(data)
        except:
            print(data)
            print("读取json出现错误，跳过吧")
            self.exceptionNum+=1
            print("共产生错误",self.exceptionNum)
            print("10s后重启程序")
            traceback.print_exc()
            time.sleep(10)
            self.restart_program()
        #print("页面读取完毕")
        count = dataj['totalCount']  # 持有组合数 count
        totalgain = 0
        # 如果组合数不为0,各组合信息
        if count > 0:
            #print('count:', count)
            name = []
            gain = []
            symbol = []
            updatetime = []
            createtime = []
            #遍历组合
            for each in dataj['list']:
                name.append(each['name'])
                gain.append(each['total_gain'])
                symbol.append(each['symbol'])
                updatetime.append(each['updated_at'])
                createtime.append(each["created_at"])

            totalgain = sum(gain)  #得到所有组合总收益
            #print(totalgain)
            roles = []
            # 把所有表中的信息意义匹配,并放入roles总列表中
            # 把组合信息的名称、收益、标志、更新时间、建立时间存储
            for (n, g, s, u, c) in zip(name, gain, symbol, updatetime, createtime):
                role = [id,n, float(g), s, u, c]
                roles.append(role)
            return totalgain, roles
        else:
            return totalgain,None




ms = XueQiuSpider()
ms.getRoleCharacter(iscontinue=True)
