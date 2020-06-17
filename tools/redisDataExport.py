#!/usr/bin/env python
# coding: utf-8

from rediscluster import StrictRedisCluster

class RedisCluster(object):  # 连接redis集群
    def __init__(self,conn_list):
        self.conn_list = conn_list  # 连接列表

    def connect(self):
        """
        连接redis集群
        :return: object
        """
        try:
            # 非密码连接redis集群
            redisconn = StrictRedisCluster(startup_nodes=self.conn_list, decode_responses=True)
            # 使用密码连接redis集群
            # redisconn = StrictRedisCluster(startup_nodes=self.conn_list, password='123456')
            return redisconn
        except Exception as e:
            print(e)
            print("错误,连接redis 集群失败")
            return False

    def get_state(self):
        """
        获取状态
        :return:
        """
        res = RedisCluster(self.conn_list).connect()
        # print("连接集群对象",res,type(res),res.__dict__)
        if not res:
            return False

        dic = res.cluster_info()  # 查看info信息, 返回dict

        for i in dic:  # 遍历dict
            ip = i.split(":")[0]
            if dic[i].get('cluster_state'):  # 获取状态
                print("节点状态, ip: ", ip, "value: ", dic[i].get('cluster_state'))


if __name__ == '__main__':

    # redis_basis_conn = [{'host': '10.2.8.5', 'port': 7001}, {'host': '10.2.8.6', 'port': 7001}, {'host': '10.2.8.7', 'port': 7001}, {'host': '10.2.8.8', 'port': 7001}, {'host': '10.2.8.9', 'port': 7001},{'host': '10.2.8.5', 'port': 7002}, {'host': '10.2.8.6', 'port': 7002}, {'host': '10.2.8.7', 'port': 7002}, {'host': '10.2.8.8', 'port': 7002}, {'host': '10.2.8.9', 'port': 7002}]

    redis_basis_conn = [{'host': '39.100.38.255', 'port': 7001}, {'host': '39.100.38.255', 'port': 7002}, {'host': '39.100.38.255', 'port': 7003}, {'host': '39.100.38.255', 'port': 7004}, {'host': '39.100.38.255', 'port': 7005},{'host': '39.100.38.255', 'port': 7006}, {'host': '39.100.38.255', 'port': 7007}, {'host': '39.100.38.255', 'port': 7008}]

    RedisCluster(redis_basis_conn).get_state()