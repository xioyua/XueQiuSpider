#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

SVNAME = "localhost"
SVUSER = "root"
SVPAWD = "1234321xy"
DBNAME = "TESTDB"
class XueQiuSql():
    '''专用于雪球的数据库方法类'''
    login = ()
    def __init__(self):
        '''检查，如果没有XUEQIU数据库，则建立一个'''
        try:
            db = MySQLdb.connect(SVNAME,SVUSER,SVPAWD,DBNAME,charset="utf8")
            cursor = db.cursor()
            # 创建数据表SQL语句
            sql = """CREATE TABLE IF NOT EXISTS TESTDB.XUEQIU (
                    FIRST_NAME  VARCHAR(40) NOT NULL,
                    ADDR CHAR(20) PRIMARY KEY NOT NULL,
                    GAIN INT
                    )"""
            cursor.execute(sql)
            sql = """CREATE TABLE IF NOT EXISTS TESTDB.READSP (
                                SP  INT NOT NULL,
                                CHANGEDATE DATE  NOT NULL
                                )"""
            cursor.execute(sql)
            #text = cursor.fetchall()
        except MySQLdb.MySQLError as e:
            print(e);
        #print(text)
        db.close()

    def addPlayer(self,players):
        '''把收集到的用户名和网址存储'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        for each in players:
            try:
                sql = "INSERT IGNORE INTO XUEQIU(FIRST_NAME,ADDR)\
                       VALUES (%s, %s)"
                # 执行sql语句
                n = cursor.execute(sql,(each[0],each[1]))
                # 提交到数据库执行
                db.commit()
            except :
                # Rollback in case there is any error
                print("有错误，rollback")
                db.rollback()
        # 关闭数据库连接
        db.close()

    def showTable(self):
        '''显示数据库中所有信息'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM XUEQIU "
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                fname = row[0]
                addr = row[1]
                # 打印结果
                print("fname=%s,addr=%s" % \
                      (fname, addr))
        except:
            print("Error: unable to fecth data")
        db.close()

    def clearDB(self):
        '''清除雪球表的数据'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        sql ="DELETE FROM XUEQIU "
        n = cursor.execute(sql)
        print(n)
        db.commit()
        db.close()

    def initSP(self,):
        '''初始化READSP数据库，将SP设为1'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        sql = "DELETE FROM READSP"
        n = cursor.execute(sql)
        sql = "INSERT INTO READSP(SP,CHANGEDATE) VALUES(0,CURRENT_DATE)"
        n = cursor.execute(sql)
        db.commit()
        db.close()

    def getSP(self):
        '''得到sp的数值'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        sql = "SELECT SP FROM READSP"
        n = cursor.execute(sql)
        sp = cursor.fetchone()
        if sp!=None:
            sp = sp[0]
        else:
            n = cursor.execute("INSERT INTO XUEQIU(SP,CHANGEDATE) VALUES(0,CURRENT_DATE)")
            sp = 0
        db.close()
        return sp

    def getTotalOfRoles(self):
        '''得到sp的数值'''
        db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        cursor = db.cursor()
        sql = "SELECT COUNT(*) FROM XUEQIU"
        try:
            n = cursor.execute(sql)
            tatol = cursor.fetchone()
            ta = tatol[0]
            db.close()
            return ta
        except:
            db.rollback()
            db.close()

    def gConnectDB(self):
        '''建立一个外部可以操作的数据连接'''
        self.db = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        self.cursor = self.db.cursor()

    def gConnectDB2(self):
        '''建立一个外部可以操作的数据连接'''
        self.db2 = MySQLdb.connect(SVNAME, SVUSER, SVPAWD, DBNAME, charset="utf8")
        self.cursor2 = self.db2.cursor()


    def gExcuteCmd(self, sql, repeatParam=None, commit = 0):
        '''执行命令'''
        try:
            if not repeatParam:
                n = self.cursor.execute(sql)
            else:
                n = self.cursor.executemany(sql, repeatParam)
            if commit:
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("数据库执行有错误")
            print(e)

    def gExcuteCmd2(self, sql, repeatParam=None, commit = 0):
        '''执行命令'''
        try:
            if not repeatParam:
                n = self.cursor2.execute(sql)
            else:
                n = self.cursor2.executemany(sql, repeatParam)
            if commit:
                self.db2.commit()
        except Exception as e:
            self.db2.rollback()
            print("数据库执行有错误")
            print(e)


    def gScroll(self,num):
        '''移动指针'''
        self.cursor.scroll(num,mode='absolute')

    def gScroll2(self,num):
        '''移动指针'''
        self.cursor2.scroll(num,mode='absolute')

    def gFetch(self,num=0):
        if num==0:
            results = self.cursor.fetchall()
        elif num==1:
            results = self.cursor.fetchone()
        elif num>1:
            results = self.cursor.fetchmany(num)
        else :
            print("参数设置错误")
            results = None
        return results

    def gFetch2(self,num=0):
        if num==0:
            results = self.cursor2.fetchall()
        elif num==1:
            results = self.cursor2.fetchone()
        elif num>1:
            results = self.cursor2.fetchmany(num)
        else :
            print("参数设置错误")
            results = None
        return results

    def gCloseDB(self):
        self.db.close()

    def gCloseDB(self):
        self.db2.close()



c = XueQiuSql()




