# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_qua_com.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_qua_com(object):
    def setupUi(self, Form_qua_com):
        Form_qua_com.setObjectName("Form_qua_com")
        Form_qua_com.resize(800, 600)
        self.frame = QtWidgets.QFrame(Form_qua_com)
        self.frame.setGeometry(QtCore.QRect(10, 120, 191, 261))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_end_time_qua_com = QtWidgets.QLabel(self.frame)
        self.label_end_time_qua_com.setGeometry(QtCore.QRect(10, 200, 91, 20))
        self.label_end_time_qua_com.setObjectName("label_end_time_qua_com")
        self.dateTimeEdit_startdate_qua_com = QtWidgets.QDateTimeEdit(self.frame)
        self.dateTimeEdit_startdate_qua_com.setGeometry(QtCore.QRect(10, 160, 171, 22))
        self.dateTimeEdit_startdate_qua_com.setObjectName("dateTimeEdit_startdate_qua_com")
        self.label_start_time_qua_com = QtWidgets.QLabel(self.frame)
        self.label_start_time_qua_com.setGeometry(QtCore.QRect(10, 130, 91, 20))
        self.label_start_time_qua_com.setObjectName("label_start_time_qua_com")
        self.dateTimeEdit_enddate_qua_com = QtWidgets.QDateTimeEdit(self.frame)
        self.dateTimeEdit_enddate_qua_com.setGeometry(QtCore.QRect(10, 230, 171, 22))
        self.dateTimeEdit_enddate_qua_com.setObjectName("dateTimeEdit_enddate_qua_com")
        self.label_farm_qua_com = QtWidgets.QLabel(self.frame)
        self.label_farm_qua_com.setGeometry(QtCore.QRect(10, 10, 91, 20))
        self.label_farm_qua_com.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_farm_qua_com.setObjectName("label_farm_qua_com")
        self.comboBox_wtgs_qua_com = QtWidgets.QComboBox(self.frame)
        self.comboBox_wtgs_qua_com.setGeometry(QtCore.QRect(10, 100, 171, 22))
        self.comboBox_wtgs_qua_com.setObjectName("comboBox_wtgs_qua_com")
        self.label_wtgs_qua_com = QtWidgets.QLabel(self.frame)
        self.label_wtgs_qua_com.setGeometry(QtCore.QRect(10, 70, 91, 20))
        self.label_wtgs_qua_com.setObjectName("label_wtgs_qua_com")
        self.comboBox_farm_qua_com = QtWidgets.QComboBox(self.frame)
        self.comboBox_farm_qua_com.setGeometry(QtCore.QRect(10, 40, 171, 22))
        self.comboBox_farm_qua_com.setObjectName("comboBox_farm_qua_com")
        self.queryButton_qua_com = QtWidgets.QPushButton(Form_qua_com)
        self.queryButton_qua_com.setGeometry(QtCore.QRect(60, 400, 93, 28))
        self.queryButton_qua_com.setObjectName("queryButton_qua_com")
        self.tableWidget_qua_com = QtWidgets.QTableWidget(Form_qua_com)
        self.tableWidget_qua_com.setGeometry(QtCore.QRect(220, 20, 561, 561))
        self.tableWidget_qua_com.setObjectName("tableWidget_qua_com")
        self.tableWidget_qua_com.setColumnCount(0)
        self.tableWidget_qua_com.setRowCount(0)

        self.retranslateUi(Form_qua_com)
        QtCore.QMetaObject.connectSlotsByName(Form_qua_com)

    def retranslateUi(self, Form_qua_com):
        _translate = QtCore.QCoreApplication.translate
        Form_qua_com.setWindowTitle(_translate("Form_qua_com", "通讯情况"))
        self.label_end_time_qua_com.setText(_translate("Form_qua_com", "结束时间:"))
        self.label_start_time_qua_com.setText(_translate("Form_qua_com", "开始时间:"))
        self.label_farm_qua_com.setText(_translate("Form_qua_com", "风场:"))
        self.label_wtgs_qua_com.setText(_translate("Form_qua_com", "机组:"))
        self.queryButton_qua_com.setText(_translate("Form_qua_com", "查  询"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_qua_com = QtWidgets.QWidget()
    ui = Ui_Form_qua_com()
    ui.setupUi(Form_qua_com)
    Form_qua_com.show()
    sys.exit(app.exec_())

