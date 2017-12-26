#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/10 9:22
# @Author  : liulijun
# @Site    : 
# @File    : dataIO.py
# @Software: PyCharm

import pandas as pd
import connectDB

def ib_wtgs_path_by_farm_code(farm_code):

    #function: 通过风场代号查询ib库中风场所有风机具体路径

    (conn, cur) = connectDB.sqlite()
    sqlstr = "SELECT * FROM farm_path_ib WHERE farm_code=\'"+str(int(farm_code))+"\'"
    wtgs_paths = pd.read_sql(sqlstr, con=conn)
    conn.close  # 关闭连接
    return wtgs_paths

def sqlserver_wtgs_path_by_farm_code(farm_code):

    #function: 通过风场代号查询actionlist库中风场所有风机具体路径

    (conn, cur) = connectDB.sqlite()
    sqlstr = "SELECT * FROM farm_path_sqlserver WHERE farm_code=\'"+str(int(farm_code))+"\'"
    wtgs_paths = pd.read_sql(sqlstr, con=conn)
    conn.close  # 关闭连接
    return wtgs_paths

def ib_wtgs_path_by_wtgs_id(wtgs_id):

    # function: 通过机组代号查询ib库中风场所有风机具体路径

    (conn, cur) = connectDB.sqlite()
    sqlstr = "SELECT * FROM farm_path_ib WHERE wtgs_id=\'" + str(int(wtgs_id)) + "\'"
    wtgs_path = pd.read_sql(sqlstr, con=conn)
    conn.close  # 关闭连接
    return wtgs_path

def sqlserver_wtgs_path_by_wtgs_id(wtgs_id):

    # function: 通过机组代号查询ib库中风场所有风机具体路径

    (conn, cur) = connectDB.sqlite()
    sqlstr = "SELECT * FROM farm_path_sqlserver WHERE wtgs_id=\'" + str(int(wtgs_id)) + "\'"
    wtgs_path = pd.read_sql(sqlstr, con=conn)
    conn.close  # 关闭连接
    return wtgs_path

def original_filed_value(dir, field):

    (conn,cur)= connectDB.connect_db(dir[3], int(dir[4]), cfg.REMOTE_DB['_user'], cfg.REMOTE_DB['_passwd'], dir[5])
    sqlstr="SELECT wtid,real_time"
    for istr in field:
        sqlstr+=', '+istr
    sqlstr +=" FROM "+dir[6]+" WHERE real_time BETWEEN " + cfg.start_datetime + " AND " + cfg.end_datetime + " "
    for istr in field:
        sqlstr+="AND "+istr+" is NOT NULL "
    sqlstr+=" ORDER BY real_time"
    #print(sqlstr)
    cur.execute(sqlstr)
    #print('e,vomv')
    results=cur.fetchall()
    conn.close()
    return  results

def actionlist_record(path,start_time,end_time):
    (conn, cur) = connectDB.sqlserver('192.168.252.90', 'test', 'test12345678', path['db'].iloc[0])
    sqlstr='SELECT WINDFARM_BIAS_NAME,TURBINE_NAME,ACTION_STR,RUN_CODE,ACTION_TIME,END_TIME,DELTA_HOURS,IS_ERROR_STOP,ERROR_STOP_GROUP,FIRST_CODE_NOTE,PITCH_ANGLE' \
           ' FROM TurbineAction_Table WHERE ACTION_TIME BETWEEN \'' + str(start_time) + '\' and \'' + str(end_time) + '\' AND TURBINE_NAME=\'' + str(path['wtgs_name'].iloc[0]) + '\' ORDER BY ACTION_TIME'
    # print(sqlstr)
    res = pd.read_sql(sqlstr,con=conn)
    conn.close()
    return res
    
def farmcodeDirectory():

    # 查询风场及机组

    (conn,cur)= connectDB.sqlite()
    sqlstr="SELECT farm_name,farm_code,wtgs_id FROM farm_path_sqlserver ORDER BY farm_code"
    farm_name_code=pd.read_sql(sqlstr,con=conn)
    conn.close # 关闭连接
    farmDir={}
    wtgsDir={}
    for ifarm_code in sorted(list(set(farm_name_code['farm_code'].tolist()))):
        farmDir[farm_name_code[farm_name_code['farm_code']==ifarm_code]['farm_name'].iloc[0]]=int(ifarm_code)
    for ifarm_code in sorted(list(set(farm_name_code['farm_code'].tolist()))):
        iwtgsDir={}
        for iwtgs_id in sorted(list(set(farm_name_code[farm_name_code['farm_code']==ifarm_code]['wtgs_id'].tolist()))):
            iwtgsDir[str(int(iwtgs_id))]=int(iwtgs_id)
        wtgsDir[ifarm_code]=iwtgsDir
    return farmDir, wtgsDir
    
def com_data(farm, sd, ed, duration):
    data=[]
    for ifarm in farm:
        (conn, cur) = connectDB.sqlserver('192.168.252.90', 'test', 'test12345678', ifarm[1])
        sqlstr='SELECT SUM(DELTA_HOURS) FROM DataQualityCheck_Table WHERE ACTION_TIME BETWEEN \''+sd.toString("yyyy/MM/dd")+'\' and \''+ed.toString("yyyy/MM/dd")+'\''
#        #print(sqlstr)
        cur.execute(sqlstr)
        res = cur.fetchall()
        conn.close()
        if res[0][0] is not None:
#            #print(res)
            data.append([ifarm[0], ifarm[2], res[0][0],res[0][0]/ifarm[2], 1-res[0][0]/(duration*24*ifarm[2]) ])
    return data
    
def com_data2(singlefarm, sd, ed, duration):
    data=[]
#    #print(singlefarm)
    wtgslist=wtgs_name_server(singlefarm)
#    #print(wtgslist)
    (conn, cur) = connectDB.sqlserver('192.168.252.90', 'test', 'test12345678', wtgslist[0][0])
    for iwtgs in wtgslist:
        sqlstr='SELECT SUM(DELTA_HOURS) FROM DataQualityCheck_Table WHERE TURBINE_NAME=\''+iwtgs[2]+'\' AND ACTION_TIME BETWEEN \''+sd.toString("yyyy/MM/dd")+'\' and \''+ed.toString("yyyy/MM/dd")+'\''
#        #print(sqlstr)
        cur.execute(sqlstr)
        res = cur.fetchall()

        if res[0][0] is not None:
#            #print(res)
            data.append([singlefarm, iwtgs[1], res[0][0],1-res[0][0]/(duration*24) ])
        else:
            data.append([singlefarm, iwtgs[1], res[0][0],1])
    conn.close()
#    #print(data)
    return data
    
def com_data3(singlefarm,wtgsid, sd, ed, duration):
    data=[]
    wtgslist=wtgs_name_server(singlefarm)
    (conn, cur) = connectDB.sqlserver('192.168.252.90', 'test', 'test12345678', wtgslist[0][0])
    sqlstr='SELECT SUM(DELTA_HOURS) FROM DataQualityCheck_Table WHERE TURBINE_NAME LIKE \'%'+wtgsid+'%\' AND ACTION_TIME BETWEEN \''+sd.toString("yyyy/MM/dd")+'\' and \''+ed.toString("yyyy/MM/dd")+'\''
    #print(sqlstr)
    cur.execute(sqlstr)
    res = cur.fetchall()

    if res[0][0] is not None:
        data.append([singlefarm,wtgsid, res[0][0],1-res[0][0]/(duration*24) ])
    else:
        data.append([singlefarm, wtgsid, res[0][0],1])
    conn.close()
    return data
    
def power(query_condition):

    sqlstr = "SELECT farm_code,farm_name,wtgs_id,time,power_ib,power_bd,power_golden from power WHERE"
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys(): # 单个机组
        sqlstr+=" farm_code=\'"+str(query_condition['farm_code'])+"\' AND wtgs_id=\'"+str(query_condition['wtgs_id'])+"\' AND time BETWEEN \'"+query_condition['start_time'] +"\' AND \'"+query_condition['end_time']+"\'"
    elif 'farm_code' in query_condition.keys(): # 单个风场
        sqlstr += " farm_code=\'" + str(query_condition['farm_code']) + "\' AND time BETWEEN \'" + query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    else: # 所有风场
        sqlstr += " time BETWEEN \'" + query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    # print(sqlstr)
    (conn,cur)= connectDB.sqlite()
    res=pd.read_sql(sqlstr,con=conn)
    conn.close()
    # #print(res)
    return res

def power2(query_condition):

    sqlstr0 = "SELECT * from power WHERE time BETWEEN \'" + query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    if 'wtgs_id' in query_condition.keys(): #多个机组
        sqlstr1 = "SELECT * FROM (" + sqlstr0 + ") WHERE wtgs_id=\'" + "\' or farm_code=\'".join(query_condition['wtgs_id']) + "\'"
    elif 'farm_code' in query_condition.keys(): # 多个风场
        sqlstr1 = "SELECT * FROM ("+sqlstr0+") WHERE farm_code=\'" + "\' or farm_code=\'".join(query_condition['farm_code']) + "\'"
    else: # 所有风场
        pass
    # print(sqlstr1)
    (conn,cur)= connectDB.sqlite()
    res=pd.read_sql(sqlstr1,con=conn)
    conn.close()
    print(res)
    return res

def fault_info(query_condition):

    sqlstr = 'SELECT farm_code,farm_name,'
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys():
        sqlstr += "wtgs_id,start_time,end_time,duration,maintain_time,status_code,fault_name,fault_group from fault_info WHERE farm_code=\'" + query_condition[
            'farm_code'] + "\' AND wtgs_id=\'" + query_condition['wtgs_id'] + "\' AND start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    elif 'farm_code' in query_condition.keys():
        sqlstr += "wtgs_id,start_time,end_time,duration,maintain_time,status_code,fault_name,fault_group from fault_info WHERE farm_code=\'" + query_condition[
            'farm_code'] + "\' AND start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    else:
        sqlstr += "wtgs_id,start_time,end_time,duration,maintain_time,status_code,fault_name,fault_group from fault_info WHERE start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    # #print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res

def utilize(query_condition):

    sqlstr = 'SELECT farm_code,farm_name,'
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys():
        sqlstr += "wtgs_id,wtgs_bd,time,fault_maintain_time,maintain_time_normal,stop_time_normal,utilize_time,utilize,info from utilize WHERE farm_code=\'" + \
                  query_condition['farm_code'] + "\' AND wtgs_id=\'" + query_condition['wtgs_id'] + "\' AND time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    elif 'farm_code' in query_condition.keys():
        sqlstr += "wtgs_id,wtgs_bd,time,fault_maintain_time,maintain_time_normal,stop_time_normal,utilize_time,utilize,info from utilize WHERE farm_code=\'" + \
                  query_condition[
                      'farm_code'] + "\' AND time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    else:
        sqlstr += "wtgs_id,wtgs_bd,time,fault_maintain_time,maintain_time_normal,stop_time_normal,utilize_time,utilize,info from utilize WHERE time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    # #print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res

def com_quality(query_condition):

    sqlstr = 'SELECT farm_code,farm_name,'
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys():
        sqlstr += "wtgs_id,wtgs_bd,start_time,end_time,duration,reason from com_quality WHERE farm_code=\'" + \
                  query_condition['farm_code'] + "\' AND wtgs_id=\'" + query_condition['wtgs_id'] + "\' AND start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    elif 'farm_code' in query_condition.keys():
        sqlstr += "wtgs_id,wtgs_bd,start_time,end_time,duration,reason from com_quality WHERE farm_code=\'" + \
                  query_condition['farm_code'] + "\' AND start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    else:
        sqlstr += "wtgs_id,wtgs_bd,start_time,end_time,duration,reason from com_quality WHERE start_time BETWEEN \'" + \
                  query_condition['start_time'] + "\' AND \'" + query_condition['end_time'] + "\'"
    # #print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res

def week_farm_index(query_condition):

    (conn,cur)= connectDB.sqlite()
    sqlstr='SELECT * FROM farm_index'
    res=pd.read_sql(sqlstr,con=conn)
    conn.close()
    return res

def farm_path_ib(query_condition):

    sqlstr = 'SELECT farm_code,farm_name,'
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys():
        sqlstr += "wtgs_id,host,port,db,table_name,wtgs_name from farm_path_ib WHERE farm_code=\'" + \
                  str(query_condition['farm_code']) + "\' AND wtgs_id=\'" + str(query_condition['wtgs_id']) + "\' ORDER BY wtgs_id"
    elif 'farm_code' in query_condition.keys():
        sqlstr += "wtgs_id,host,port,db,table_name,wtgs_name from farm_path_ib WHERE farm_code=\'" + \
                  str(query_condition['farm_code']) + "\' ORDER BY wtgs_id"
    else:
        sqlstr += "wtgs_id,host,port,db,table_name,wtgs_name from farm_path_ib ORDER BY wtgs_id"
    # #print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res

def farm_path_sqlserver(query_condition):
    sqlstr = 'SELECT farm_code,farm_name,wtgs_id,db,wtgs_name from farm_path_sqlserver'
    if 'wtgs_id' in query_condition.keys():
        sqlstr += " WHERE wtgs_id=\'" + "\' or wtgs_id=\'".join(query_condition['wtgs_id']) + "\' ORDER BY wtgs_id"
    elif 'farm_code' in query_condition.keys():
        sqlstr += " WHERE farm_code=\'" +  "\' or farm_code=\'".join(query_condition['farm_code']) + "\' ORDER BY wtgs_id"
    else:
        sqlstr += " ORDER BY wtgs_id"
    # print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res

def farm_tag(query_condition):

    sqlstr = 'SELECT farm_code,farm_name,'
    if 'farm_code' in query_condition.keys() and 'wtgs_id' in query_condition.keys():
        sqlstr += "wtgs_id,power from golden_tag WHERE wtgs_id=\'" + "\' or wtgs_id=\'".join(query_condition['wtgs_id']) + "\' ORDER BY wtgs_id"
    elif 'farm_code' in query_condition.keys():
        sqlstr += "wtgs_id,power from golden_tag WHERE farm_code=\'" + "\' or farm_code=\'".join(query_condition['farm_code']) + "\' ORDER BY wtgs_id"
    else:
        sqlstr += "wtgs_id,power from golden_tag ORDER BY wtgs_id"
    # print(sqlstr)
    (conn, cur) = connectDB.sqlite()
    res = pd.read_sql(sqlstr, con=conn)
    conn.close()
    return res




if __name__=="__main__":
    sqlserver_wtgs_path_by_wtgs_id(10001001)
    
