# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import config
import connectDB
from view.Ui_Form_utilize import Ui_utilize_info


class wtgs_utilize(QWidget, Ui_utilize_info):

    def __init__(self, utilize_info, wtgs_id, parent=None):

        super(wtgs_utilize, self).__init__(parent)

        self.argv_cfg=config.argv_cfg()

        self.wtgs_id=wtgs_id

        self.utilize_info=utilize_info

        self.setupUi(self)

        self.__initial_combobox__()

        self.__initial_wtgs_utilize__()

    def  __initial_combobox__(self):

        cmp_wtgs_group=list(set(self.utilize_info[self.utilize_info['farm_code'] == self.wtgs_id[0:5]]['wtgs_id'].tolist()))

        self.plistwidget_wtgs=QtWidgets.QListWidget()

        self.check_box_wtgs=QtWidgets.QCheckBox('全选')

        self.check_box_wtgs.stateChanged.connect(self.on_check_box_wtgs_stateChanged)

        self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), self.check_box_wtgs)

        for wtgs_name in cmp_wtgs_group:

            self.plistwidget_wtgs.setItemWidget(QtWidgets.QListWidgetItem(self.plistwidget_wtgs), QtWidgets.QCheckBox(wtgs_name))

        self.plistwidget_wtgs.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.combobox_wtgs.setModel(self.plistwidget_wtgs.model())

        self.combobox_wtgs.setView(self.plistwidget_wtgs)

    def  __initial_wtgs_utilize__(self):

        self.info_table.clear()

        self.wtgs_utilize_data = self.utilize_info[self.utilize_info['wtgs_id'] == self.wtgs_id]

        label = ['机组号', '日期', '故障(维护)时间', '无故障维护时间', '无故障停机时间', '可利用时间', '可利用率','备注']

        self.info_table.setColumnCount(8)

        self.info_table.setRowCount(len(self.wtgs_utilize_data))

        self.info_table.setHorizontalHeaderLabels(label)

        self.info_table.verticalHeader().setVisible(False)

        self.wtgs_utilize_data.index=self.wtgs_utilize_data['time'].tolist()

        self.wtgs_utilize_data.sort_index()

        for row in range(len(self.wtgs_utilize_data)):

            self.info_table.setItem(row, 0, QTableWidgetItem(self.wtgs_utilize_data['wtgs_id'].iloc[row]))

            self.info_table.setItem(row, 1, QTableWidgetItem(self.wtgs_utilize_data['time'].iloc[row]))

            self.info_table.setItem(row, 2, QTableWidgetItem(str(self.wtgs_utilize_data['fault_maintain_time'].iloc[row])))

            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.wtgs_utilize_data['maintain_time_normal'].iloc[row])))

            self.info_table.setItem(row, 4, QTableWidgetItem(str(self.wtgs_utilize_data['stop_time_normal'].iloc[row])))

            self.info_table.setItem(row, 5, QTableWidgetItem(str(self.wtgs_utilize_data['utilize_time'].iloc[row])))

            self.info_table.setItem(row, 6, QTableWidgetItem(str(self.wtgs_utilize_data['utilize'].iloc[row])))

            self.info_table.setItem(row, 7, QTableWidgetItem(self.wtgs_utilize_data['info'].iloc[row]))

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
                farmname=self.wtgs_utilize_data[self.wtgs_utilize_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_name'].iloc[0]
                farmcode=self.wtgs_utilize_data[self.wtgs_utilize_data['wtgs_id']==self.info_table.item(row,0).text()]['farm_code'].iloc[0]
                wtgsid = self.info_table.item(row,0).text()
                wtgsbd = self.wtgs_utilize_data[self.wtgs_utilize_data['wtgs_id'] == self.info_table.item(row, 0).text()]['wtgs_bd'].iloc[0]
                iupdated_table_data=[farmname,farmcode,wtgsid,wtgsbd]
            for column in range(1,self.info_table.columnCount()):
                if self.info_table.item(row,column).text():
                    iupdated_table_data.append(self.info_table.item(row,column).text())
                else:
                    if column==1:
                        QMessageBox.question(self, "消息", "请填写时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==2:
                        QMessageBox.question(self, "消息", "请填写故障(维护)时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==3:
                        QMessageBox.question(self, "消息", "请填写无故障维护时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==4:
                        QMessageBox.question(self, "消息", "请填写无故障停机时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==5:
                        QMessageBox.question(self, "消息", "请填写可利用时间！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==6:
                        QMessageBox.question(self, "消息", "请填写可利用率！", QMessageBox.Yes | QMessageBox.No)
                        pass
                    elif column==7:
                        iupdated_table_data.append('')
            self.updated_table_data.append(iupdated_table_data)

    def export(self):

        if len(self.updated_table_data)>0:

            for table_data in self.updated_table_data:
                (conn, cur) = connectDB.sqlite()
                sqlstr = "REPLACE INTO utilize (farm_name,farm_code,wtgs_id,wtgs_bd,time,fault_maintain_time,maintain_time_normal,stop_time_normal,utilize_time,utilize,info) VALUES "
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

        self.wtgs_utilize_data = self.utilize_info[self.utilize_info['wtgs_id'].isin(self.wtgs_list)]

        label = ['机组号', '日期', '故障(维护)时间', '无故障维护时间', '无故障停机时间', '可利用时间', '可利用率', '备注']

        self.info_table.setColumnCount(7)

        self.info_table.setRowCount(len(self.wtgs_utilize_data))

        self.info_table.setHorizontalHeaderLabels(label)

        self.info_table.verticalHeader().setVisible(False)

        self.wtgs_utilize_data.index=self.wtgs_utilize_data['time'].tolist()

        self.wtgs_utilize_data.sort_index()

        for row in range(len(self.wtgs_utilize_data)):

            self.info_table.setItem(row, 0, QTableWidgetItem(self.wtgs_utilize_data['wtgs_id'].iloc[row]))

            self.info_table.setItem(row, 1, QTableWidgetItem(self.wtgs_utilize_data['time'].iloc[row]))

            self.info_table.setItem(row, 2, QTableWidgetItem(str(self.wtgs_utilize_data['fault_maintain_time'].iloc[row])))

            self.info_table.setItem(row, 3, QTableWidgetItem(str(self.wtgs_utilize_data['maintain_time_normal'].iloc[row])))

            self.info_table.setItem(row, 4, QTableWidgetItem(str(self.wtgs_utilize_data['stop_time_normal'].iloc[row])))

            self.info_table.setItem(row, 5, QTableWidgetItem(str(self.wtgs_utilize_data['utilize_time'].iloc[row])))

            self.info_table.setItem(row, 6, QTableWidgetItem(str(self.wtgs_utilize_data['utilize'].iloc[row])))

            self.info_table.setItem(row, 7, QTableWidgetItem(self.wtgs_utilize_data['info'].iloc[row]))

        self.info_table.resizeColumnsToContents()


if __name__=="__main__":
    app=QApplication(sys.argv)
    uset_db=wtgs_utilize([1, 23], 10005008)
    uset_db.show()
    sys.exit(app.exec_())
