#!/usr/bin/env python
# encoding=utf-8
# 引入Cluster模块
# 提取西安需求所需的数据
# -*- encoding: utf-8 -*-
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.policies import DowngradingConsistencyRetryPolicy
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from cassandra.query import dict_factory
import pandas as pd
import time
import requests
import xlrd


def getlocation(lon, lat):
    location = str(lat) + ',' + str(lon)
    items = {'location': location, 'ak': 'gHnVXdpepEUcRlEU47sviOvyvwsWGxBl', 'output': 'json', 'coordtype': 'wgs84ll'}
    res = requests.get('http://api.map.baidu.com/reverse_geocoding/v3/', params=items)
    return res.json()


def exportData(sess,  vin, maxct, minct, rlt):
    cql_str = "select * from dpsspacef.dps_realtime where v=" + "'" + vin + "'" + " and ct< " + str(
        maxct) + "  and ct> " + str(minct) + "order by ct DESC limit 10000;"
    simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE)
    # 对语句的执行设置超时时间为None
    execute_result = sess.execute(simple_statement, timeout=None)
    # 获取执行结果中的原始数据
    result = execute_result._current_rows
    ct = 0
    for item in result:
        vin = item.v
        dt = item.ct
        st = item.st
        ct = item.ct
        content = item.data
        contents = content.split(';')
        if len(contents) > 44:
            miles = contents[7]
            positionstate = contents[42]
            if positionstate is not None and positionstate == '0':
                lon = float(contents[43]) / 3600000
                lat = float(contents[44]) / 3600000
                # print(vin + ',' + str(miles) + ',' + str(lon) + ","+str(lat)+","+ str(dt))
                rlt.append(vin + ',' + str(dt) + ',' + str(miles) + ',' + str(lon) + ',' + str(lat) + ',' + str(st))
            else:
                continue;
    print(str(vin) + '该批数据采集时间' + str(ct))
    if ct != 0:
        exportData(session, vin, ct, minct, rlt)


def exportalldata(session, vin, minct, maxct, rlt):
    cql_str = "select * from dpsspacef.dps_realtime where v=" + "'" + vin + "'" + " and ct< " + str(
        maxct) + "  and ct> " + str(minct) + "order by ct ASC"
    simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE)
    # 对语句的执行设置超时时间为None
    execute_result = session.execute(simple_statement, timeout=None)
    # 获取执行结果中的原始数据
    result = execute_result._current_rows
    for item in result:
        vin = item.v
        ct = item.ct
        content = item.data
        st = item.st
        rlt.append(vin + ',' + str(ct) + ',' + str(content) + ',' + str(st))
    print(str(vin) + '该批数据采集时间' + str(maxct))


if __name__ == '__main__':
    # 配置Cassandra集群的IP，记得改成自己的远程数据库IP哦
    contact_points = ['10.2.7.125', '10.2.7.126', '10.2.7.127', '10.2.4.135', '10.2.4.136', '10.2.4.137', '10.2.4.138',
                      '10.2.4.139']
    # 配置登陆Cassandra集群的账号和密码，记得改成自己知道的账号和密码
    # auth_provider = PlainTextAuthProvider(username='bba_tfs', password='bba_tfs')
    # 创建一个Cassandra的cluster
    # cluster = Cluster(contact_points=contact_points, auth_provider=auth_provider)
    cluster = Cluster(contact_points, port=19042)

    # 连接并创建一个会话
    session = cluster.connect('dpsspacef')
    session.default_consistency_level = ConsistencyLevel.LOCAL_QUORUM
    # 定义一条cql查询语句 2019/1/31 23:59:59 - 2020/1/31 23:59:59

    # 打开文件
    data = xlrd.open_workbook('xian.xlsx')
    # 查看工作表
    data.sheet_names()
    print("sheets：" + str(data.sheet_names()))
    # 通过文件名获得工作表,获取工作表1
    table = data.sheet_by_name('Sheet1')
    # 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
    # table = data.sheet_by_index(0)
    # 获取行数和列数
    # 行数：table.nrows
    # 列数：table.ncols
    # print("总行数：" + str(table.nrows))
    # print("总列数：" + str(table.ncols))
    # 获取整行的值 和整列的值，返回的结果为数组
    # 整行值：table.row_values(start,end)
    # 整列值：table.col_values(start,end)
    # 参数 start 为从第几个开始打印，
    # end为打印到那个位置结束，默认为none
    # print("整行值：" + str(table.row_values(0)))
    # print("整列值：" + str(table.col_values(1)))
    for i in range(1, 2):
        # 获取某个单元格的值，例如获取B3单元格值
        vin = table.cell(i, 0).value
        print("第" + str(i) + "行第一列的值：" + vin)
        startime = table.cell(i, 7).value
        timeArray = time.strptime(startime, "%Y/%m/%d")
        starttimestamp = int(time.mktime(timeArray))
        endtimeStamp = starttimestamp
        rlt = []
        count = 0
        while count == 0:
            starttimestamp = endtimeStamp
            endtimeStamp = endtimeStamp + 30 * 24 * 60 * 60
            if endtimeStamp > 1580486399:
                endtimeStamp = 1580486399
                count = 1
            exportalldata(session, vin, starttimestamp, endtimeStamp, rlt)
        # 把结果转成DataFrame格式
        result = pd.DataFrame(rlt)
        # 把查询结果写入csv
        result.to_csv('../data/' + str(vin) + '.csv', mode='a', header=True)
    # 关闭连接
    cluster.shutdown()
