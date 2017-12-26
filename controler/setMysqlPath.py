# -*- coding: utf-8 -*-

"""
Module implementing set_db.
"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import dataIO
from view.Ui_Form_set_db import Ui_Form_set_db


class set_db(QWidget, Ui_Form_set_db):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
#        if not self.isVisible():
#            self.show()
        super(set_db, self).__init__(parent)
        self.setupUi(self)
        self.initial_farm_wtgs()
    
    @pyqtSlot(int)
    def on_comboBox_farm_set_db_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        # TODO: not implemented yet
        if self.comboBox_farm_set_db.currentText()!="全部":
            (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
            index=self.comboBox_farm_set_db.currentIndex()
            intdata=self.comboBox_farm_set_db.itemData(index)
            self.comboBox_wtgs_set_db.clear()
            self.comboBox_wtgs_set_db.addItem(u'全部')
            for (keys, val) in self.wtgs[intdata].items(): 
                self.comboBox_wtgs_set_db.addItem(val, QVariant(keys))
    
    @pyqtSlot()
    def on_query_Button_set_db_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        farmvalue=self.comboBox_farm_set_db.currentText()
        wtgsvalue=self.comboBox_wtgs_set_db.currentText()

        queryfiledcon=[]
        
        if farmvalue!="全部":
            queryfiledcon.append("farm_name=\'"+farmvalue+"\'")
        if wtgsvalue!="全部":
            queryfiledcon.append("wtgs_id=\'"+wtgsvalue+"\'")
        
        res= dataIO.query_data_set_db(queryfiledcon)
        
        self.update_table_data(res)
    
    def initial_farm_wtgs(self):    
        #set option for farm and wtgs
        self.comboBox_farm_set_db.clear() # 清空items
        self.comboBox_wtgs_set_db.clear() # 清空items
        self.comboBox_farm_set_db.addItem(u'全部')
        self.comboBox_wtgs_set_db.addItem(u'全部')
        
        # initial the items of comboBox_farm
        
        (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
        for (keys, val) in self.farm.items():
            self.comboBox_farm_set_db.addItem(val, QVariant(keys))
        
    def update_table_data(self, data):
        
        if len(data)>0:
            self.tableWidget_set_db.setRowCount(len(data))
            self.tableWidget_set_db.setColumnCount(len(data[0]))
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.tableWidget_set_db.setItem(i,j, QTableWidgetItem(str(data[i][j])))
        else:
            self.tableWidget_set_db.clear()
            self.tableWidget_set_db.setRowCount(0)
            
        #set the base infomation(width,height) about tablewidget
        Header = ["风场","代号","机组ID","IP","端口", "数据库", "表", "机组号"]
        self.tableWidget_set_db.setHorizontalHeaderLabels(Header)
        for index in range(self.tableWidget_set_db.columnCount()):
            headItem = self.tableWidget_set_db.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
        self.tableWidget_set_db.setColumnWidth(0,170)
        self.tableWidget_set_db.setColumnWidth(1,55) 
        self.tableWidget_set_db.setColumnWidth(2,90) 
        self.tableWidget_set_db.setColumnWidth(3,100) 
        self.tableWidget_set_db.setColumnWidth(4,45) 
        self.tableWidget_set_db.setColumnWidth(5,90)
        self.tableWidget_set_db.setColumnWidth(6,90) 
        self.tableWidget_set_db.setColumnWidth(7,60)
        self.tableWidget_set_db.setSelectionBehavior(QTableWidget.SelectRows )
            

    @pyqtSlot(int)
    def on_comboBox_farm_set_db_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        self.comboBox_wtgs_set_db.clear()
        self.comboBox_wtgs_set_db.addItem(u'全部')
        

if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=set_db()
    uset_db.show()
    sys.exit(app.exec_())
