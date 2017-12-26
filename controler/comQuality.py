# -*- coding: utf-8 -*-

"""
Module implementing qua_com.
"""

import datetime
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import dataIO
from view.Ui_Form_qua_com import Ui_Form_qua_com

DATETIME_FORMAT = "yyyy-MM-dd"

class qua_com(QWidget, Ui_Form_qua_com):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(qua_com, self).__init__(parent)
        self.setupUi(self)
        self.initial_date_data()
        self.initial_farm_wtgs()
        
    def initial_date_data(self):
        #set start and end date as the current date
        self.dateTimeEdit_startdate_qua_com.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime()), 'yyyy-MM-dd'))
        self.dateTimeEdit_startdate_qua_com.setDisplayFormat(DATETIME_FORMAT)
        self.dateTimeEdit_startdate_qua_com.setCalendarPopup(True)
        self.dateTimeEdit_enddate_qua_com.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime()), 'yyyy-MM-dd'))
        self.dateTimeEdit_enddate_qua_com.setDisplayFormat(DATETIME_FORMAT)
        self.dateTimeEdit_enddate_qua_com.setCalendarPopup(True)
        
    def initial_farm_wtgs(self):    
        #set option for farm and wtgs
        self.comboBox_farm_qua_com.clear() # 清空items
        self.comboBox_wtgs_qua_com.clear() # 清空items
        self.comboBox_farm_qua_com.addItem(u'全部')
        self.comboBox_wtgs_qua_com.addItem(u'全部')
        
        # initial the items of comboBox_farm
        
        (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
        for (keys, val) in self.farm.items():
            self.comboBox_farm_qua_com.addItem(val, QVariant(keys))
                
    def update_table_data(self, data):
        
        if len(data)>0:
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.tableWidget.setItem(i,j, QTableWidgetItem(str(data[i][j])))
        else:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
    
    @pyqtSlot(int)
    def on_comboBox_farm_qua_com_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        if self.comboBox_farm_qua_com.currentText()!="全部":
            (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
            index=self.comboBox_farm_qua_com.currentIndex()
            intdata=self.comboBox_farm_qua_com.itemData(index)
            self.comboBox_wtgs_qua_com.clear()
            self.comboBox_wtgs_qua_com.addItem(u'全部')
            for (keys, val) in self.wtgs[intdata].items(): 
                self.comboBox_wtgs_qua_com.addItem(val, QVariant(keys))
    
    @pyqtSlot(int)
    def on_comboBox_farm_qua_com_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        self.comboBox_wtgs_qua_com.clear()
        self.comboBox_wtgs_qua_com.addItem(u'全部')
        
    @pyqtSlot()
    def on_queryButton_qua_com_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        farmvalue=self.comboBox_farm_qua_com.currentText()
        wtgsvalue=self.comboBox_wtgs_qua_com.currentText()
        startdatevalue=self.dateTimeEdit_startdate_qua_com.date()
        enddatevalue=self.dateTimeEdit_enddate_qua_com.dateTime().toTime_t()+ 86400
        enddatevalue=QtCore.QDateTime.fromTime_t(enddatevalue).date()
        startdatetime=datetime.datetime.strptime(startdatevalue.toString("yyyy-MM-dd"), '%Y-%m-%d')
        enddatetime=datetime.datetime.strptime(enddatevalue.toString("yyyy-MM-dd"), '%Y-%m-%d')
        delta=enddatetime-startdatetime
 
        if startdatevalue>enddatevalue:
            QMessageBox.question(self, "消息", "开始时间大于结束时间，请重新选择！",  QMessageBox.Yes | QMessageBox.No)
            
        else:
            if farmvalue=="全部" and wtgsvalue=="全部":#全风场
                res= dataIO.farm_name_server()
                res1= dataIO.com_data(res, startdatevalue, enddatevalue, delta.days)
                if len(res1)>0:
                    self.tableWidget_qua_com.setRowCount(len(res1))
                    self.tableWidget_qua_com.setColumnCount(len(res1[0]))
                    for i in range(len(res1)):
                        for j in range(len(res1[0])):
                            self.tableWidget_qua_com.setItem(i,j, QTableWidgetItem(str(res1[i][j])))
                else:
                    self.tableWidget_qua_com.clear()
                    self.tableWidget_qua_com.setRowCount(1)
                    self.tableWidget_qua_com.setColumnCount(1)
                    self.tableWidget_qua_com.setItem(0,0, QTableWidgetItem("无数据"))
                            
            if farmvalue!="全部" and wtgsvalue=="全部":#某风场
                res1= dataIO.com_data2(farmvalue, startdatevalue, enddatevalue, delta.days)
                if len(res1)>0:
                    self.tableWidget_qua_com.setRowCount(len(res1))
                    self.tableWidget_qua_com.setColumnCount(len(res1[0]))
                    for i in range(len(res1)):
                        for j in range(len(res1[0])):
                            self.tableWidget_qua_com.setItem(i,j, QTableWidgetItem(str(res1[i][j])))
                else:
                    self.tableWidget_qua_com.clear()
                    self.tableWidget_qua_com.setRowCount(1)
                    self.tableWidget_qua_com.setColumnCount(1)
                    self.tableWidget_qua_com.setItem(0,0, QTableWidgetItem("无数据"))
                
            if farmvalue!="全部" and wtgsvalue!="全部":#某机组
                res1= dataIO.com_data3(farmvalue, wtgsvalue, startdatevalue, enddatevalue, delta.days)
                if len(res1)>0:
                    self.tableWidget_qua_com.setRowCount(len(res1))
                    self.tableWidget_qua_com.setColumnCount(len(res1[0]))
                    for i in range(len(res1)):
                        for j in range(len(res1[0])):
                            self.tableWidget_qua_com.setItem(i,j, QTableWidgetItem(str(res1[i][j])))
                else:
                    self.tableWidget_qua_com.clear()
                    self.tableWidget_qua_com.setRowCount(1)
                    self.tableWidget_qua_com.setColumnCount(1)
                    self.tableWidget_qua_com.setItem(0,0, QTableWidgetItem("无数据"))
                
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=qua_com()
    uset_db.show()
    sys.exit(app.exec_())
