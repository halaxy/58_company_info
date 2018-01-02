"""
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.9.20"
"""
#coding=utf-8

import json
from time import ctime
from time import sleep

import pymysql

#存储数据
class DataStore(object):
    #本地数据存储
    def local_store(self, data, path):
        with open(path, 'a+') as js:
            json.dump(data, fp=js, ensure_ascii=False)

    #加载本地数据
    def load_data(self, path):
        with open(path, 'r') as js:
            data = json.load(js)
            return data

    #公司信息数据插入数据库
    def insert_database(self, name, com_info):
        try:
            conn = pymysql.connect(host="127.0.0.1", user="root", passwd="xy02012017", db="mypydb")
            cursor = conn.cursor()
            grap_time = str(ctime())
            sql = """create table if not exists comin_fo(name varchar(1000), 
                                                           grap_time varchar(50), 
                                                           register_num varchar(50),
                                                           linkman varchar(20),
                                                           owner varchar(20),
                                                           telephone_num varchar(20),
                                                           com_nature varchar(20),
                                                           com_netaddr varchar(100),
                                                           com_size varchar(20),
                                                           com_addr varchar(100),
                                                           com_business varchar(100)
                                                           )engine=innodb char set utf8"""
            cursor.execute(sql)
            sql1 = "insert into comin_fo(name, grap_time, register_num, linkman, owner,telephone_num,com_nature, com_netaddr, com_size ,com_addr, com_business) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);"
            cursor.execute(sql1, (name, grap_time, str(com_info[0]), str(com_info[1]), str(com_info[2]), str(com_info[3]), str(com_info[4]), str(com_info[5]), str(com_info[6]),str(com_info[7]), str(com_info[8])))
            conn.commit()

        except Exception as e:
            print("异常:" + e)

