# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
""", 
import datetime
import sys
import time
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import dataIO
from controler import wtgs_power
from controler.comQuality import qua_com
from controler.com_quality import com_quality
from controler.setMysqlPath import set_db
from controler.setSqlServerPath import set_db2
from controler.utilize import wtgs_utilize
from controler import wtgs_fault
from controler.wtgs_power import query
from dao import mainWindowData
from view.Ui_Form_manual import Ui_Form_manual
from view.Ui_Form_warning_statis import Ui_Form_warning_statis
from view.Ui_main_window import Ui_MainWindow

DATETIME_FORMAT = "yyyy-MM-dd"


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initial_date()
        self.initial_farm_wtgs()
        self.check_state_change()
        self.dailog=1
        self.pbar=0
        self.btn_query=0
        self.label_progress_bar_ib.setVisible(0)
        self.label_progress_bar_bd.setVisible(0)
        self.label_progress_bar_golden.setVisible(0)
        self.progress_bar_ib.setVisible(0)
        self.progress_bar_bd.setVisible(0)
        self.progress_bar_golden.setVisible(0)

    def initial_date(self):
        #set start and end date as the current date
        self.dateTimeEdit_startdate.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime()), 'yyyy-MM-dd'))
        self.dateTimeEdit_startdate.setDisplayFormat(DATETIME_FORMAT)
        self.dateTimeEdit_startdate.setCalendarPopup(True)
        self.dateTimeEdit_enddate.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime()), 'yyyy-MM-dd'))
        self.dateTimeEdit_enddate.setDisplayFormat(DATETIME_FORMAT)
        self.dateTimeEdit_enddate.setCalendarPopup(True)
    
    def initial_farm_wtgs(self):
        # set option for farm and wtgs
        self.comboBox_farm.clear()
        self.comboBox_wtgs.clear()
        self.comboBox_farm.addItem(u'全选')
        self.comboBox_wtgs.addItem(u'全选')
        (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
        self.farmListWidget = QtWidgets.QListWidget()
        self.checkBoxfarmAll = QtWidgets.QCheckBox('全选')
        self.checkBoxfarmAll.stateChanged.connect(self.onChecBoxFarmAllStateChanged)
        self.farmListWidget.setItemWidget(QtWidgets.QListWidgetItem(self.farmListWidget),self.checkBoxfarmAll)
        self.farmListWidget.currentRowChanged.connect(self.on_comboBox_farm_activated)
        for (keys, val) in self.farm.items():
            self.farmListWidget.setItemWidget(QtWidgets.QListWidgetItem(self.farmListWidget),QtWidgets.QCheckBox(str(keys)))
        self.farmListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.comboBox_farm.setModel(self.farmListWidget.model())
        self.comboBox_farm.setView(self.farmListWidget)
        self.farm_name_code = pd.DataFrame(self.farm,index=['farm_name']).T
        self.farm_name_code['farm_code']=self.farm_name_code.index.tolist()
        self.farm_name_code.index=self.farm_name_code['farm_name'].tolist()
        # for (keys, val) in self.farm.items():
        #     self.comboBox_farm.addItem(str(keys), QVariant(keys))
    def onChecBoxFarmAllStateChanged(self):
        for index in range(1,self.farmListWidget.count()):
            check_box = self.farmListWidget.itemWidget(self.farmListWidget.item(index))
            if self.checkBoxfarmAll.isChecked():
                check_box.setCheckState(QtCore.Qt.Checked)
            else:
                check_box.setCheckState(QtCore.Qt.Unchecked)

    def onChecBoxWtgsAllStateChanged(self):
        for index in range(1,self.wtgsListWidget.count()):
            check_box = self.wtgsListWidget.itemWidget(self.wtgsListWidget.item(index))
            if self.checkBoxWtgsAll.isChecked():
                check_box.setCheckState(QtCore.Qt.Checked)
            else:
                check_box.setCheckState(QtCore.Qt.Unchecked)

    def refresh_power_data(self):

        startdatevalue = self.dateTimeEdit_startdate.date()
        enddatevalue = self.dateTimeEdit_enddate.dateTime().toTime_t() + 86400
        enddatevalue = QtCore.QDateTime.fromTime_t(enddatevalue).date()
        days_delta=(datetime.datetime.strptime(enddatevalue.toString("yyyy-MM-dd"),"%Y-%m-%d")-datetime.datetime.strptime(startdatevalue.toString("yyyy-MM-dd"),"%Y-%m-%d")).days
        farm_list = self.whichFarmIsChecked()  # 风场
        selected_farm = []
        if '全选' in farm_list:
            selected_farm = farm_list[1:]
        selected_wtgs = self.whichWtgsIsChecked()  # 机组
        if len(selected_farm) > 1 and selected_farm[0] != "全选":  #多个风场
            self.main_table.clear()  #清空主表
            label = ['编号','风场','发电量(ib)','发电量(集)','发电量(庚)','平均发电量(庚)','利用小时数(庚)','容量系数(庚)']
            farm_list=selected_farm
            self.main_table.setColumnCount(len(label))
            self.main_table.setRowCount(len(farm_list))
            self.main_table.setHorizontalHeaderLabels(label)
            self.main_table.verticalHeader().setVisible(False)
            for id in range(len(farm_list)):
                self.main_table.setItem(id, 0, QTableWidgetItem(farm_list[id]))
                self.main_table.setItem(id, 1, QTableWidgetItem(str(self.farm[farm_list[id]])))
                # print(not self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_ib'].tolist().remove('None'))
                # if not self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_ib'].tolist().remove('None'):
                self.main_table.setItem(id, 2, QTableWidgetItem('无'))
                # else:
                #     self.main_table.setItem(id, 2, QTableWidgetItem(str(sum(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_ib'].tolist()))))
                # if not self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_bd'].tolist().remove('None'):
                self.main_table.setItem(id, 3, QTableWidgetItem('无'))
                # else:
                #     self.main_table.setItem(id, 3, QTableWidgetItem(str(sum(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_bd'].tolist()))))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 4, QTableWidgetItem(str(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum())))
                else:
                    self.main_table.setItem(id, 4, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 5, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])]),2))))
                else:
                    self.main_table.setItem(id, 5, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 6, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])])/(1500 if str(self.farm[farm_list[id]])[0]=='1' else 2000),2))))
                else:
                    self.main_table.setItem(id, 6, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 7, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])])/(1500 if str(self.farm[farm_list[id]])[0]=='1' else 2000)/days_delta/24,2))))
                else:
                    self.main_table.setItem(id, 7, QTableWidgetItem('无'))
            self.main_table.verticalHeader().setVisible(False)
        else: # 单个风场
            self.main_table.clear()
            farm_code = self.farm[selected_farm[0]]
            query_wtgs_list = self.wtgs[str(farm_code)]
            # print(query_wtgs_list)
            mainlabel = ['机组','发电量(ib)','发电量(集控)','发电量(庚顿)','平均发电量(庚顿)','利用小时数(庚顿)','容量系数(庚顿)']
            self.main_table.setColumnCount(len(mainlabel))
            self.main_table.setRowCount(len(query_wtgs_list))
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            for id in range(len(query_wtgs_list)):
                self.main_table.setItem(id, 0, QTableWidgetItem(query_wtgs_list[id]))
                if self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_ib'].sum()>= 0:
                    self.main_table.setItem(id, 1, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_ib'].sum())))
                else:
                    self.main_table.setItem(id, 1, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_bd'].sum() >= 0:
                    self.main_table.setItem(id, 2, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_bd'].sum())))
                else:
                    self.main_table.setItem(id, 2, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 3, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum())))
                else:
                    self.main_table.setItem(id, 3, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 4, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/days_delta,2))))
                    self.main_table.setItem(id, 5, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/(1500 if query_wtgs_list[id][0]=='1' else 2000),2))))
                    self.main_table.setItem(id, 6, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/days_delta/24/(1500 if query_wtgs_list[id][0]=='1' else 2000),2))))
                else:
                    self.main_table.setItem(id, 4, QTableWidgetItem('无'))
                    self.main_table.setItem(id, 5, QTableWidgetItem('无'))
                    self.main_table.setItem(id, 6, QTableWidgetItem('无'))
            self.main_table.verticalHeader().setVisible(False)

    def refresh_fault_info_data(self):

        if self.comboBox_farm.currentText()=="全选":  #多个风场
            self.main_table.clear()  #清空主表
            label = ['编号','风场','故障次数','故障时间','无故障停机时间','平均故障次数','MTBF','MTBF(月)','可利用率']
            farm_list=list(self.farm.keys())
            self.main_table.setColumnCount(len(label))
            self.main_table.setRowCount(len(farm_list))
            self.main_table.setHorizontalHeaderLabels(label)
            self.main_table.verticalHeader().setVisible(False)
            for id in range(len(farm_list)):
                self.main_table.setItem(id, 0, QTableWidgetItem(farm_list[id]))
                self.main_table.setItem(id, 1, QTableWidgetItem(str(self.farm[farm_list[id]])))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_ib'].sum() >= 0:
                    self.main_table.setItem(id, 2, QTableWidgetItem(str(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_ib'].sum())))
                else:
                    self.main_table.setItem(id, 2, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_bd'].sum() >= 0:
                    self.main_table.setItem(id, 3, QTableWidgetItem(str(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_bd'].sum())))
                else:
                    self.main_table.setItem(id, 3, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 4, QTableWidgetItem(str(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum())))
                else:
                    self.main_table.setItem(id, 4, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 5, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])]),2))))
                else:
                    self.main_table.setItem(id, 5, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 6, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])])/(1500 if str(self.farm[farm_list[id]])[0]=='1' else 2000),2))))
                else:
                    self.main_table.setItem(id, 6, QTableWidgetItem('无'))
                if self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 7, QTableWidgetItem(str(round(self.query_res[self.query_res['farm_code'] == str(self.farm[farm_list[id]])]['power_golden'].sum()/len(self.wtgs[str(self.farm[farm_list[id]])])/(1500 if str(self.farm[farm_list[id]])[0]=='1' else 2000)/days_delta/24,2))))
                else:
                    self.main_table.setItem(id, 7, QTableWidgetItem('无'))
            self.main_table.verticalHeader().setVisible(False)
        else: # 单个风场
            self.main_table.clear()
            query_wtgs_list=sorted(list(set(self.query_res['wtgs_id'].tolist())))
            mainlabel = ['机组','发电量(ib)','发电量(集控)','发电量(庚顿)','平均发电量(庚顿)','利用小时数(庚顿)','容量系数(庚顿)']
            self.main_table.setColumnCount(len(mainlabel))
            self.main_table.setRowCount(len(query_wtgs_list))
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            for id in range(len(query_wtgs_list)):
                self.main_table.setItem(id, 0, QTableWidgetItem(query_wtgs_list[id]))
                if self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_ib'].sum()>= 0:
                    self.main_table.setItem(id, 1, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_ib'].sum())))
                else:
                    self.main_table.setItem(id, 1, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_bd'].sum() >= 0:
                    self.main_table.setItem(id, 2, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_bd'].sum())))
                else:
                    self.main_table.setItem(id, 2, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 3, QTableWidgetItem(str(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum())))
                else:
                    self.main_table.setItem(id, 3, QTableWidgetItem('无'))
                if self.query_res[self.query_res['wtgs_id'] == query_wtgs_list[id]]['power_golden'].sum() >= 0:
                    self.main_table.setItem(id, 4, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/days_delta,2))))
                    self.main_table.setItem(id, 5, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/(1500 if query_wtgs_list[id][0]=='1' else 2000),2))))
                    self.main_table.setItem(id, 6, QTableWidgetItem(str(round(self.query_res[self.query_res['wtgs_id']==query_wtgs_list[id]]['power_golden'].sum()/days_delta/24/(1500 if query_wtgs_list[id][0]=='1' else 2000),2))))
                else:
                    self.main_table.setItem(id, 4, QTableWidgetItem('无'))
                    self.main_table.setItem(id, 5, QTableWidgetItem('无'))
                    self.main_table.setItem(id, 6, QTableWidgetItem('无'))
            self.main_table.verticalHeader().setVisible(False)

    def refresh_utilize_info_data(self):

        if len(set(self.query_res['farm_code'].tolist())) > 1:

            self.main_table.clear()
            # self.sub_table.clear()
            # self.sub_table.setRowCount(0)

            label = ['风场', '风场编号', '可利用时间', '可利用率']
            farm_list = list(set(self.query_res['farm_name'].tolist()))
            self.main_table.setColumnCount(4)
            self.main_table.setRowCount(len(farm_list))
            self.main_table.setHorizontalHeaderLabels(label)
            self.main_table.verticalHeader().setVisible(False)

            for row in range(len(farm_list)):

                adata = self.query_res[self.query_res['farm_name'] == farm_list[row]]
                self.main_table.setItem(row, 0, QTableWidgetItem(farm_list[row]))
                self.main_table.setItem(row, 1, QTableWidgetItem(str(self.farm_name_code['farm_code'].loc[farm_list[row]])))
                self.main_table.setItem(row, 2, QTableWidgetItem(str(sum(adata['utilize_time'].tolist()))))
                self.main_table.setItem(row, 3, QTableWidgetItem(str(sum(adata['utilize'].tolist())/len(adata['utilize'].tolist()))))

        elif len(set(self.query_res['farm_code'].tolist())) == 1 and len(set(self.query_res['wtgs_id'].tolist())) == 1:

            self.main_table.clear()
            # self.sub_table.clear()

            mainlabel = ['风场', '风场编号', '可利用时间', '可利用率']
            self.main_table.setColumnCount(4)
            self.main_table.setRowCount(1)
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            self.main_table.verticalHeader().setVisible(False)
            self.main_table.setItem(0, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
            self.main_table.setItem(0, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
            self.main_table.setItem(0, 2, QTableWidgetItem(str(sum(self.query_res['utilize_time'].tolist())/len(self.query_res['utilize_time'].tolist()))))
            self.main_table.setItem(0, 3, QTableWidgetItem(str(sum(self.query_res['utilize'].tolist())/len(self.query_res['utilize'].tolist()))))

            # label = ['风场', '风场编号', '机组', '可利用时间', '可利用率']
            # self.sub_table.setColumnCount(5)
            # self.sub_table.setRowCount(1)
            # self.sub_table.setHorizontalHeaderLabels(label)
            # self.sub_table.verticalHeader().setVisible(False)
            # self.sub_table.setItem(0, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
            # self.sub_table.setItem(0, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
            # self.sub_table.setItem(0, 2, QTableWidgetItem(self.query_res['wtgs_id'].iloc[0]))
            # self.sub_table.setItem(0, 3, QTableWidgetItem(str(sum(self.query_res['utilize_time'].tolist())/len(self.query_res['utilize_time'].tolist()))))
            # self.sub_table.setItem(0, 4, QTableWidgetItem(str(sum(self.query_res['utilize'].tolist())/len(self.query_res['utilize'].tolist()))))


        elif len(set(self.query_res['farm_code'].tolist())) == 1 and len(set(self.query_res['wtgs_id'].tolist())) > 1:

            self.main_table.clear()
            # self.sub_table.clear()

            mainlabel = ['风场', '风场编号', '可利用时间', '可利用率']
            farm_list = list(set(self.query_res['farm_name'].tolist()))
            self.main_table.setColumnCount(3)
            self.main_table.setRowCount(1)
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            self.main_table.verticalHeader().setVisible(False)
            adata = self.query_res[self.query_res['farm_name'] == farm_list[0]]
            self.main_table.setItem(0, 0, QTableWidgetItem(farm_list[0]))
            self.main_table.setItem(0, 1, QTableWidgetItem(self.farm_name_code['farm_code'].loc[farm_list[0]]))
            self.main_table.setItem(0, 2, QTableWidgetItem(str(sum(adata['utilize_time'].tolist()))))
            self.main_table.setItem(0, 3, QTableWidgetItem(str(sum(adata['utilize'].tolist())/len(adata['utilize'].tolist()))))

            sublabel = ['风场', '风场编号', '机组', '可利用时间', '可利用率']
            wtgslist = sorted(
                list(set(self.query_res[self.query_res['farm_name'] == farm_list[0]]['wtgs_id'].tolist())))
            # self.sub_table.setColumnCount(5)
            # self.sub_table.setRowCount(len(wtgslist))
            # self.sub_table.setHorizontalHeaderLabels(sublabel)
            # self.sub_table.verticalHeader().setVisible(False)
            # for i in range(len(wtgslist)):
                # self.sub_table.setItem(i, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
                # self.sub_table.setItem(i, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
                # self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
                # self.sub_table.setItem(i, 3, QTableWidgetItem(
                #     str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize_time'].tolist()))))
                # self.sub_table.setItem(i, 4, QTableWidgetItem(
                #     str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize'].tolist())/len(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize'].tolist()))))

    def refresh_quality_data(self):
        if len(set(self.query_res['farm_code'].tolist())) > 1:

            self.main_table.clear()
            # self.sub_table.clear()
            # self.sub_table.setRowCount(0)

            label = ['风场', '风场编号', '通讯中断时间']
            farm_list = list(set(self.query_res['farm_name'].tolist()))
            self.main_table.setColumnCount(3)
            self.main_table.setRowCount(len(farm_list))
            self.main_table.setHorizontalHeaderLabels(label)
            self.main_table.verticalHeader().setVisible(False)

            for row in range(len(farm_list)):

                adata = self.query_res[self.query_res['farm_name'] == farm_list[row]]
                self.main_table.setItem(row, 0, QTableWidgetItem(farm_list[row]))
                self.main_table.setItem(row, 1, QTableWidgetItem(str(self.farm_name_code['farm_code'].loc[farm_list[row]])))
                self.main_table.setItem(row, 2, QTableWidgetItem(str(sum(adata['duration'].tolist()))))

        elif len(set(self.query_res['farm_code'].tolist())) == 1 and len(set(self.query_res['wtgs_id'].tolist())) == 1:

            self.main_table.clear()
            # self.sub_table.clear()

            mainlabel = ['风场', '风场编号', '通讯中断时间']
            self.main_table.setColumnCount(3)
            self.main_table.setRowCount(1)
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            self.main_table.verticalHeader().setVisible(False)
            self.main_table.setItem(0, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
            self.main_table.setItem(0, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
            self.main_table.setItem(0, 2, QTableWidgetItem(str(sum(self.query_res['duration'].tolist()))))

            label = ['风场', '风场编号', '机组', '通讯中断时间']
            # self.sub_table.setColumnCount(4)
            # self.sub_table.setRowCount(1)
            # self.sub_table.setHorizontalHeaderLabels(label)
            # self.sub_table.verticalHeader().setVisible(False)
            # self.sub_table.setItem(0, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
            # self.sub_table.setItem(0, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
            # self.sub_table.setItem(0, 2, QTableWidgetItem(self.query_res['wtgs_id'].iloc[0]))
            # self.sub_table.setItem(0, 3, QTableWidgetItem(str(sum(self.query_res['duration'].tolist()))))

        elif len(set(self.query_res['farm_code'].tolist())) == 1 and len(set(self.query_res['wtgs_id'].tolist())) > 1:

            self.main_table.clear()
            # self.sub_table.clear()

            mainlabel = ['风场', '风场编号', '通讯中断时间']
            farm_list = list(set(self.query_res['farm_name'].tolist()))
            self.main_table.setColumnCount(3)
            self.main_table.setRowCount(1)
            self.main_table.setHorizontalHeaderLabels(mainlabel)
            self.main_table.verticalHeader().setVisible(False)
            adata = self.query_res[self.query_res['farm_name'] == farm_list[0]]
            self.main_table.setItem(0, 0, QTableWidgetItem(farm_list[0]))
            self.main_table.setItem(0, 1, QTableWidgetItem(self.farm_name_code['farm_code'].loc[farm_list[0]]))
            self.main_table.setItem(0, 2, QTableWidgetItem(str(sum(adata['duration'].tolist()))))

            sublabel = ['风场', '风场编号', '机组', '通讯中断时间']
            wtgslist = sorted(
                list(set(self.query_res[self.query_res['farm_name'] == farm_list[0]]['wtgs_id'].tolist())))
            # self.sub_table.setColumnCount(4)
            # self.sub_table.setRowCount(len(wtgslist))
            # self.sub_table.setHorizontalHeaderLabels(sublabel)
            # self.sub_table.verticalHeader().setVisible(False)
            # for i in range(len(wtgslist)):
            #     self.sub_table.setItem(i, 0, QTableWidgetItem(self.query_res['farm_name'].iloc[0]))
            #     self.sub_table.setItem(i, 1, QTableWidgetItem(self.query_res['farm_code'].iloc[0]))
            #     self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
            #     self.sub_table.setItem(i, 3, QTableWidgetItem(str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['duration'].tolist()))))

    # @pyqtSlot(int)
    def on_comboBox_farm_activated(self):
        farm_name = self.whichFarmIsChecked()
        self.wtgsListWidget = QtWidgets.QListWidget()
        if len(farm_name)==1 and farm_name[0]!='全选':
            farm_code=self.farm[farm_name[0]]
            wtgs_list=self.wtgs[str(farm_code)]
            self.checkBoxWtgsAll = QtWidgets.QCheckBox('全选')
            self.wtgsListWidget.setItemWidget(QtWidgets.QListWidgetItem(self.wtgsListWidget), self.checkBoxWtgsAll)
            for (keys, val) in wtgs_list.items():
                self.wtgsListWidget.setItemWidget(QtWidgets.QListWidgetItem(self.wtgsListWidget),QtWidgets.QCheckBox(str(keys)))
            # print(self.checkBoxWtgsAll.isChecked())
            # self.checkBoxWtgsAll.stateChanged.connect(self.onChecBoxWtgsAllStateChanged())
            self.wtgsListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.comboBox_wtgs.setModel(self.wtgsListWidget.model())
            self.comboBox_wtgs.setView(self.wtgsListWidget)
        else:
            self.comboBox_wtgs.clear()
            self.comboBox_wtgs.addItem(u'全选')

    def whichFarmIsChecked(self):
        checkedFarmList=[]
        for index in range(0,self.farmListWidget.count()):
            check_box = self.farmListWidget.itemWidget(self.farmListWidget.item(index))
            if check_box.isChecked():
                checkedFarmList.append(check_box.text())
        return checkedFarmList

    def whichWtgsIsChecked(self):
        checkedWtgsList=[]
        index=1
        while index<self.wtgsListWidget.count():
            check_box = self.wtgsListWidget.itemWidget(self.wtgsListWidget.item(index))
            if check_box.isChecked():
                checkedWtgsList.append(check_box.text())
            index+=1
        return checkedWtgsList

    @pyqtSlot()
    def on_btn_save_clicked(self):
        output=[]
        RowCount=self.main_table.rowCount()
        ColCount=self.main_table.columnCount()
        if RowCount>0:
            for row in range(RowCount):
                ioutput=[]
                for col in range(ColCount):
                    ioutput.append(self.main_table.item(row, col).text())
                output.append(ioutput)
            if self.check_power.isChecked():
                output=pd.DataFrame(output,columns=['风场','编号','发电量(ib)','发电量(集)','发电量(庚)','平均发电量(庚)','利用小时数(庚)','容量系数(庚)'])
            elif self.check_fault_info.isChecked():
                output = pd.DataFrame(output,columns=['风场','故障次数','故障时间','无故障停机时间','平均故障次数','MTBF','MTBF(月)','可利用率'])
            else:
                output = pd.DataFrame(output)
            directory=self.path_open()
            output.to_excel(directory+".xlsx")
        else:
            QMessageBox.information(self, '提示', '表格内无数据！')
        QMessageBox.information(self, '提示', directory+".xlsx"+'\n保存成功！')

    def path_open(self):
        directory,ok = QFileDialog.getSaveFileName(self, "选取路径","C:/")
        return directory

    @pyqtSlot()
    def on_pushButton_query_clicked(self):
        self.btn_query=1
        self.main_table.clear()
        farm_list = self.whichFarmIsChecked()#风场
        if '全选' in farm_list:
            selected_farm = farm_list[1:]
        else:
            selected_farm = farm_list
        selected_wtgs = self.whichWtgsIsChecked()#机组
        # selected_farm=self.comboBox_farm.currentText() #风场
        # selected_wtgs=self.comboBox_wtgs.currentText() #机组
        startdatevalue=self.dateTimeEdit_startdate.date() #开始时间
        enddatevalue = self.dateTimeEdit_enddate.date() #结束时间
        # enddatevalue=self.dateTimeEdit_enddate.dateTime().toTime_t()+ 86400
        # enddatevalue=QtCore.QDateTime.fromTime_t(enddatevalue).date()
        if startdatevalue>enddatevalue:
            QMessageBox.question(self, "消息", "开始时间大于结束时间，请重新选择！",  QMessageBox.Yes | QMessageBox.No)
        elif not (self.check_power.isChecked() or self.check_fault_info.isChecked() or self.check_utilize.isChecked() or self.check_quality.isChecked()):
            QMessageBox.question(self, "消息", "请选择项目！", QMessageBox.Yes | QMessageBox.No)
        else:
            queryfiledcon={}
            if len(selected_farm) > 0 and selected_farm[0] != "全选":
                queryfiledcon['farm_code'] = [str(self.farm[farm_name]) for farm_name in selected_farm]  # 风场编号列表
            if len(selected_wtgs) > 0 and selected_wtgs[0] != "全选":
                queryfiledcon['wtgs_id'] = selected_wtgs
            queryfiledcon['start_time'] = startdatevalue.toString("yyyy-MM-dd")
            queryfiledcon['end_time'] = enddatevalue.toString("yyyy-MM-dd")
            if self.check_power.isChecked():
                queryfiledcon['db']='power'
                # print(queryfiledcon)
                self.query_res= dataIO.power2(queryfiledcon)  # 根据条件查询电量
                if len(self.query_res)>0:
                    self.refresh_power_data()
                else:
                    QMessageBox.information(self,'提示','查询期间内无数据，请重新选择开始结束时间！')
            elif self.check_fault_info.isChecked():
                queryfiledcon['db'] ='fault_info'
                # print(queryfiledcon)
                self.query_res = wtgs_fault.fault_query(queryfiledcon)
                if len(self.query_res):
                    self.refresh_fault_info_data()
                else:
                    QMessageBox.information(self,'提示','查询期间内无数据，请重新选择开始结束时间！')
            elif self.check_utilize.isChecked():
                queryfiledcon['db'] ='utilize'
                self.query_res = dataIO.utilize(queryfiledcon)
                if len(self.query_res):
                    self.refresh_utilize_info_data()
                else:
                    QMessageBox.information(self,'提示','查询期间内无数据，请重新选择开始结束时间！')
            elif self.check_quality.isChecked():
                queryfiledcon['db'] ='quality'
                self.query_res = dataIO.com_quality(queryfiledcon)
                if len(self.query_res):
                    self.refresh_quality_data()
                else:
                    QMessageBox.information(self,'提示','查询期间内无数据，请重新选择开始结束时间！')

        for row in range(self.main_table.rowCount()):
            for column in range(self.main_table.columnCount()):
                self.main_table.item(row, column).setTextAlignment(Qt.AlignCenter)

    @pyqtSlot()
    def on_pushButton_cal_clicked(self):

        if self.pushButton_cal.text()=="计   算":
            farm_list=self.whichFarmIsChecked()
            if '全选' in farm_list:
                farm_list=farm_list[1:]
            wtgs_list=self.whichWtgsIsChecked()
            # farmvalue = self.comboBox_farm.currentText()
            # wtgsvalue = self.comboBox_wtgs.currentText()
            startdatevalue = self.dateTimeEdit_startdate.date()
            enddatevalue = self.dateTimeEdit_enddate.dateTime().toTime_t() + 86400
            enddatevalue = QtCore.QDateTime.fromTime_t(enddatevalue).date()
            if startdatevalue > enddatevalue:
                QMessageBox.question(self, "消息", "开始时间大于结束时间，请重新选择！", QMessageBox.Yes | QMessageBox.No)
            elif not (self.check_power.isChecked() or self.check_fault_info.isChecked() or self.check_utilize.isChecked() or self.check_quality.isChecked()):
                QMessageBox.question(self, "消息", "请选择项目！", QMessageBox.Yes | QMessageBox.No)
            else:
                calfiledcon = {}
                if len(farm_list)>0 and farm_list[0] != "全选":
                    calfiledcon['farm_code'] = [str(self.farm[farm_name]) for farm_name in farm_list] #风场编号列表
                if len(wtgs_list)>0 and wtgs_list[0] != "全选":
                    calfiledcon['wtgs_id'] = wtgs_list
                calfiledcon['start_time'] = startdatevalue.toString("yyyy-MM-dd")
                calfiledcon['end_time'] = enddatevalue.toString("yyyy-MM-dd")

                if self.check_power.isChecked(): # 计算发电量
                    if not (self.check_power_ib.isChecked() or self.check_power_bd.isChecked() or self.check_power_golden.isChecked()):
                        QMessageBox.question(self, "消息", "请选择计算数据来源！", QMessageBox.Yes | QMessageBox.No)
                    else:
                        calfiledcon['db'] = 'power'
                        if self.check_power_ib.isChecked(): # ib数据库
                            self.label_progress_bar_ib.setVisible(True)
                            self.progress_bar_ib.setVisible(True)
                            self.thread0=wtgs_power.calculate_multi_thread_ib(calfiledcon)
                            self.thread0.finishedSignal.connect(self.progress_bar_ib_update)
                            self.thread0.textinfo.connect(self.text_browser_update)
                            self.thread0.start()

                        elif self.check_power_bd.isChecked(): # 集控系统
                            self.label_progress_bar_bd.setVisible(True)
                            self.progress_bar_bd.setVisible(True)
                            self.thread1 = wtgs_power.calculate_multi_thread_bd(calfiledcon)
                            self.thread1.finishedSignal.connect(self.progress_bar_bd_update)
                            self.thread1.textinfo.connect(self.text_browser_update)
                            self.thread1.start()

                        else :  # 庚顿数据库
                            self.label_progress_bar_golden.setVisible(True)
                            self.progress_bar_golden.setVisible(True)
                            self.thread2 = wtgs_power.calculate_multi_thread_golden(calfiledcon)
                            self.thread2.finishedSignal.connect(self.progress_bar_golden_update)
                            self.thread2.textinfo.connect(self.text_browser_update)
                            self.thread2.start()

                elif self.check_fault_info.isChecked(): # 计算故障信息
                    self.label_progress_bar_ib.setVisible(1)
                    self.label_progress_bar_ib.setText('故障')
                    self.label_progress_bar_bd.setVisible(0)
                    self.label_progress_bar_golden.setVisible(0)
                    self.progress_bar_ib.setVisible(1)
                    self.progress_bar_bd.setVisible(0)
                    self.progress_bar_golden.setVisible(0)
                    calfiledcon['db'] = 'fault_info'
                    self.thread0 = wtgs_fault.cal_sub_thread(calfiledcon)
                    self.thread0.finishedSignal.connect(self.progress_bar_ib_update)
                    self.thread0.textinfo.connect(self.text_browser_update)
                    self.thread0.start()

                elif self.check_utilize.isChecked(): # 计算可利用率
                    calfiledcon['db'] = 'utilize'
                    self.query_res = dataIO.utilize(calfiledcon)
                    self.refresh_utilize_info_data()

                elif self.check_quality.isChecked(): # 计算通讯质量
                    calfiledcon['db'] = 'quality'
                    self.query_res = dataIO.com_quality(calfiledcon)
                    self.refresh_quality_data()
        elif self.pushButton_cal.text() == "中   断":
            self.pushButton_cal.setText(u"计   算")
            if self.check_power_ib.isChecked():
                pass
            elif self.check_power_bd.isChecked():
                pass
            elif self.check_power_golden.isChecked():
                pass
            else:
                pass

    def text_browser_update(self,info):
        self.log_window.append(info)

    def progress_bar_ib_update(self, value):
        self.progress_bar_ib.setVisible(True)
        self.progress_bar_ib.setValue(value)

    def progress_bar_bd_update(self, value):
        self.progress_bar_bd.setValue(value)

    def progress_bar_golden_update(self, value):
        self.progress_bar_golden.setValue(value)


    def check_state_change(self):

        self.check_power.stateChanged.connect(self.check_powerStateChanged)
        self.check_fault_info.stateChanged.connect(self.check_fault_infoStateChanged)
        self.check_utilize.stateChanged.connect(self.check_utilizeStateChanged)
        self.check_quality.stateChanged.connect(self.check_qualityStateChanged)
        self.check_avg_speed.stateChanged.connect(self.check_avgSpeedStateChanged)

    def check_powerStateChanged(self):

        if self.check_power.isChecked():
            self.check_fault_info.setCheckState(QtCore.Qt.Unchecked)
            self.check_utilize.setCheckState(QtCore.Qt.Unchecked)
            self.check_quality.setCheckState(QtCore.Qt.Unchecked)
            self.check_avg_speed.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setDisabled(False)
            self.check_power_bd.setDisabled(False)
            self.check_power_golden.setDisabled(False)
            self.btn_query=0

    def check_fault_infoStateChanged(self):

        if self.check_fault_info.isChecked():
            self.check_power.setCheckState(QtCore.Qt.Unchecked)
            self.check_utilize.setCheckState(QtCore.Qt.Unchecked)
            self.check_quality.setCheckState(QtCore.Qt.Unchecked)
            self.check_avg_speed.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_bd.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_golden.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setDisabled(True)
            self.check_power_bd.setDisabled(True)
            self.check_power_golden.setDisabled(True)
            self.btn_query = 0

    def check_utilizeStateChanged(self):

        if self.check_utilize.isChecked():
            self.check_fault_info.setCheckState(QtCore.Qt.Unchecked)
            self.check_power.setCheckState(QtCore.Qt.Unchecked)
            self.check_quality.setCheckState(QtCore.Qt.Unchecked)
            self.check_avg_speed.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_bd.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_golden.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setDisabled(True)
            self.check_power_bd.setDisabled(True)
            self.check_power_golden.setDisabled(True)
            self.btn_query = 0

    def check_qualityStateChanged(self):

        if self.check_quality.isChecked():
            self.check_fault_info.setCheckState(QtCore.Qt.Unchecked)
            self.check_utilize.setCheckState(QtCore.Qt.Unchecked)
            self.check_power.setCheckState(QtCore.Qt.Unchecked)
            self.check_avg_speed.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_bd.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_golden.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setDisabled(True)
            self.check_power_bd.setDisabled(True)
            self.check_power_golden.setDisabled(True)
            self.btn_query = 0

    def check_avgSpeedStateChanged(self):

        if self.check_avg_speed.isChecked():
            self.check_fault_info.setCheckState(QtCore.Qt.Unchecked)
            self.check_utilize.setCheckState(QtCore.Qt.Unchecked)
            self.check_quality.setCheckState(QtCore.Qt.Unchecked)
            self.check_power.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_bd.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_golden.setCheckState(QtCore.Qt.Unchecked)
            self.check_power_ib.setDisabled(True)
            self.check_power_bd.setDisabled(True)
            self.check_power_golden.setDisabled(True)
            self.btn_query = 0

    @pyqtSlot()
    def on_set_ib_triggered(self):

        self.dailog = set_db()
        self.dailog.show()

    @pyqtSlot()
    def on_warning_statis_triggered(self):

        dialog = QtWidgets.QDialog()
        ui_form_warning_statis = Ui_Form_warning_statis()
        ui_form_warning_statis.setupUi(dialog)
        dialog.show()
        dialog.exec_()

    @pyqtSlot()
    def on_com_quality_triggered(self):

        self.dailog = qua_com()
        self.dailog.show()

    @pyqtSlot()
    def on_set_exit_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # close the application
        reply = self.msg()
        if reply==QMessageBox.Yes:
            self.close() #close the application


    def msg(self):
        reply = QMessageBox.question(self, "消息", "退出程序?",  QMessageBox.Yes | QMessageBox.No)
        return reply

    @pyqtSlot()
    def on_help_manual_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        dialog = QtWidgets.QDialog()
        ui_form_manual = Ui_Form_manual()
        ui_form_manual.setupUi(dialog)
        dialog.show()
        dialog.exec_()

    @pyqtSlot()
    def on_help_maintain_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        dialog = QtWidgets.QDialog()
        # ui_form_maintain = Ui_Form_maintain()
        # ui_form_maintain.setupUi(dialog)
        dialog.show()
        dialog.exec_()

    @pyqtSlot()
    def on_set_login_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_set_action_list_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.dailog = set_db2()
        self.dailog.show()

    def week_get(self,today):

        weekEN2CH={'0':'一','1':'二','2':'三','3':'四','4':'五','5':'六','6':'日'}
        dayscount=datetime.timedelta(days=today.isoweekday())
        dayfrom=today-dayscount+datetime.timedelta(days=1)
        datto=today-dayscount+datetime.timedelta(days=7)
        week7={}
        i=0
        while i<=6:
            date=str(dayfrom+datetime.timedelta(days=i))
            week7['星期'+weekEN2CH[str(i)]]=date
            i+=1
        return week7

    def week_warning_data(self):

        res=mainWindowData.warning_table_data(self.weekday)
        warning_info_as_week={}
        key_list=list(self.weekday.keys())
        for key in self.weekday.keys():
            warning_info_as_week[key]=[]

        for iinfo in res:
            for index in range(len(key_list)):
                if index!=6:
                    if iinfo[3] >= self.weekday[key_list[index]] and iinfo[3] <= self.weekday[key_list[index + 1]]:
                        warning_info_as_week[key_list[index]].append(' '.join(iinfo))
                        break
                    else:
                        continue
                else:
                    if iinfo[3]>=self.weekday[key_list[index]]:
                        warning_info_as_week[key_list[index]].append(' '.join(iinfo))
                        break
                    else:
                        continue
        return warning_info_as_week

    @pyqtSlot(int,int)
    def on_main_table_cellClicked(self, row, column):
        if self.check_power.isChecked():
            if self.btn_query == 1:
                # self.sub_table.clear()
                sublabel = ['风场', '风场编号', '机组', '发电量']
                wtgslist = sorted(list(set(self.query_res[self.query_res['farm_name'] == self.main_table.item(row, 0).text()]['wtgs_id'].tolist())))
                # self.sub_table.setColumnCount(4)
                # self.sub_table.setRowCount(len(wtgslist))
                # self.sub_table.setHorizontalHeaderLabels(sublabel)
                # self.sub_table.verticalHeader().setVisible(False)
                # for i in range(len(wtgslist)):
                #     self.sub_table.setItem(i, 0, QTableWidgetItem(self.main_table.item(row, 0).text()))
                #     self.sub_table.setItem(i, 1, QTableWidgetItem(self.main_table.item(row, 1).text()))
                #     self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
                #     self.sub_table.setItem(i, 3, QTableWidgetItem(str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['power'].tolist()))))
            else:
                QMessageBox.information(self,'提示','请先点击查询按钮！')

        elif self.check_fault_info.isChecked():
            if self.btn_query == 1:
                pass
                # self.sub_table.clear()
                # sublabel = ['风场', '风场编号', '机组', '故障次数','故障时间']
                # wtgslist = sorted(list(set(self.query_res[self.query_res['farm_name'] == self.main_table.item(row, 0).text()]['wtgs_id'].tolist())))
                # self.sub_table.setColumnCount(5)
                # self.sub_table.setRowCount(len(wtgslist))
                # self.sub_table.setHorizontalHeaderLabels(sublabel)
                # self.sub_table.verticalHeader().setVisible(False)
                # for i in range(len(wtgslist)):
                #     self.sub_table.setItem(i, 0, QTableWidgetItem(self.main_table.item(row, 0).text()))
                #     self.sub_table.setItem(i, 1, QTableWidgetItem(self.main_table.item(row, 1).text()))
                #     self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
                #     self.sub_table.setItem(i, 3, QTableWidgetItem(str(len(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]))))
                #     self.sub_table.setItem(i, 4, QTableWidgetItem(str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['duration'].tolist()))))
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')
        elif self.check_utilize.isChecked():
            if self.btn_query == 1:
                # self.sub_table.clear()
                sublabel = ['风场', '风场编号', '机组', '可利用时间', '可利用率']
                wtgslist = sorted(list(set(self.query_res[self.query_res['farm_name'] == self.main_table.item(row, 0).text()]['wtgs_id'].tolist())))
                # self.sub_table.setColumnCount(5)
                # self.sub_table.setRowCount(len(wtgslist))
                # self.sub_table.setHorizontalHeaderLabels(sublabel)
                # self.sub_table.verticalHeader().setVisible(False)
                # for i in range(len(wtgslist)):
                #     self.sub_table.setItem(i, 0, QTableWidgetItem(self.main_table.item(row, 0).text()))
                #     self.sub_table.setItem(i, 1, QTableWidgetItem(self.main_table.item(row, 1).text()))
                #     self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
                #     self.sub_table.setItem(i, 3, QTableWidgetItem(
                #         str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize_time'].tolist()))))
                #     self.sub_table.setItem(i, 4, QTableWidgetItem(
                #         str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize'].tolist())/len(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['utilize'].tolist()))))
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')
        else:
            if self.btn_query == 1:
                # self.sub_table.clear()
                sublabel = ['风场', '风场编号', '机组', '通讯中断时间']
                wtgslist = sorted(list(set(self.query_res[self.query_res['farm_name'] == self.main_table.item(row, 0).text()]['wtgs_id'].tolist())))
                # self.sub_table.setColumnCount(4)
                # self.sub_table.setRowCount(len(wtgslist))
                # self.sub_table.setHorizontalHeaderLabels(sublabel)
                # self.sub_table.verticalHeader().setVisible(False)
                # for i in range(len(wtgslist)):
                #     self.sub_table.setItem(i, 0, QTableWidgetItem(self.main_table.item(row, 0).text()))
                #     self.sub_table.setItem(i, 1, QTableWidgetItem(self.main_table.item(row, 1).text()))
                #     self.sub_table.setItem(i, 2, QTableWidgetItem(wtgslist[i]))
                #     self.sub_table.setItem(i, 3, QTableWidgetItem(str(sum(self.query_res[self.query_res['wtgs_id'] == wtgslist[i]]['duration'].tolist()))))
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')

        # for row in range(self.sub_table.rowCount()):
        #     for column in range(self.sub_table.columnCount()):
        #         self.sub_table.item(row, column).setTextAlignment(Qt.AlignCenter)

    @pyqtSlot(int, int)
    def on_sub_table_cellClicked(self, row, column):

        if self.check_power.isChecked():

            if self.btn_query == 1:
                self.dialog = query(self.query_res, self.sub_table.item(row, 2).text())
                self.dialog.show()
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')

        elif self.check_fault_info.isChecked():

            if self.btn_query == 1:
                self.dialog = wtgs_fault(self.query_res, self.sub_table.item(row, 2).text())
                self.dialog.show()
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')

        elif self.check_utilize.isChecked():

            if self.btn_query == 1:
                self.dialog = wtgs_utilize(self.query_res, self.sub_table.item(row, 2).text())
                self.dialog.show()
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')

        elif self.check_quality.isChecked():

            if self.btn_query == 1:
                self.dialog = com_quality(self.query_res, self.sub_table.item(row, 2).text())
                self.dialog.show()
            else:
                QMessageBox.information(self, '提示', '请先点击查询按钮！')

        else:
            QMessageBox.information(self, '提示', '请先选择KPI指标！')
        
if __name__=="__main__":

    app=QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
    
