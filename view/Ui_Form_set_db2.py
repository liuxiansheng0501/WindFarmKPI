# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_set_db2.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_set_db2(object):
    def setupUi(self, Form_set_db2):
        Form_set_db2.setObjectName("Form_set_db2")
        Form_set_db2.resize(800, 600)
        self.label_wtgs_set_db2 = QtWidgets.QLabel(Form_set_db2)
        self.label_wtgs_set_db2.setGeometry(QtCore.QRect(290, 30, 51, 20))
        self.label_wtgs_set_db2.setObjectName("label_wtgs_set_db2")
        self.comboBox_wtgs_set_db2 = QtWidgets.QComboBox(Form_set_db2)
        self.comboBox_wtgs_set_db2.setGeometry(QtCore.QRect(350, 30, 151, 22))
        self.comboBox_wtgs_set_db2.setObjectName("comboBox_wtgs_set_db2")
        self.comboBox_farm_set_db2 = QtWidgets.QComboBox(Form_set_db2)
        self.comboBox_farm_set_db2.setGeometry(QtCore.QRect(100, 30, 151, 22))
        self.comboBox_farm_set_db2.setObjectName("comboBox_farm_set_db2")
        self.edit_Button_set_db2 = QtWidgets.QPushButton(Form_set_db2)
        self.edit_Button_set_db2.setGeometry(QtCore.QRect(560, 17, 93, 41))
        self.edit_Button_set_db2.setObjectName("edit_Button_set_db2")
        self.label_farm_set_db2 = QtWidgets.QLabel(Form_set_db2)
        self.label_farm_set_db2.setGeometry(QtCore.QRect(40, 30, 51, 20))
        self.label_farm_set_db2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_farm_set_db2.setObjectName("label_farm_set_db2")
        self.query_Button_set_db_2 = QtWidgets.QPushButton(Form_set_db2)
        self.query_Button_set_db_2.setGeometry(QtCore.QRect(670, 17, 93, 41))
        self.query_Button_set_db_2.setObjectName("query_Button_set_db_2")
        self.tableWidget_set_db2 = QtWidgets.QTableWidget(Form_set_db2)
        self.tableWidget_set_db2.setGeometry(QtCore.QRect(20, 70, 761, 511))
        self.tableWidget_set_db2.setObjectName("tableWidget_set_db2")
        self.tableWidget_set_db2.setColumnCount(0)
        self.tableWidget_set_db2.setRowCount(0)

        self.retranslateUi(Form_set_db2)
        QtCore.QMetaObject.connectSlotsByName(Form_set_db2)

    def retranslateUi(self, Form_set_db2):
        _translate = QtCore.QCoreApplication.translate
        Form_set_db2.setWindowTitle(_translate("Form_set_db2", "数据库(sqlserver)"))
        self.label_wtgs_set_db2.setText(_translate("Form_set_db2", "机组:"))
        self.edit_Button_set_db2.setText(_translate("Form_set_db2", "保  存"))
        self.label_farm_set_db2.setText(_translate("Form_set_db2", "风场:"))
        self.query_Button_set_db_2.setText(_translate("Form_set_db2", "查  询"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_set_db2 = QtWidgets.QWidget()
    ui = Ui_Form_set_db2()
    ui.setupUi(Form_set_db2)
    Form_set_db2.show()
    sys.exit(app.exec_())

