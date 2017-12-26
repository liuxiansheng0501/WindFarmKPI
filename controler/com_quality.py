# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import config
import connectDB
from view.Ui_Form_com_quality import Ui_com_quality


class com_quality(QWidget, Ui_com_quality):

    def __init__(self, com_quality_info, wtgs_id, parent=None):

        super(com_quality, self).__init__(parent)

        self.argv_cfg=config.argv_cfg()

        self.wtgs_id=wtgs_id

        self.com_quality_info=com_quality_info

        self.setupUi(self)

        self.__initial_combobox__()

        self.__initial_com_quality__()

    def  __initial_combobox__(self):

        cmp_wtgs_group=list(set(self.com_quality_info[self.com_quality_info['farm_code'] == self.wtgs_id[0:5]]['wtgs_id'].tolist()))

        self.plistwidget_wtgs=QtWidgets.QListWidget()

        self.check_box_wtgs=QtWidgets.QCheckBox('全选')

        self.check_box_wtgs.stateChanged.connect(self.on_check_box_wtgs_stateChanged)

        self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), self.check_box_wtgs)

        for wtgs_name in cmp_wtgs_group:

            self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), QtWidgets.QCheckBox(wtgs_name))

        self.plistwidget_wtgs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.combobox_wtgs.setModel(self.plistwidget_wtgs.model())

        self.combobox_wtgs.setView(self.plistwidget_wtgs)

    def  __initial_com_quality__(self):

        self.info_table.clear()

        self.com_quality_data = self.com_quality_info[self.com_quality_info['wtgs_id'] == self.wtgs_id]

        label = ['机组号', '开始时间', '结束时间', '持续时间', '备注']

        self.info_table.setColumnCount(5)

        self.info_table.setRowCount(len(self.com_quality_data))

        self.info_table.setHorizontalHeaderLabels(label)

        self.info_table.verticalHeader().setVisible(False)

        self.com_quality_data.sort(columns='start_time')

        for row in range(len(self.com_quality_data)):

            self.info_table.setItem(row, 0, QTableWidgetItem(self.com_quality_data['wtgs_id'].iloc[row]))

            self.info_table.setItem(row, 1, QTableWidgetItem(self.com_quality_data['start_time'].iloc[row]))

            self.info_table.setItem(row, 2, QTableWidgetItem(str(self.com_quality_data['end_time'].iloc[row])))

            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.com_quality_data['duration'].iloc[row])))

            self.info_table.setItem(row, 4, QTableWidgetItem(str(self.com_quality_data['reason'].iloc[row])))

        self.info_table.resizeColumnsToContents()

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

        if self.info_table.item(lastrow,0) or self.info_table.item(lastrow,1) or self.info_table.item(lastrow,2) or self.info_table.item(lastrow,3) or self.info_table.item(lastrow,4) or self.info_table.item(lastrow,5) or self.info_table.item(lastrow,6):
            self.info_table.setRowCount(self.info_table.rowCount() + 1)
            for column in range(self.info_table.columnCount()):
                self.info_table.setItem(self.info_table.rowCount() - 1, column, QTableWidgetItem(''))
        else:
            reply = QMessageBox.question(self, "消息", "已存在空白行，请填写内容！", QMessageBox.Yes | QMessageBox.No)
            pass

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
                farmname=self.com_quality_data[self.com_quality_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_name'].iloc[0]
                farmcode=self.com_quality_data[self.com_quality_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_code'].iloc[0]
                wtgsid = self.info_table.item(row,0).text()
                wtgsbd = self.com_quality_data[self.com_quality_data['wtgs_id'] == self.info_table.item(row, 0).text()]['wtgs_bd'].iloc[0]
                iupdated_table_data=[farmname,farmcode,wtgsid,wtgsbd]
            for column in range(1,self.info_table.columnCount()):
                if self.info_table.item(row,column).text():
                    iupdated_table_data.append(self.info_table.item(row,column).text())
                else:
                    if column==1:
                        QMessageBox.question(self, "消息", "请填写通讯中断开始时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==2:
                        QMessageBox.question(self, "消息", "请填写通讯中断结束时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==3:
                        QMessageBox.question(self, "消息", "请填写通讯中断持续时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==4:
                        iupdated_table_data.append('')
            self.updated_table_data.append(iupdated_table_data)

    def export(self):

        if len(self.updated_table_data)>0:

            for table_data in self.updated_table_data:
                (conn, cur) = connectDB.sqlite()
                sqlstr = "REPLACE INTO com_quality (farm_name,farm_code,wtgs_id,wtgs_bd,start_time,end_time,duration,reason) VALUES "
                value = '(\''
                value+='\',\''.join(table_data)
                value += '\')'
                sqlstr += value
                try:
                    # print(sqlstr)
                    cur.execute(sqlstr)
                    conn.commit()
                    QMessageBox.question(self, "消息", "保存成功！", QMessageBox.Yes | QMessageBox.No)
                    pass
                except:
                    # print('insert error')
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

        self.com_quality_data = self.com_quality_info[self.com_quality_info['wtgs_id'].isin(self.wtgs_list)]

        label = ['机组号', '开始时间', '结束时间', '持续时间', '备注']

        self.info_table.setColumnCount(5)

        self.info_table.setRowCount(len(self.com_quality_data))

        self.info_table.setHorizontalHeaderLabels(label)

        self.info_table.verticalHeader().setVisible(False)

        self.com_quality_data.sort(columns='start_time')

        for row in range(len(self.com_quality_data)):

            self.info_table.setItem(row, 0, QTableWidgetItem(self.com_quality_data['wtgs_id'].iloc[row]))

            self.info_table.setItem(row, 1, QTableWidgetItem(self.com_quality_data['start_time'].iloc[row]))

            self.info_table.setItem(row, 2, QTableWidgetItem(str(self.com_quality_data['end_time'].iloc[row])))

            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.com_quality_data['duration'].iloc[row])))

            self.info_table.setItem(row, 4, QTableWidgetItem(str(self.com_quality_data['reason'].iloc[row])))

        self.info_table.resizeColumnsToContents()


if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=com_quality([1, 23], 10005008)
    uset_db.show()
    sys.exit(app.exec_())
