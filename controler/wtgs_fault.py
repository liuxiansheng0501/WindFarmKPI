# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import dataIO
import pandas as pd
import config
import connectDB
import datetime
from view.Ui_Form_wtgs_fault import Ui_fault_info

class wtgs_fault(QWidget, Ui_fault_info):

    def __init__(self, fault_info, wtgs_id, parent=None):
        super(wtgs_fault, self).__init__(parent)
        self.argv_cfg=config.argv_cfg()
        self.wtgs_id=wtgs_id
        self.fault_info=fault_info
        self.setupUi(self)
        self.__initial_combobox__()
        self.__initial_wtgs_fault__()

    def  __initial_combobox__(self):
        cmp_wtgs_group=list(set(self.fault_info[self.fault_info['farm_code'] == self.wtgs_id[0:5]]['wtgs_id'].tolist()))
        self.plistwidget_wtgs=QtWidgets.QListWidget()
        self.check_box_wtgs=QtWidgets.QCheckBox('全选')
        self.check_box_wtgs.stateChanged.connect(self.on_check_box_wtgs_stateChanged)
        self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), self.check_box_wtgs)
        for wtgs_name in cmp_wtgs_group:
            self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), QtWidgets.QCheckBox(wtgs_name))
        self.plistwidget_wtgs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.combobox_wtgs.setModel(self.plistwidget_wtgs.model())
        self.combobox_wtgs.setView(self.plistwidget_wtgs)

    def  __initial_wtgs_fault__(self):
        self.info_table.clear()
        self.wtgs_fault_data = self.fault_info[self.fault_info['wtgs_id']==self.wtgs_id]
        label = ['机组号', '开始时间', '结束时间', '持续时间', '状态码', '故障名', '故障类别']
        self.info_table.setColumnCount(7)
        self.info_table.setRowCount(len(self.wtgs_fault_data))
        self.info_table.setHorizontalHeaderLabels(label)
        self.info_table.verticalHeader().setVisible(False)
        self.wtgs_fault_data.sort(columns='start_time')
        for row in range(len(self.wtgs_fault_data)):
            self.info_table.setItem(row, 0, QTableWidgetItem(self.wtgs_fault_data['wtgs_id'].iloc[row]))
            self.info_table.setItem(row, 1, QTableWidgetItem(self.wtgs_fault_data['start_time'].iloc[row]))
            self.info_table.setItem(row, 2, QTableWidgetItem(self.wtgs_fault_data['end_time'].iloc[row]))
            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.wtgs_fault_data['duration'].iloc[row])))
            self.info_table.setItem(row, 4, QTableWidgetItem(self.wtgs_fault_data['status_code'].iloc[row]))
            self.info_table.setItem(row, 5, QTableWidgetItem(self.wtgs_fault_data['fault_name'].iloc[row]))
            self.info_table.setItem(row, 6, QTableWidgetItem(self.wtgs_fault_data['fault_group'].iloc[row]))
        self.info_table.setColumnWidth(0, 80)
        self.info_table.setColumnWidth(1, 160)
        self.info_table.setColumnWidth(2, 160)
        self.info_table.setColumnWidth(3, 80)
        self.info_table.resizeColumnToContents(4)
        self.info_table.resizeColumnToContents(5)
        self.info_table.resizeColumnToContents(6)

    @pyqtSlot()
    def on_query_clicked(self):

        self.wtgs_list = []
        for index in range(1, self.plistwidget_wtgs.count()):
            check_box = self.plistwidget_wtgs.itemWidget(self.plistwidget_wtgs.item(index))
            if check_box.isChecked():
                self.wtgs_list.append(check_box.text())
        if len(self.wtgs_list)==0:
            QMessageBox.question(self, "消息", "请选择机组！", QMessageBox.Yes | QMessageBox.No)
            pass
        else:
            self.update_data()

    @pyqtSlot()
    def on_add_clicked(self):
        lastrow=self.info_table.rowCount()-1
        if not (self.info_table.item(lastrow,0) and self.info_table.item(lastrow,1) and self.info_table.item(lastrow,2) and self.info_table.item(lastrow,3) and self.info_table.item(lastrow,4) and self.info_table.item(lastrow,5) and self.info_table.item(lastrow,6)):
            reply=QMessageBox.question(self, "消息", "已存在空白行，请填写内容！", QMessageBox.Yes | QMessageBox.No)
            pass
        else:
            self.info_table.setRowCount(self.info_table.rowCount()+1)
            for column in range(self.info_table.columnCount()):
                self.info_table.setItem(self.info_table.rowCount()-1,column,QTableWidgetItem(''))

    @pyqtSlot()
    def on_save_clicked(self):
        self.table_data()
        self.export()

    def table_data(self):
        self.updated_table_data=[]
        for row in range(self.info_table.rowCount()):
            if not self.info_table.item(row,0).text():
                QMessageBox.question(self, "消息", "请填写机组号！", QMessageBox.Yes | QMessageBox.No)
                pass
            else:
                farmname=self.wtgs_fault_data[self.wtgs_fault_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_name'].iloc[0]
                farmcode=self.wtgs_fault_data[self.wtgs_fault_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_code'].iloc[0]
                wtgsid = self.info_table.item(row,0).text()
                wtgsbd = self.wtgs_fault_data[self.wtgs_fault_data['wtgs_id'] == self.info_table.item(row, 0).text()]['wtgs_bd'].iloc[0]
                iupdated_table_data=[farmname,farmcode,wtgsid,wtgsbd]
            for column in range(1,self.info_table.columnCount()):
                if self.info_table.item(row,column).text():
                    iupdated_table_data.append(self.info_table.item(row,column).text())
                else:
                    if column==1:
                        QMessageBox.question(self, "消息", "请填写故障开始时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==2:
                        QMessageBox.question(self, "消息", "请填写故障结束时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==3:
                        QMessageBox.question(self, "消息", "请填写故障持续时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==4:
                        QMessageBox.question(self, "消息", "请填写故障状态码！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==5:
                        QMessageBox.question(self, "消息", "请填写故障名称！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==6:
                        QMessageBox.question(self, "消息", "请填写故障类别！", QMessageBox.Yes | QMessageBox.No)
                        pass
            self.updated_table_data.append(iupdated_table_data)

    def export(self):

        if len(self.updated_table_data)>0:

            for table_data in self.updated_table_data:
                (conn, cur) = connectDB.sqlite()
                sqlstr = "REPLACE INTO fault_info (farm_name,farm_code,wtgs_id,wtgs_bd,start_time,end_time,duration,status_code,fault_name,fault_group) VALUES "
                value = '(\''
                value+='\',\''.join(table_data)
                value += '\')'
                sqlstr += value
                try:
                    # ##print(sqlstr)
                    cur.execute(sqlstr)
                    conn.commit()
                    QMessageBox.question(self, "消息", "保存成功！", QMessageBox.Yes | QMessageBox.No)
                    pass
                except:
                    # ##print('insert error')
                    pass
                conn.close()
        else:
            pass

    def on_check_box_wtgs_stateChanged(self):

        for index in range(1, self.plistwidget_wtgs.count()):
            check_box = self.plistwidget_wtgs.itemWidget(self.plistwidget_wtgs.item(index))
            if self.check_box_wtgs.isChecked():
                check_box.setCheckState(QtCore.Qt.Checked)
            else:
                check_box.setCheckState(QtCore.Qt.Unchecked)

    def update_data(self):

        self.info_table.clear()
        self.wtgs_fault_data = self.fault_info[self.fault_info['wtgs_id'].isin(self.wtgs_list)]
        label = ['机组号', '开始时间', '结束时间', '持续时间','状态码','故障名','故障类别']
        self.info_table.setColumnCount(7)
        self.info_table.setRowCount(len(self.wtgs_fault_data))
        self.info_table.setHorizontalHeaderLabels(label)
        self.info_table.verticalHeader().setVisible(False)
        self.wtgs_fault_data.sort(columns='start_time')
        for row in range(len(self.wtgs_fault_data)):
            self.info_table.setItem(row, 0, QTableWidgetItem(self.wtgs_fault_data['wtgs_id'].iloc[row]))
            self.info_table.setItem(row, 1, QTableWidgetItem(self.wtgs_fault_data['start_time'].iloc[row]))
            self.info_table.setItem(row, 2, QTableWidgetItem(self.wtgs_fault_data['end_time'].iloc[row]))
            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.wtgs_fault_data['duration'].iloc[row])))
            self.info_table.setItem(row, 4, QTableWidgetItem(self.wtgs_fault_data['status_code'].iloc[row]))
            self.info_table.setItem(row, 5, QTableWidgetItem(self.wtgs_fault_data['fault_name'].iloc[row]))
            self.info_table.setItem(row, 6, QTableWidgetItem(self.wtgs_fault_data['fault_group'].iloc[row]))
        self.info_table.setColumnWidth(0, 80)
        self.info_table.setColumnWidth(1, 160)
        self.info_table.setColumnWidth(2, 160)
        self.info_table.setColumnWidth(3, 80)
        self.info_table.resizeColumnToContents(4)
        self.info_table.resizeColumnToContents(5)
        self.info_table.resizeColumnToContents(6)

class cal_sub_thread(QtCore.QThread):

    finishedSignal=QtCore.pyqtSignal(int)
    textinfo=QtCore.pyqtSignal(str)
    def __init__(self,calfiledcon,parent=None):
        super(cal_sub_thread, self).__init__(parent)
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
            cal_wtgs_paths = dataIO.farm_path_sqlserver(self.calfiledcon)
            self.textinfo.emit('actionlist:故障信息执行机组台数：'+str(len(cal_wtgs_paths))+'，请稍后！')
            for row in range(len(cal_wtgs_paths)):
                wtgs_path=cal_wtgs_paths[row:row+1]
                self.actionlist_fault(wtgs_path)
                cal_num+=1
                self.finishedSignal.emit(cal_num/len(cal_wtgs_paths)*100)
            self.run_flag=False

    def actionlist_fault(self,wtgs_path):

        fault_info=[]
        res = dataIO.actionlist_record(wtgs_path,self.start_time,self.end_time)
        ##print('原始数据',res)
        row=0
        while row < len(res):
            #print(len(res),row)
            if int(res['RUN_CODE'].iloc[row])==4 and str(res['IS_ERROR_STOP'].iloc[row])=='是': # 机组故障维护时间
                #print('故障：')
                farm_name=str(res['WINDFARM_BIAS_NAME'].iloc[row])
                farm_code=str(int(res['TURBINE_NAME'].iloc[row][0:5]))
                wtgs_id=str(int(res['TURBINE_NAME'].iloc[row][6:14]))
                start_time=str(res['ACTION_TIME'].iloc[row])
                # end_time=str(res['END_TIME'].iloc[row])
                duration=str(res['DELTA_HOURS'].iloc[row])
                status_code=str(res['FIRST_CODE_NOTE'].iloc[row][res['FIRST_CODE_NOTE'].iloc[row].index(':')+1:])
                match_fault_name,match_fault_group=match(int(res['TURBINE_NAME'].iloc[row][0:1]),res['FIRST_CODE_NOTE'].iloc[row][res['FIRST_CODE_NOTE'].iloc[row].index(':')+1:])
                # self.textinfo.emit(farm_name,wtgs_id,start_time,end_time,duration,status_code,match_fault_name,match_fault_group)
                if len(match_fault_name)>0:
                    fault_name=match_fault_name
                    fault_group=match_fault_group
                else:
                    fault_name=res['ERROR_STOP_GROUP'].iloc[row][:-4]
                    fault_group=res['ERROR_STOP_GROUP'].iloc[row][:-4]
                rowj=row+1
                if rowj==len(res):
                    row =len(res)
                    break
                else:
                    while rowj< len(res):
                        # print(rowj,len(res),str(res['ACTION_STR'].iloc[rowj]),res['END_TIME'].iloc[rowj])
                        if str(res['ACTION_STR'].iloc[rowj]) in ['环境停机','环境待机','电网故障停机']:
                            delta=(datetime.datetime.strptime(str(res['ACTION_TIME'].iloc[rowj]),"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(str(res['END_TIME'].iloc[row]),"%Y-%m-%d %H:%M:%S"))
                            maintain_time=delta.seconds/3600+delta.days*24
                            maintain_time=str(round(maintain_time,4))
                            end_time = str(res['ACTION_TIME'].iloc[rowj])
                            row=rowj+1
                            break
                        elif str(res['ACTION_STR'].iloc[rowj]) == '机组启动' and (rowj==len(res)-1): # 最后一条是机组启动状态
                            delta = (datetime.datetime.strptime(str(res['ACTION_TIME'].iloc[rowj]),"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(res['END_TIME'].iloc[row]), "%Y-%m-%d %H:%M:%S"))
                            maintain_time = delta.seconds / 3600 + delta.days * 24
                            maintain_time = str(round(maintain_time, 4))
                            end_time = str(res['ACTION_TIME'].iloc[rowj])
                            row = rowj + 1
                            break
                        elif str(res['ACTION_STR'].iloc[rowj]) == '机组启动' and (rowj<(len(res)-1)):
                            if str(res['ACTION_STR'].iloc[rowj+1]) == '并网运行':
                                delta = (datetime.datetime.strptime(str(res['ACTION_TIME'].iloc[rowj]),"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(res['END_TIME'].iloc[row]), "%Y-%m-%d %H:%M:%S"))
                                maintain_time = delta.seconds / 3600 + delta.days * 24
                                maintain_time=str(round(maintain_time,4))
                                end_time = str(res['ACTION_TIME'].iloc[rowj])
                                row = rowj + 1
                                break
                            else:
                                rowj+=1
                                continue
                        elif str(res['ACTION_STR'].iloc[rowj]) == '并网运行':
                            delta = (datetime.datetime.strptime(str(res['ACTION_TIME'].iloc[rowj]),"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(res['END_TIME'].iloc[row]), "%Y-%m-%d %H:%M:%S"))
                            maintain_time = delta.seconds / 3600 + delta.days * 24
                            maintain_time=str(round(maintain_time,4))
                            end_time = str(res['ACTION_TIME'].iloc[rowj])
                            row = rowj + 1
                            break
                        elif rowj==len(res)-1 and str(res['ACTION_STR'].iloc[rowj])=='机组维护': # 截止到统计周期末端仍故障维护中
                            delta = (datetime.datetime.strptime(str(res['END_TIME'].iloc[rowj]),"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(res['END_TIME'].iloc[row]), "%Y-%m-%d %H:%M:%S"))
                            maintain_time = delta.seconds / 3600 + delta.days * 24
                            maintain_time = str(round(maintain_time, 4))
                            end_time = str(res['END_TIME'].iloc[rowj])
                            row = len(res)
                            break
                        else:
                            rowj += 1
                            continue
                    row=rowj+1
                fault_info.append([farm_name,farm_code,wtgs_id,start_time,end_time,duration,maintain_time,status_code,fault_name,fault_group])
            elif str(res['ACTION_STR'].iloc[row]) in ['机组维护','机组故障停机','就地停机','远程停机','电网故障停机','环境停机']:  # 机组不可用时间
                # ##print('不可用',res[row:row+1])
                farm_name = str(res['WINDFARM_BIAS_NAME'].iloc[row])
                farm_code = str(int(res['TURBINE_NAME'].iloc[row][0:5]))
                wtgs_id = str(int(res['TURBINE_NAME'].iloc[row][6:14]))
                start_time = str(res['ACTION_TIME'].iloc[row])
                end_time = str(res['END_TIME'].iloc[row])
                duration = str(res['DELTA_HOURS'].iloc[row])
                status_code = 'unavailable'
                fault_name = str(res['ACTION_STR'].iloc[row])
                fault_group = str(res['ACTION_STR'].iloc[row])
                maintain_time='10000'
                fault_info.append([farm_name, farm_code, wtgs_id, start_time, end_time, duration, maintain_time, status_code,fault_name, fault_group])
                row += 1
                continue
            else:
                # ##print('其它', res[row:row+1])
                row+=1
                continue
        if len(fault_info)>0:
            for i in range(len(fault_info)):
                sqlstr = "REPLACE INTO fault_info (farm_name,farm_code,wtgs_id,start_time,end_time,duration,maintain_time,status_code,fault_name,fault_group) VALUES "
                sqlstr += "(\'"+"\',\'".join(fault_info[i])+"\')"
                self.textinfo.emit("\',\'".join(fault_info[i]))
                try:
                    (conn, cur) = connectDB.sqlite()
                    cur.execute(sqlstr)
                    conn.commit()
                    conn.close()
                except:
                    conn.close()
                    pass

class fault_query(QtCore.QThread):
    def __init__(self,quefiledcon,parent=None):
        super(fault_query, self).__init__(parent)
        self.quefiledcon=quefiledcon
        self.start_time=quefiledcon['start_time']
        self.end_time = datetime.datetime.strptime(quefiledcon['end_time'], "%Y-%m-%d")+datetime.timedelta(days=1)
        self.end_time=self.end_time.strftime("%Y-%m-%d %H:%M:%S")
        self.run()

    def run(self):
        fault_times_time={}
        fautlt_list=pd.DataFrame()
        cal_wtgs_paths = dataIO.farm_path_sqlserver(self.quefiledcon)
        for row in range(len(cal_wtgs_paths)):
            wtgs_path = cal_wtgs_paths[row:row + 1]
            (res_a,res_b)=self.fault_info(wtgs_path)
            print(res_b)
            if len(res_a)>0:
                fautlt_list=pd.concat([fautlt_list,res_a])
            else:
                pass
            if res_b[0] not in fault_times_time.keys():
                fault_times_time[res_b[0]]=[res_b]
            else:
                fault_times_time[res_b[0]].append(res_b)
        # print(fautlt_list)
        all_data_list=[]
        fautlt_list.to_excel("D:\\work\\周报表\\11.19-11.25\\" + "总故障清单" + ".xlsx")
        writer = pd.ExcelWriter('D:\\work\\周报表\\11.19-11.25\\MTBF.xlsx')
        for farm in fault_times_time.keys():
            data=pd.DataFrame(fault_times_time[farm],columns=['风场','机组','次数','时间','不可用','故障+不可用','MTBF','可利用率'])
            data.to_excel(writer,farm,index=True)
            all_data_list.append([farm,sum(data['次数'].tolist()),sum(data['时间'].tolist()),sum(data['MTBF'].tolist())/len(data['MTBF'].tolist()),sum(data['可利用率'].tolist())/len(data['可利用率'].tolist())])
        all_data_list=pd.DataFrame(all_data_list,columns=['风场','故障次数','故障时间','MTBF','可利用率'])
        all_data_list.to_excel(writer,'所有',index=True)
        writer.save
        f15=fautlt_list[fautlt_list['farm_code'] <'20000' ]
        f20 = fautlt_list[fautlt_list['farm_code'] > '20000']
        rank_f15=[]
        rank_f20=[]
        type_f15=list(set(f15['fault_group'].tolist()))
        type_f20 = list(set(f20['fault_group'].tolist()))
        for f in type_f15:
            sub_f=f15[f15['fault_group']==f]
            type_f = list(set(sub_f['fault_name'].tolist()))
            max=0
            for isub_f in type_f:
                if len(sub_f[sub_f['fault_name']==isub_f])>max:
                    max=len(sub_f[sub_f['fault_name'] == isub_f])
                    fault_name=isub_f
            rank_f15.append([f,len(f15[f15['fault_group']==f]),fault_name,max])
        for f in type_f20:
            sub_f = f20[f20['fault_group'] == f]
            type_f = list(set(sub_f['fault_name'].tolist()))
            max = 0
            for isub_f in type_f:
                if len(sub_f[sub_f['fault_name'] == isub_f]) > max:
                    max = len(sub_f[sub_f['fault_name'] == isub_f])
                    fault_name = isub_f
            rank_f20.append([f, len(f20[f20['fault_group'] == f]),fault_name,max])
        rank_f15=pd.DataFrame(rank_f15,columns=['主故障','主故障次数','子故障','子故障次数'])
        rank_f15=rank_f15.sort_values(by='主故障次数', ascending=False)
        rank_f20 = pd.DataFrame(rank_f20,columns=['主故障','主故障次数','子故障','子故障次数'])
        rank_f20 = rank_f20.sort_values(by='主故障次数', ascending=False)
        wtgs_f15 = []
        wtgs_f20 = []
        wtgsf15 = list(set(f15['wtgs_id'].tolist()))
        wtgsf20 = list(set(f20['wtgs_id'].tolist()))
        for iwtgs in wtgsf15:
            wtgs_f15.append([iwtgs,len(f15[f15['wtgs_id']==iwtgs])])
        for iwtgs in wtgsf20:
            wtgs_f20.append([iwtgs, len(f20[f20['wtgs_id'] == iwtgs])])

        wtgs_f15 = pd.DataFrame(wtgs_f15,columns=['机组','故障次数'])
        wtgs_f15 = wtgs_f15.sort_values(by='故障次数', ascending=False)
        wtgs_f20 = pd.DataFrame(wtgs_f20,columns=['机组','故障次数'])
        wtgs_f20 = wtgs_f20.sort_values(by='故障次数', ascending=False)

        writer = pd.ExcelWriter('D:\\work\\周报表\\11.19-11.25\\机型.xlsx')
        rank_f15.to_excel(writer,'1.5故障',index=True)
        rank_f20.to_excel(writer, '2.0故障', index=True)
        wtgs_f15.to_excel(writer, '1.5机组', index=True)
        wtgs_f20.to_excel(writer, '2.0机组', index=True)
        writer.save

        farm_list = list(set(fautlt_list['farm_name'].tolist()))
        writer = pd.ExcelWriter('D:\\work\\周报表\\11.19-11.25\\所有风场故障类型-故障次数.xlsx')
        for farm in farm_list:
            fautlt_list_farm=fautlt_list[fautlt_list['farm_name']==farm]
            type=list(set(fautlt_list_farm['fault_group'].tolist()))
            aa=[]
            for itype in type:
                aa.append([farm,itype,len(fautlt_list_farm[fautlt_list_farm['fault_group']==itype])])
            aa=pd.DataFrame(aa,columns=['风场','故障类型','故障次数'])
            aa = aa.sort_values(by='故障次数', ascending=False)
            aa.to_excel(writer,farm,index=True)
        writer.save
        writer = pd.ExcelWriter('D:\\work\\周报表\\11.19-11.25\\所有风场故障次数-故障时间.xlsx')
        farm_list = list(set(fautlt_list['farm_name'].tolist()))
        for farm in farm_list:
            fautlt_list_farm=fautlt_list[fautlt_list['farm_name']==farm]
            type=list(set(fautlt_list_farm['wtgs_id'].tolist()))
            # print(type)
            aa=[]
            for itype in type:
                time0=0
                for j in range(len(fautlt_list_farm[fautlt_list_farm['wtgs_id'] == itype])):
                    time0+=float(fautlt_list_farm[fautlt_list_farm['wtgs_id'] == itype]['duration'].iloc[j])
                    time0+=float(fautlt_list_farm[fautlt_list_farm['wtgs_id'] == itype]['maintain_time'].iloc[j])
                aa.append([farm,itype,len(fautlt_list_farm[fautlt_list_farm['wtgs_id']==itype]),time0])
            aa=pd.DataFrame(aa,columns=['风场','机组','故障次数','故障时间'])
            aa = aa.sort_values(by='故障时间', ascending=False)
            aa.to_excel(writer,farm,index=True)
        writer.save

    def fault_info(self,wtgs_path):
        (conn,cur)=connectDB.sqlite()
        sqlstr="SELECT * from fault_info WHERE wtgs_id=\'"+str(wtgs_path['wtgs_id'].iloc[0])+"\' AND end_time >= \'"+self.start_time+"\' AND start_time <=\'"+self.end_time+"\'"
        res=pd.read_sql(sqlstr,con=conn)
        conn.close()
        left_flag = 0 # 是否有跨越统计周期开始时间的故障标志位
        span_flag = 0 # 是否有跨越整个统计周期的故障标志位
        right_flag = 0 # 是否有跨越统计周期结束时间的故障标志位
        middle_flag = 0 # 统计周期内的故障次数标志位
        # if len(res)>0:
        fault_reocrd =res[res['status_code']!='unavailable']
        fault_times=0
        fault_time=0
        unavailabel_time=0
        fault_plus_unavailabel_time=0
        for row in range(len(res)):
            if res['status_code'].iloc[row]!='unavailable':
                fault_times+=1
                if res['end_time'].iloc[row]>self.end_time and res['start_time'].iloc[row]>self.start_time:#右侧
                    etime=datetime.datetime.strptime(str(self.end_time),"%Y-%m-%d %H:%M:%S")
                    stime=datetime.datetime.strptime(str(res['start_time'].iloc[row]),"%Y-%m-%d %H:%M:%S")
                    this_fault_time =  round((etime-stime).seconds/3600,4)+(etime-stime).days*24
                elif res['end_time'].iloc[row]>self.end_time and res['start_time'].iloc[row]<self.start_time:#横跨
                    span_flag=1
                    this_fault_time=168
                elif res['end_time'].iloc[row]<self.end_time and res['start_time'].iloc[row]<self.start_time:#左侧
                    etime = datetime.datetime.strptime(str(res['end_time'].iloc[row]), "%Y-%m-%d %H:%M:%S")
                    stime = datetime.datetime.strptime(str(self.start_time), "%Y-%m-%d")
                    this_fault_time = float(res['maintain_time'].iloc[row]) + round((etime - stime).seconds / 3600,4) + (etime - stime).days * 24
                else:#中间
                    middle_flag+=1
                    this_fault_time=float(res['duration'].iloc[row])+float(res['maintain_time'].iloc[row])
                fault_time+=this_fault_time
                fault_plus_unavailabel_time+=this_fault_time
            elif res['fault_name'].iloc[row] not in ['环境停机','远程停机','电网故障停机']:
                if res['end_time'].iloc[row]>self.end_time and res['start_time'].iloc[row]>self.start_time:#右侧
                    etime=datetime.datetime.strptime(str(self.end_time),"%Y-%m-%d %H:%M:%S")
                    stime=datetime.datetime.strptime(str(res['start_time'].iloc[row]),"%Y-%m-%d %H:%M:%S")
                    this_fault_time = + round((etime-stime).seconds/3600,4)+(etime-stime).days*24
                elif res['end_time'].iloc[row]>self.end_time and res['start_time'].iloc[row]<self.start_time:#横跨
                    span_flag=1
                    this_fault_time=168
                elif res['end_time'].iloc[row]<self.end_time and res['start_time'].iloc[row]<self.start_time:#左侧
                    etime = datetime.datetime.strptime(str(res['end_time'].iloc[row]), "%Y-%m-%d %H:%M:%S")
                    stime = datetime.datetime.strptime(str(self.start_time), "%Y-%m-%d")
                    this_fault_time = round((etime - stime).seconds / 3600,4) + (etime - stime).days * 24
                else:#中间
                    middle_flag+=1
                    this_fault_time = float(res['duration'].iloc[row])
                fault_time += this_fault_time
                fault_plus_unavailabel_time+= this_fault_time
                # if res['end_time'].iloc[row]>self.end_time:
                #     Stime = datetime.datetime.strptime(res['start_time'].iloc[row], "%Y-%m-%d %H:%M:%S")
                #     Etime = datetime.datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
                #     this_fault_time=round((Etime-Stime).seconds/3600,4)+(Etime-Stime).days*24
                #     # fault_times += 1
                #     fault_time += this_fault_time
                #     fault_plus_unavailabel_time += this_fault_time
                # else:
                #     # fault_times += 1
                #     fault_time += float(res['duration'].iloc[row])
                #     fault_plus_unavailabel_time+= float(res['duration'].iloc[row])
        # if fault_times>0:
        #     mtbf=(168-fault_plus_unavailabel_time)/fault_times
        # else:
        #     mtbf=168-fault_plus_unavailabel_time
        # availabel_p=(168-fault_plus_unavailabel_time)/168
        delta_time=datetime.datetime.strptime(self.end_time,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(self.start_time,"%Y-%m-%d")
        if span_flag==1 and fault_time>(delta_time.days*24):
            fault_time-=delta_time.days*24
            fault_plus_unavailabel_time -= delta_time.days * 24
            mtbf = (168 - fault_plus_unavailabel_time)/(middle_flag+1)
            availabel_p = (168 - fault_plus_unavailabel_time) / 168
        elif span_flag==1 and fault_time==(delta_time.days*24):
            mtbf = 0
            availabel_p = 0
        elif middle_flag==0:
            mtbf=(168-fault_plus_unavailabel_time)
            availabel_p=(168-fault_plus_unavailabel_time)/168
        else:
            mtbf = (168 - fault_plus_unavailabel_time)/(middle_flag+1)
            availabel_p = (168 - fault_plus_unavailabel_time) / 168
        # else:
        #     # 查询机组是否在本周内一直停机
        #     (conn, cur) = connectDB.sqlite()
        #     sqlstr = "SELECT * from fault_info WHERE start_time<\'"+self.start_time+"\' and end_time LIKE \'2049%\' AND fault_name!=\'环境停机\' AND wtgs_id=\'"+wtgs_path['wtgs_id'].iloc[0]+"\'"
        #     # print(sqlstr)
        #     res = pd.read_sql(sqlstr, con=conn)
        #     conn.close()
        #     if len(res)>0:
        #         fault_reocrd = []
        #         fault_times = 1
        #         fault_time = 168
        #         unavailabel_time = 0
        #         fault_plus_unavailabel_time = 168
        #         mtbf = 0
        #         availabel_p = 0
        #     else:
        #         fault_reocrd = []
        #         fault_times = 0
        #         fault_time = 0
        #         unavailabel_time = 0
        #         fault_plus_unavailabel_time = 0
        #         mtbf = 168
        #         availabel_p = 1
        return fault_reocrd,[wtgs_path['farm_name'].iloc[0],wtgs_path['wtgs_id'].iloc[0],fault_times,fault_time,unavailabel_time,fault_plus_unavailabel_time,mtbf,availabel_p]


def match(type,status_code):
    conn,cur=connectDB.sqlite()
    if type==1:
        sqlstr="SELECT fault_name,fault_group FROM status_code_cfg_1p5 WHERE status_code==\'"+status_code+"\'"
    else:
        sqlstr="SELECT fault_name,fault_group FROM status_code_cfg_2p0 WHERE status_code==\'"+status_code+"\'"
    res=pd.read_sql(sqlstr,con=conn)
    if len(res)>0:
        fault_name=res['fault_name'].iloc[0]
        fault_group=res['fault_group'].iloc[0]
    else:
        fault_name=[]
        fault_group=[]
    return fault_name,fault_group

if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=wtgs_fault([1, 23], 10005008)
    uset_db.show()
    sys.exit(app.exec_())
