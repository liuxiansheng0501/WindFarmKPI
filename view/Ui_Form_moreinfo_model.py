# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_moreinfo_model.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_moreinfo_model(object):
    def setupUi(self, Form_moreinfo_model):
        Form_moreinfo_model.setObjectName("Form_moreinfo_model")
        Form_moreinfo_model.resize(800, 600)
        self.tableWidget_model = QtWidgets.QTableWidget(Form_moreinfo_model)
        self.tableWidget_model.setGeometry(QtCore.QRect(40, 20, 721, 561))
        self.tableWidget_model.setObjectName("tableWidget_model")
        self.tableWidget_model.setColumnCount(0)
        self.tableWidget_model.setRowCount(0)

        self.retranslateUi(Form_moreinfo_model)
        QtCore.QMetaObject.connectSlotsByName(Form_moreinfo_model)

    def retranslateUi(self, Form_moreinfo_model):
        _translate = QtCore.QCoreApplication.translate
        Form_moreinfo_model.setWindowTitle(_translate("Form_moreinfo_model", "预警模型"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_moreinfo_model = QtWidgets.QWidget()
    ui = Ui_Form_moreinfo_model()
    ui.setupUi(Form_moreinfo_model)
    Form_moreinfo_model.show()
    sys.exit(app.exec_())

