# -*- coding: utf-8 -*-

"""
Module implementing set_db2.
"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import dataIO
from view.Ui_Form_set_db2 import Ui_Form_set_db2


class set_db2(QWidget, Ui_Form_set_db2):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(set_db2, self).__init__(parent)
        self.setupUi(self)
        self.initial_farm_wtgs()
    
    @pyqtSlot(int)
    def on_comboBox_farm_set_db2_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        if self.comboBox_farm_set_db2.currentText()!="全部":
            (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
            index=self.comboBox_farm_set_db2.currentIndex()
            intdata=self.comboBox_farm_set_db2.itemData(index)
            self.comboBox_wtgs_set_db2.clear()
            self.comboBox_wtgs_set_db2.addItem(u'全部')
            for (keys, val) in self.wtgs[intdata].items(): 
                self.comboBox_wtgs_set_db2.addItem(val, QVariant(keys))
    
    @pyqtSlot(int)
    def on_comboBox_farm_set_db2_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        self.comboBox_wtgs_set_db2.clear()
        self.comboBox_wtgs_set_db2.addItem(u'全部')
    
    @pyqtSlot()
    def on_query_Button_set_db_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        farmvalue=self.comboBox_farm_set_db2.currentText()
        wtgsvalue=self.comboBox_wtgs_set_db2.currentText()

        queryfiledcon=[]
        
        if farmvalue!="全部":
            queryfiledcon.append("FARM_NAME_CH=\'"+farmvalue+"\'")
        if wtgsvalue!="全部":
            queryfiledcon.append("WTGS_ID=\'"+wtgsvalue+"\'")
        print(queryfiledcon)
        res= dataIO.query_data_set_db2(queryfiledcon)
        
        self.update_table_data(res)
        
    def initial_farm_wtgs(self):    
        #set option for farm and wtgs
        self.comboBox_farm_set_db2.clear() # 清空items
        self.comboBox_wtgs_set_db2.clear() # 清空items
        self.comboBox_farm_set_db2.addItem(u'全部')
        self.comboBox_wtgs_set_db2.addItem(u'全部')
        
        # initial the items of comboBox_farm
        
        (self.farm, self.wtgs)= dataIO.farmcodeDirectory()
        for (keys, val) in self.farm.items():
            self.comboBox_farm_set_db2.addItem(val, QVariant(keys))
            
    def update_table_data(self, data):
        
        if len(data)>0:
            self.tableWidget_set_db2.setRowCount(len(data))
            self.tableWidget_set_db2.setColumnCount(len(data[0]))
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.tableWidget_set_db2.setItem(i,j, QTableWidgetItem(str(data[i][j])))
        else:
            self.tableWidget_set_db2.clear()
            self.tableWidget_set_db2.setRowCount(0)
            
if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=set_db2()
    uset_db.show()
    sys.exit(app.exec_())
