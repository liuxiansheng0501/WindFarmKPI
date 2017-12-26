# -*- coding: utf-8 -*-

import datetime
import random
import sys
import os
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import config
import connectDB
import dataIO
from view.Ui_Form_wtgs_power import Ui_wtgs_power
os.environ['CLASSPATH'] = "../Lib/my.golden.jar"
from jnius import autoclass


class query(QWidget, Ui_wtgs_power):

    def __init__(self, power_info, wtgs_id, parent=None):
        super(query, self).__init__(parent)
        self.argv_cfg=config.argv_cfg()
        self.wtgs_id=wtgs_id
        self.power_info=power_info
        self.setupUi(self)
        self.__initial_combobox__()

    def  __initial_combobox__(self):
        cmp_wtgs_group=sorted(list(set(self.power_info[self.power_info['farm_code']==self.wtgs_id[0:5]]['wtgs_id'].tolist())))
        self.plistwidget_wtgs=QtWidgets.QListWidget()
        self.check_box_wtgs=QtWidgets.QCheckBox('全选')
        self.check_box_wtgs.stateChanged.connect(self.on_check_box_wtgs_stateChanged)
        self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), self.check_box_wtgs)
        for wtgs_name in cmp_wtgs_group:
            self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), QtWidgets.QCheckBox(wtgs_name))
        self.plistwidget_wtgs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.combobox_wtgs.setModel(self.plistwidget_wtgs.model())
        self.combobox_wtgs.setView(self.plistwidget_wtgs)

    @pyqtSlot()
    def on_plt_btn_clicked(self):
        self.wtgs_list = []
        for index in range(1, self.plistwidget_wtgs.count()):
            check_box = self.plistwidget_wtgs.itemWidget(self.plistwidget_wtgs.item(index))
            if check_box.isChecked():
                self.wtgs_list.append(check_box.text())
        if len(self.wtgs_list)==0:
            QMessageBox.information(self, "消息", "请选择机组！")
        sorted(self.wtgs_list)
        self.curve_plot()

    def on_check_box_wtgs_stateChanged(self):
        for index in range(1, self.plistwidget_wtgs.count()):
            check_box = self.plistwidget_wtgs.itemWidget(self.plistwidget_wtgs.item(index))
            if self.check_box_wtgs.isChecked():
                check_box.setCheckState(QtCore.Qt.Checked)
            else:
                check_box.setCheckState(QtCore.Qt.Unchecked)

    def curve_plot(self):
        self.axes.cla()
        if len(list(set(self.power_info[self.power_info['farm_code']==self.wtgs_id[0:5]]['time'].tolist())))>1:
            for i in range(len(self.wtgs_list)):
                wtgs=self.wtgs_list[i]
                color_list=list(self.argv_cfg.cnames.keys())
                if i<len(color_list):
                    color_id=i
                else:
                    color_id=random.randint(0, len(color_list)-1)
                marker_list = list(self.argv_cfg.marker.keys())
                if i<len(marker_list):
                    marker_id=i
                else:
                    marker_id=random.randint(0, len(marker_list)-1)
                wtgs_power=self.power_info[self.power_info['wtgs_id']==wtgs]
                wtgs_power.index=wtgs_power['time'].tolist()
                wtgs_power=wtgs_power.sort_index()
                x_data=list(wtgs_power['time'].tolist())
                y_data=list(wtgs_power['power'].tolist())
                self.axes.plot(range(len(x_data)), y_data, color=color_list[color_id], marker=marker_list[marker_id],linewidth =2)
            self.axes.grid()
            self.axes.set_xticks(range(len(x_data)))
            self.axes.set_xticklabels(x_data)
            self.axes.legend(self.wtgs_list, loc='upper left')
        else:
            power_value=[]
            xdata=range(len(self.wtgs_list))
            for wtgs in self.wtgs_list:
                power_value.append(self.power_info[self.power_info['wtgs_id'] == wtgs]['power'].iloc[0])
            self.axes.bar(xdata,power_value,0.2, color="blue")
            self.axes.set_xticks(xdata)
            self.axes.set_xticklabels(self.wtgs_list)
        self.canvas.draw()

class calculate_multi_thread_ib(QtCore.QThread):

    finishedSignal=QtCore.pyqtSignal(int)
    textinfo=QtCore.pyqtSignal(str)
    def __init__(self,calfiledcon,parent=None):
        super(calculate_multi_thread_ib, self).__init__(parent)
        self.exit_flag=False
        self.run_flag = True
        self.calfiledcon = calfiledcon
        self.start_time=calfiledcon['start_time']
        self.end_time = calfiledcon['end_time']
    def __del__(self):
        self.exit_flag = True
        self.sleep(0.1)
    def run(self):
        cal_num=0
        while self.run_flag:
            cal_wtgs_paths = dataIO.farm_path_ib(self.calfiledcon)
            self.textinfo.emit('发电量:从ib库取数据计算发电量\n计算机组台数：'+str(len(cal_wtgs_paths))+'，请稍后！')
            for row in range(len(cal_wtgs_paths)):
                wtgs_path=cal_wtgs_paths[row:row+1]
                self.calculate_power(wtgs_path)
                cal_num+=1
                self.finishedSignal.emit(cal_num/len(cal_wtgs_paths)*100)
            self.run_flag=False
    def calculate_power(self,wtgs_path):

        self.wtgs_path = wtgs_path
        self.power_cal_loop()
    def power_cal_loop(self):

        start_date_time=datetime.datetime.strptime(self.start_time, "%Y-%m-%d")
        end_date_time= datetime.datetime.strptime(self.end_time, "%Y-%m-%d")
        while start_date_time<end_date_time:
            # print(start_date_time,end_date_time)
            res = self.power_record(start_date_time)
            power = self.cal_power(res)
            self.textinfo.emit('ib数据，风场：'+self.wtgs_path['farm_name'].iloc[0]+','+'机组：'+self.wtgs_path['wtgs_id'].iloc[0]+'，时间：'+start_date_time.strftime("%Y-%m-%d")+',发电量：'+str(power))
            self.export(power,start_date_time.strftime("%Y-%m-%d"))
            start_date_time = start_date_time+datetime.timedelta(days=1)
    def power_record(self,start_date_time):  # 查询记录
        end_time=start_date_time+datetime.timedelta(days=1)
        type=int(int(self.wtgs_path['farm_code'].iloc[0])/10000)
        if type == 1:
            (conn, cur) = connectDB.mysql(self.wtgs_path['host'].iloc[0], int(self.wtgs_path['port'].iloc[0]), 'llj', 'llj@2016', self.wtgs_path['db'].iloc[0])
            sqlstr = "SELECT real_time,PAR_iKWhOverall FROM " + self.wtgs_path['table_name'].iloc[0] + " WHERE real_time BETWEEN '" + start_date_time.strftime("%Y-%m-%d") + "' AND '" + end_time.strftime("%Y-%m-%d") + "' AND PAR_iKWhThisDay BETWEEN \'1\' AND  \'40000\'"
            cur.execute(sqlstr)
            res = cur.fetchall()
            conn.close()
        elif type == 2:
            (conn, cur) = connectDB.mysql(self.wtgs_path['host'].iloc[0], int(self.wtgs_path['port'].iloc[0]), 'llj', 'llj@2016', self.wtgs_path['db'].iloc[0])
            sqlstr = "SELECT real_time,iKWhOverall_h FROM " +self.wtgs_path['table_name'].iloc[0] + " WHERE real_time BETWEEN '" + start_date_time.strftime("%Y-%m-%d") + "' AND '" + end_time.strftime("%Y-%m-%d") + "' AND iKWhThisDay_h BETWEEN \'1\' AND  \'50000\'"
            cur.execute(sqlstr)
            res = cur.fetchall()
            conn.close()
        else:
            pass
        if len(res) == 0:
            self.textinfo.emit('机组：'+self.wtgs_path['wtgs_id'].iloc[0]+'，时间：'+start_date_time.strftime("%Y-%m-%d")+',无数据')
        return res

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


    def cal_power(self,power_record):
        power_week = 0
        i = 0
        while i < len(power_record):
            j = i + 1
            if j >= len(power_record):
                break
            while j < len(power_record):
                if power_record[j][1] >= power_record[j - 1][1]:
                    if j == len(power_record) - 1:
                        power_week += (power_record[j][1] - power_record[i][1])
                        i = len(power_record)
                        break
                    elif (power_record[j][0] - power_record[j - 1][0]).seconds == 0:
                        j += 1
                        if j >= len(power_record):
                            i = len(power_record)
                        continue
                    elif abs((power_record[j][1] - power_record[j - 1][1]) / (
                        power_record[j][0] - power_record[j - 1][0]).seconds) >= 10 and power_record[j + 1][1] >= \
                            power_record[j - 1][1]:
                        j += 2
                        if j >= len(power_record):
                            i = len(power_record)
                        continue  # 防止出现向上突变
                    else:
                        j += 1
                        continue
                else:
                    if power_record[j][0] == power_record[j - 1][0]:
                        power_week += (power_record[j - 1][1] - power_record[i][1])
                        i = j + 1
                        break
                    elif j - 1 == 0:
                        i = j
                        break
                    elif power_record[j + 1][1] >= power_record[j - 1][1]:
                        j += 2
                        if j >= len(power_record):
                            i = len(power_record)
                        continue  # 防止出现向下突变
                    elif (power_record[j - 1][0]).hour <= 1 and power_record[j - 1][1] >= power_record[0][1]:
                        power_week += (power_record[j - 1][1] - power_record[i][1])
                    else:
                        power_week += (power_record[j - 1][1] - power_record[i][1])
                    i = j
                    break
        return power_week

    def export(self,power,time):

        (conn, cur) = connectDB.sqlite()
        sql_que = "SELECT * FROM power WHERE wtgs_id=\'" + str(self.wtgs_path['wtgs_id'].iloc[0]) + "\' AND time=\'" + time + "\'"
        res = pd.read_sql(sql_que, con=conn)
        if len(res) > 0:
            sqlstr = "UPDATE power SET power_ib=\'" + str(power) + "\' WHERE wtgs_id=\'" + str(self.wtgs_path['wtgs_id'].iloc[0]) + "\' AND time=\'" + time + "\'"
            try:
                cur.execute(sqlstr)
                conn.commit()
            except:
                #print(self.wtgs_path['wtgs_id'], time, power, 'UPDATE error')
                pass
        else:
            sqlstr = "REPLACE INTO power (farm_code,farm_name,wtgs_id,time,power_ib) VALUES "
            value = "(\'" + str(self.wtgs_path['farm_code'].iloc[0]) + "\',\'" + self.wtgs_path['farm_name'].iloc[0] + "\',\'" + str(self.wtgs_path['wtgs_id'].iloc[0]) + "\',\'"  + time + "\',\'" + str(power) + "\')"
            sqlstr += value
            try:
                cur.execute(sqlstr)
                conn.commit()
            except:
                #print(self.wtgs_path['wtgs_id'], time, power, 'insert error')
                pass
        conn.close()

class calculate_multi_thread_bd(QtCore.QThread):

    finishedSignal=QtCore.pyqtSignal(int)
    textinfo=QtCore.pyqtSignal(str)
    def __init__(self,calfiledcon,parent=None):
        super(calculate_multi_thread_bd, self).__init__(parent)
        self.exit_flag=False
        self.run_flag = True
        self.calfiledcon = calfiledcon
        self.start_time=calfiledcon['start_time']
        self.end_time = calfiledcon['end_time']
    def __del__(self):
        self.exit_flag = True
        self.sleep(0.1)
    def run(self):
        cal_num=0
        while self.run_flag:
            cal_wtgs_paths = dataIO.farm_path_ib(self.calfiledcon)
            self.textinfo.emit('发电量:从集控取数据计算发电量\n计算机组台数：'+str(len(cal_wtgs_paths))+'，请稍后！')
            for row in range(len(cal_wtgs_paths)):
                wtgs_path=cal_wtgs_paths[row:row+1]
                self.calculate_power(wtgs_path)
                cal_num+=1
                self.finishedSignal.emit(cal_num/len(cal_wtgs_paths)*100)
            self.run_flag=False

    def calculate_power(self,wtgs_path):
        self.wtgs_path = wtgs_path
        self.power_cal_loop()

    def power_cal_loop(self):
        start_date_time=datetime.datetime.strptime(self.start_time, "%Y-%m-%d")
        end_date_time= datetime.datetime.strptime(self.end_time, "%Y-%m-%d")
        while start_date_time<end_date_time:
            power = self.power_cal(start_date_time)
            self.textinfo.emit('集控数据，风场：'+self.wtgs_path['farm_name'].iloc[0]+','+'机组：'+self.wtgs_path['wtgs_id'].iloc[0]+'，时间：'+start_date_time.strftime("%Y-%m-%d")+',发电量：'+str(power))
            self.export(power,start_date_time.strftime("%Y-%m-%d"))
            start_date_time = start_date_time+datetime.timedelta(days=1)

    def power_cal(self, start_date_time):  # 查询记录
        end_time=start_date_time+datetime.timedelta(days=1)
        (conn, cur) = connectDB.mysql('192.168.0.19', 3306, 'llj', 'llj@2016', 'iot_wind')
        sqlstr = "SELECT SUM(DATA_ACCUMULATE) FROM tb_generate_power_report WHERE WTG_ID=\'"+str(self.wtgs_path['wtgs_id'].iloc[0])+"\' AND DATA_TYPE LIKE '%kWh%' AND START_TIME>=\'"+start_date_time.strftime("%Y-%m-%d") +"\' AND START_TIME<\'"+ end_time.strftime("%Y-%m-%d")+"\'"
        cur.execute(sqlstr)
        res = cur.fetchall()
        # #print(res)
        conn.close()
        if len(res) == 0:
            self.textinfo.emit('机组：'+self.wtgs_path['wtgs_id'].iloc[0]+'，时间：'+start_date_time.strftime("%Y-%m-%d")+',无数据')
        return res[0][0]

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

    def export(self,power,time):

        (conn, cur) = connectDB.sqlite()
        sql_que="SELECT * FROM power WHERE wtgs_id=\'"+str(self.wtgs_path['wtgs_id'].iloc[0])+"\' AND time=\'"+time+"\'"
        res=pd.read_sql(sql_que,con=conn)
        if len(res)>0:
            sqlstr = "UPDATE power SET power_bd=\'"+str(power)+"\' WHERE wtgs_id=\'"+str(self.wtgs_path['wtgs_id'].iloc[0])+"\' AND time=\'"+time+"\'"
            try:
                cur.execute(sqlstr)
                conn.commit()
            except:
                #print(self.wtgs_path['wtgs_id'],time,power,'UPDATE error')
                pass
        else:
            sqlstr = "REPLACE INTO power (farm_code,farm_name,wtgs_id,time,power_bd) VALUES "
            value = "(\'" + str(self.wtgs_path['farm_code'].iloc[0]) + "\',\'" + str(self.wtgs_path['farm_name'].iloc[0]) + "\',\'" + self.wtgs_path['wtgs_id'].iloc[0] + "\',\'"  + time + "\',\'" + str(power) + "\')"
            sqlstr += value
            try:
                cur.execute(sqlstr)
                conn.commit()
            except:
                #print(self.wtgs_path['wtgs_id'], time, power, 'insert error')
                pass
        conn.close()

class calculate_multi_thread_golden(QtCore.QThread):

    finishedSignal=QtCore.pyqtSignal(int)
    textinfo=QtCore.pyqtSignal(str)
    def __init__(self,calfiledcon,parent=None):
        super(calculate_multi_thread_golden, self).__init__(parent)
        self.exit_flag=False
        self.run_flag = True
        self.calfiledcon = calfiledcon
        self.start_time=calfiledcon['start_time']
        self.end_time = calfiledcon['end_time']
    def __del__(self):
        self.exit_flag = True
        self.sleep(0.1)
    def run(self):
        cal_num=0
        server_impl = autoclass('com.rtdb.service.impl.ServerImpl')
        server = server_impl("192.168.0.37", 6327, "sa", "golden")
        historian_impl = autoclass('com.rtdb.service.impl.HistorianImpl')
        his = historian_impl(server)
        while self.run_flag:
            # print(self.calfiledcon)
            cal_wtgs_paths = dataIO.farm_tag(self.calfiledcon)
            self.textinfo.emit('发电量:从庚顿库取数据计算发电量\n计算机组台数：'+str(len(cal_wtgs_paths))+'，请稍后！')
            for row in range(len(cal_wtgs_paths)):
                wtgs_path=cal_wtgs_paths[row:row+1]
                self.calculate_power(wtgs_path,his)
                cal_num+=1
                self.finishedSignal.emit(cal_num/len(cal_wtgs_paths)*100)
            self.run_flag=False
        server.close()
        his.close()

    def calculate_power(self,wtgs_path,his):
        self.wtgs_path = wtgs_path
        self.power_cal_loop(his)

    def power_cal_loop(self,his):
        start_date_time=datetime.datetime.strptime(self.start_time, "%Y-%m-%d")
        end_date_time= datetime.datetime.strptime(self.end_time, "%Y-%m-%d")
        cal_result=[]
        while start_date_time<end_date_time:
            end_date_time_loop=start_date_time+datetime.timedelta(days=1)
            power = getIntArchivedValues(int(self.wtgs_path['power'].iloc[0]),start_date_time.strftime("%Y-%m-%d %H:%M:%S"),end_date_time_loop.strftime("%Y-%m-%d %H:%M:%S"),his)
            self.textinfo.emit('庚顿数据，风场：'+self.wtgs_path['farm_name'].iloc[0]+','+'机组：'+str(self.wtgs_path['wtgs_id'].iloc[0])+'，时间：'+start_date_time.strftime("%Y-%m-%d")+',发电量：'+str(power))
            cal_result.append([str(self.wtgs_path['farm_code'].iloc[0]),self.wtgs_path['farm_name'].iloc[0],str(self.wtgs_path['wtgs_id'].iloc[0]),start_date_time.strftime("%Y-%m-%d"),'','',str(power)])
            start_date_time = start_date_time + datetime.timedelta(days=1)
        cal_result=pd.DataFrame(cal_result,columns=['farm_code','farm_name','wtgs_id','time','power_ib','power_bd','power_golden'])
        self.export(cal_result,cal_result['time'].iloc[0],cal_result['time'].iloc[-1])
    def export(self,power,stime,etime):
        (conn, cur) = connectDB.sqlite()
        sql_que="SELECT * FROM power WHERE wtgs_id=\'"+str(self.wtgs_path['wtgs_id'].iloc[0])+"\' AND time>=\'"+stime+"\' AND time<=\'"+etime+"\'"
        res=pd.read_sql(sql_que,con=conn)
        power.index=power['time'].tolist()
        if len(res)>0:
            for row in range(len(res)):
                power['power_ib'].loc[res['time'].iloc[row]]=str(res['power_ib'].iloc[row])
                power['power_bd'].loc[res['time'].iloc[row]] = str(res['power_bd'].iloc[row])
        power=np.array(power)
        sqlvul='(\''
        for item in power:
            if not item[4]:
                item[4]=''
            if not item[5]:
                item[5] = ''
            sqlvul+="\',\'".join(item)
            sqlvul +="\'),(\'"
        # print(sqlvul[:-3])
        sqlstr = "REPLACE INTO power VALUES "
        sqlstr += sqlvul[:-3]
        # print(sqlstr)
        try:
            cur.execute(sqlstr)
            conn.commit()
        except:
            pass
        conn.close()

def getIntArchivedValues(tag_id, start_time, end_time,his):
    # 查询一段时间的存储值
    data_unit = autoclass('com.rtdb.api.util.DateUtil')
    count = pd.date_range(start=start_time, end=end_time, freq='S').size
    values = []
    result = his.getIntArchivedValues(tag_id,count, data_unit.stringToDate(start_time),data_unit.stringToDate(end_time))
    if result.size()>1:
        for i in range(result.size()):
            r = result.get(i)
            values.append(r.getValue())
        power=realPower(values)
    else:
        power=0
    return power

def realPower(powerList):
    while True:
        if max(powerList) - min(powerList)>55000:
            powerList.remove(min(powerList))
            continue
        else:
            break
    return max(powerList) - min(powerList)



if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=query([1, 23], 10005008)
    uset_db.show()
    sys.exit(app.exec_())
