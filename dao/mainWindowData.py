#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/27 17:47
# @Author  : liulijun
# @Site    : 
# @File    : mainWindowData.py
# @Software: PyCharm

import datetime

import pandas as pd

import connectDB


def warning_table_data(weekdays):
    (conn,cur)= connectDB.mysql('127.0.0.1', 3306, 'root', '911220', 'sub_healthy_model')
    end_date=weekdays['星期日']
    end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_date+=datetime.timedelta(days=1)
    end_date=end_date.strftime('%Y-%m-%d')
    # sqlstr='SELECT farm_name,wtgs_bd,model_name,abnormal_start_time,abnormal_end_time,abnormal_duration FROM early_warning WHERE abnormal_start_time BETWEEN \''+weekdays['星期一']+'\' AND \''+end_date+'\''
    sqlstr = 'SELECT farm_name,wtgs_bd,model_name,abnormal_start_time FROM early_warning WHERE abnormal_start_time BETWEEN \'' + weekdays['星期一'] + '\' AND \'' + end_date + '\''
    cur.execute(sqlstr)
    res = cur.fetchall()
    conn.close()
    return res

def warning_info(query_condition):
    (conn,cur)= connectDB.mysql('127.0.0.1', 3306, 'root', '911220', 'sub_healthy_model')
    sqlstr = 'SELECT * FROM early_warning WHERE farm_name=\''+query_condition[0]+'\' AND wtgs_bd=\''+query_condition[1]+'\' AND model_name=\''+query_condition[2]+'\' AND abnormal_start_time=\''+query_condition[3]+' '+query_condition[4]+'\''
    res=pd.read_sql(sqlstr,con=conn)
    return res