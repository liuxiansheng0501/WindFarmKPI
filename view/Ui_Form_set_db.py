# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_set_db.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_set_db(object):
    def setupUi(self, Form_set_db):
        Form_set_db.setObjectName("Form_set_db")
        Form_set_db.resize(800, 600)
        self.label_farm_set_db = QtWidgets.QLabel(Form_set_db)
        self.label_farm_set_db.setGeometry(QtCore.QRect(40, 30, 51, 20))
        self.label_farm_set_db.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_farm_set_db.setObjectName("label_farm_set_db")
        self.label_wtgs_set_db = QtWidgets.QLabel(Form_set_db)
        self.label_wtgs_set_db.setGeometry(QtCore.QRect(290, 30, 51, 20))
        self.label_wtgs_set_db.setObjectName("label_wtgs_set_db")
        self.comboBox_wtgs_set_db = QtWidgets.QComboBox(Form_set_db)
        self.comboBox_wtgs_set_db.setGeometry(QtCore.QRect(350, 30, 151, 22))
        self.comboBox_wtgs_set_db.setObjectName("comboBox_wtgs_set_db")
        self.comboBox_farm_set_db = QtWidgets.QComboBox(Form_set_db)
        self.comboBox_farm_set_db.setGeometry(QtCore.QRect(100, 30, 151, 22))
        self.comboBox_farm_set_db.setObjectName("comboBox_farm_set_db")
        self.edit_Button_set_db = QtWidgets.QPushButton(Form_set_db)
        self.edit_Button_set_db.setGeometry(QtCore.QRect(560, 17, 93, 41))
        self.edit_Button_set_db.setObjectName("edit_Button_set_db")
        self.tableWidget_set_db = QtWidgets.QTableWidget(Form_set_db)
        self.tableWidget_set_db.setGeometry(QtCore.QRect(20, 70, 761, 511))
        self.tableWidget_set_db.setObjectName("tableWidget_set_db")
        self.tableWidget_set_db.setColumnCount(0)
        self.tableWidget_set_db.setRowCount(0)
        self.query_Button_set_db = QtWidgets.QPushButton(Form_set_db)
        self.query_Button_set_db.setGeometry(QtCore.QRect(670, 17, 93, 41))
        self.query_Button_set_db.setObjectName("query_Button_set_db")

        self.retranslateUi(Form_set_db)
        QtCore.QMetaObject.connectSlotsByName(Form_set_db)

    def retranslateUi(self, Form_set_db):
        _translate = QtCore.QCoreApplication.translate
        Form_set_db.setWindowTitle(_translate("Form_set_db", "数据库(IB)"))
        self.label_farm_set_db.setText(_translate("Form_set_db", "风场:"))
        self.label_wtgs_set_db.setText(_translate("Form_set_db", "机组:"))
        self.edit_Button_set_db.setText(_translate("Form_set_db", "保  存"))
        self.query_Button_set_db.setText(_translate("Form_set_db", "查  询"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_set_db = QtWidgets.QWidget()
    ui = Ui_Form_set_db()
    ui.setupUi(Form_set_db)
    Form_set_db.show()
    sys.exit(app.exec_())

