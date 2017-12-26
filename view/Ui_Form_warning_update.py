# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_warning_update.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_warning_update(object):
    def setupUi(self, Form_warning_update):
        Form_warning_update.setObjectName("Form_warning_update")
        Form_warning_update.resize(800, 600)
        self.frame = QtWidgets.QFrame(Form_warning_update)
        self.frame.setGeometry(QtCore.QRect(10, 110, 171, 371))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_end_time_warning_update = QtWidgets.QLabel(self.frame)
        self.label_end_time_warning_update.setGeometry(QtCore.QRect(10, 260, 91, 20))
        self.label_end_time_warning_update.setObjectName("label_end_time_warning_update")
        self.dateTimeEdit_startdate_warning_update = QtWidgets.QDateTimeEdit(self.frame)
        self.dateTimeEdit_startdate_warning_update.setGeometry(QtCore.QRect(10, 220, 151, 22))
        self.dateTimeEdit_startdate_warning_update.setObjectName("dateTimeEdit_startdate_warning_update")
        self.label_start_time_warning_update = QtWidgets.QLabel(self.frame)
        self.label_start_time_warning_update.setGeometry(QtCore.QRect(10, 190, 91, 20))
        self.label_start_time_warning_update.setObjectName("label_start_time_warning_update")
        self.dateTimeEdit_enddate_warning_update = QtWidgets.QDateTimeEdit(self.frame)
        self.dateTimeEdit_enddate_warning_update.setGeometry(QtCore.QRect(10, 290, 151, 22))
        self.dateTimeEdit_enddate_warning_update.setObjectName("dateTimeEdit_enddate_warning_update")
        self.label_farm_warning_update = QtWidgets.QLabel(self.frame)
        self.label_farm_warning_update.setGeometry(QtCore.QRect(10, 10, 91, 20))
        self.label_farm_warning_update.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_farm_warning_update.setObjectName("label_farm_warning_update")
        self.comboBox_wtgs_warning_update = QtWidgets.QComboBox(self.frame)
        self.comboBox_wtgs_warning_update.setGeometry(QtCore.QRect(10, 100, 151, 22))
        self.comboBox_wtgs_warning_update.setObjectName("comboBox_wtgs_warning_update")
        self.label_wtgs_warning_update = QtWidgets.QLabel(self.frame)
        self.label_wtgs_warning_update.setGeometry(QtCore.QRect(10, 70, 91, 20))
        self.label_wtgs_warning_update.setObjectName("label_wtgs_warning_update")
        self.comboBox_farm_warning_update = QtWidgets.QComboBox(self.frame)
        self.comboBox_farm_warning_update.setGeometry(QtCore.QRect(10, 40, 151, 22))
        self.comboBox_farm_warning_update.setObjectName("comboBox_farm_warning_update")
        self.label_model_warning_update = QtWidgets.QLabel(self.frame)
        self.label_model_warning_update.setGeometry(QtCore.QRect(10, 130, 91, 20))
        self.label_model_warning_update.setObjectName("label_model_warning_update")
        self.comboBox_model_warning_update = QtWidgets.QComboBox(self.frame)
        self.comboBox_model_warning_update.setGeometry(QtCore.QRect(10, 160, 151, 22))
        self.comboBox_model_warning_update.setObjectName("comboBox_model_warning_update")
        self.update_Button_warning_update = QtWidgets.QPushButton(self.frame)
        self.update_Button_warning_update.setGeometry(QtCore.QRect(100, 330, 61, 28))
        self.update_Button_warning_update.setObjectName("update_Button_warning_update")
        self.stop_Button_warning_update_2 = QtWidgets.QPushButton(self.frame)
        self.stop_Button_warning_update_2.setGeometry(QtCore.QRect(10, 330, 61, 28))
        self.stop_Button_warning_update_2.setObjectName("stop_Button_warning_update_2")
        self.listWidget = QtWidgets.QListWidget(Form_warning_update)
        self.listWidget.setGeometry(QtCore.QRect(200, 30, 581, 541))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Form_warning_update)
        QtCore.QMetaObject.connectSlotsByName(Form_warning_update)

    def retranslateUi(self, Form_warning_update):
        _translate = QtCore.QCoreApplication.translate
        Form_warning_update.setWindowTitle(_translate("Form_warning_update", "预警更新"))
        self.label_end_time_warning_update.setText(_translate("Form_warning_update", "结束时间:"))
        self.label_start_time_warning_update.setText(_translate("Form_warning_update", "开始时间:"))
        self.label_farm_warning_update.setText(_translate("Form_warning_update", "风场:"))
        self.label_wtgs_warning_update.setText(_translate("Form_warning_update", "机组:"))
        self.label_model_warning_update.setText(_translate("Form_warning_update", "模型:"))
        self.update_Button_warning_update.setText(_translate("Form_warning_update", "更  新"))
        self.stop_Button_warning_update_2.setText(_translate("Form_warning_update", "中  止"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_warning_update = QtWidgets.QWidget()
    ui = Ui_Form_warning_update()
    ui.setupUi(Form_warning_update)
    Form_warning_update.show()
    sys.exit(app.exec_())

