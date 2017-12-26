#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/10 9:15
# @Author  : liulijun
# @Site    : 
# @File    : db_connect.py
# @Software: PyCharm

import pymysql
import pymssql
import sqlite3

#链接mysql数据库函数
def mysql(_host,_port,_user,_passwd,_db):
    # 建立链接
    try:
        conn = pymysql.connect(
            host=_host,
            port=_port,
            user=_user,
            passwd=_passwd,
            db=_db,
            charset="utf8"
        )
        cur = conn.cursor()
        return conn, cur
    except:
        print("Could not connect to MySQL server.")
        exit(0)

#链接sqlserver数据库函数
def sqlserver(_host,_user,_passwd,_db):
    # 建立链接
    try:
        conn = pymssql.connect(
            host=_host,
            user=_user,
            password=_passwd,
            database=_db,
            charset="GBK"
        )
        cur = conn.cursor()
        return conn, cur
    except:
        print("Could not connect to SQLServer server.")
        exit(0)

def sqlite():

    conn = sqlite3.connect('../DB/KPI.db')
    cur = conn.cursor()
    return conn, cur

if __name__=="__main__":
    sqlite()