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
from openpyxl import Workbook
wb = Workbook()
dest_filename = '低电电压报警.xls'
ws1 = wb.active
ws1.title = "低电电压报警"

# 配置Cassandra集群的IP，记得改成自己的远程数据库IP哦
contact_points = ['10.2.7.125', '10.2.7.126', '10.2.7.127', '10.2.4.135', '10.2.4.136', '10.2.4.137',
                  '10.2.4.138', '10.2.4.139']
# 配置登陆Cassandra集群的账号和密码，记得改成自己知道的账号和密码
# auth_provider = PlainTextAuthProvider(username='bba_tfs', password='bba_tfs')
# 创建一个Cassandra的cluster
# cluster = Cluster(contact_points=contact_points, auth_provider=auth_provider)
cluster = Cluster(contact_points, port=19042)

def exportData(session, vin, rlt, cts, mileages):
    cql_str = "select * from dpsspacef.dps_realtime where v="+"'"+vin+"'"+" and ct>1582646400 and ct< 1582730075 order by ct DESC;"
    simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE)
    # 对语句的执行设置超时时间为None
    execute_result = session.execute(simple_statement, timeout=None)
    # 获取执行结果中的原始数据
    result = execute_result._current_rows
    for item in result:
        vin = item.v
        ct = item.ct
        # # 转换成localtime
        time_local = time.localtime(ct)
        # # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        content = item.data
        contents = content.split(';')
        if len(contents) >= 64:
            A = (contents[60])
            B = (contents[61])
            C = (contents[62])
            D = (contents[63])
            print(str(vin) + '低电电压报警' + str(A)+';'+ str(B)+';'+ str(C)+';'+ str(D))
            rlt.append(vin)
            cts.append(str(dt))
            mileages.append(str(A))
        else:
            continue;

def getSession():
    # 连接并创建一个会话
    session = cluster.connect('dpsspacef')
    session.default_consistency_level = ConsistencyLevel.LOCAL_QUORUM
    return session

# 打开文件
data = xlrd.open_workbook('低电电压vin.xlsx')
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
# print("整列值：" + str(table.col_values(1)))396
name = []
cts = []
mileages = []
for i in range(0, 1):
    # 获取某个单元格的值，例如获取B3单元格值
    vin = table.cell(i, 0).value
    # print("第"+str(i)+"行第3列的值：" + vin)
    exportData(getSession(), vin, name, cts, mileages)
    # 把结果转成DataFrame格式

ws1['A1'] = 'VIN号'
ws1['B1'] = '采集时间'
ws1['C1'] = '低电电压报警'
for (i, m, o) in zip(name, cts, mileages):
    col_A = 'A%s' % (cts.index(m) + 2)
    col_B = 'B%s' % (cts.index(m) + 2)
    col_C = 'C%s' % (cts.index(m) + 2)
    ws1[col_A] = i
    ws1[col_B] = m
    ws1[col_C] = o

wb.save(filename=dest_filename)
# 关闭连接
cluster.shutdown()


