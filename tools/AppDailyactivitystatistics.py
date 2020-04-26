import cx_Oracle  # 导入包
import datetime
# from pyecharts import Bar, Line, EffectScatter, Overlap, Map, Geo
import pandas as pd


def getyesterday(i):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=i)
    yesterday = today - oneday
    return yesterday


def appusercount(con):
    rlt = []
    for i in range(0, 163):
        # 连接数据库
        cur = con.cursor()  # 游标操作
        sql = "select  to_char(sysdate - "+str(i)+", 'yyyy-mm-dd') as days,  count(b.userid)  from  (select a.userid ,sum(a.access_count) from ( select b.userid, b.code, b.access_date, count(1) as access_count from t_app_access_list b " + "where b.access_date = to_char(sysdate - " + str(
            i) + ", 'yyyy-mm-dd') group by b.userid, b.access_date, b.code ) a where a.code='login' group by a.userid) b"
        cur.execute(sql)  # 执行sql语句
        rows = cur.fetchall()  # 获取数据
        # 打印数据
        count = 0
        for row in rows:
            count += row[1]
            # print("用户ID:"+str(row[0])+"访问总数:"+str(row[1]))
        # yesterday = getYesterday(i)
        print(str(row[0]) + "访问总数：" + str(count))
        rlt.append(str(row[0]) + "," + str(count))
    result = pd.DataFrame(rlt)
    # 把查询结果写入csv
    result.to_csv('../data/app日用户数统计.csv', mode='a', header=True)


def logincount(con):
    rlt = []
    for i in range(0, 163):
        # 连接数据库
        cur = con.cursor()  # 游标操作
        sql = "select  to_char(sysdate - "+str(i)+", 'yyyy-mm-dd') as days,  sum(counts)  from  (select a.userid ,sum(a.access_count) as counts from ( select b.userid, b.code, b.access_date, count(1) as access_count from t_app_access_list b " + "where b.access_date = to_char(sysdate - " + str(
            i) + ", 'yyyy-mm-dd') group by b.userid, b.access_date, b.code ) a where a.code='login' group by a.userid) b"
        cur.execute(sql)  # 执行sql语句
        rows = cur.fetchall()  # 获取数据
        # 打印数据
        count = 0
        for row in rows:
            if row[1] is not None:
                count += row[1]
        print(str(row[0]) + "访问总数：" + str(count))
        rlt.append(str(row[0]) + "," + str(count))
    result = pd.DataFrame(rlt)
    # 把查询结果写入csv
    result.to_csv('../data/app日登录数统计.csv', mode='a', header=True)


if __name__ == '__main__':
    db = cx_Oracle.connect("cherymon/1q@W3e$R@tlmsrac.mychery.com:1521/cheryddc_taf")
    # db = cx_Oracle.connect("cherymon1/chery@tlmsrac.mychery.com:1521/cheryddc_taf")
    print(db.version)  # 打印版本看看 显示 11.2.0.1.0
    appusercount(db)
    logincount(db)
