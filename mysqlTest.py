import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)


db = MySQLdb.connect("localhost", "root", "1234321xy", "TESTDB",charset="utf8")
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT * FROM XUEQIU "
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    for n in range(2):
        print("这是第%d次：" %n)
        results = cursor.fetchmany(50)
        print(len(results))
        for row in results:
            fname = row[0]
            addr = row[1]
            # 打印结果
            print("fname=%s,addr=%s" % \
                      (fname, addr))
except:
    print("Error: unable to fecth data")
db.close()

