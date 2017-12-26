#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/11 16:07
# @Author  : liulijun
# @Site    : 
# @File    : record_maintain.py
# @Software: PyCharm

import pandas as pd

import connectDB


def record():
    # workbook= win32com.client.Dispatch('Excel.Application').Workbooks.Open('D:/work/周报表/9.3-9.9/9.10工程运维停机机组处理进度跟进表.xlsx')
    # sht1 = workbook.Worksheets('9.3')
    # sht2 = workbook.Worksheets('9.4')
    # sht3 = workbook.Worksheets('9.5')
    # sht4 = workbook.Worksheets('9.6')
    # sht5 = workbook.Worksheets('9.7')
    # sht6 = workbook.Worksheets('9.8')
    # sht7 = workbook.Worksheets('9.9')
    # sht1.Rows(1).Delete()
    # sht2.Rows(1).Delete()
    # sht3.Rows(1).Delete()
    # sht4.Rows(1).Delete()
    # sht5.Rows(1).Delete()
    # sht6.Rows(1).Delete()
    # sht7.Rows(1).Delete()
    # workbook.Close()
    (conn, cur) = connectDB.sqlite()
    sqlstr = "SELECT DISTINCT farm_name FROM farm_path_ib"
    try:
        farm=pd.read_sql(sqlstr,con=conn)
    except:
        pass
    farm=farm['farm_name'].tolist()
    print(len(farm),farm)

    selectedRecord=[]
    for date in ['9.3','9.4','9.5','9.6','9.7','9.8','9.9']:
        recorddata=pd.read_excel('D:/work/周报表/9.3-9.9/9.10工程运维停机机组处理进度跟进表.xlsx',sheetname=date)
        for row in range(len(recorddata)):
            irecord=recorddata.ix[row:row+1]
            for ifarm in farm:
                print(irecord.tolist())
                if irecord['项目名称'].iloc[0] in ifarm:
                    print('yes')
                    selectedRecord.append(irecord)
    da=pd.DataFrame(selectedRecord,columns=['运维中心','项目名称','项目状态 停机因素','异常机位','机组状态','故障类型',	'故障描述','故障日期','停机天数','备件','处理进度	','项目主管','预计恢复时间','备注'])
    da.to_excel('D:/work/周报表/9.3-9.9/运维筛选.xlsx')
if __name__=="__main__":
    record()
