# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_warning_statis.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_warning_statis(object):
    def setupUi(self, Form_warning_statis):
        Form_warning_statis.setObjectName("Form_warning_statis")
        Form_warning_statis.resize(400, 300)

        self.retranslateUi(Form_warning_statis)
        QtCore.QMetaObject.connectSlotsByName(Form_warning_statis)

    def retranslateUi(self, Form_warning_statis):
        _translate = QtCore.QCoreApplication.translate
        Form_warning_statis.setWindowTitle(_translate("Form_warning_statis", "预警统计分析"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_warning_statis = QtWidgets.QWidget()
    ui = Ui_Form_warning_statis()
    ui.setupUi(Form_warning_statis)
    Form_warning_statis.show()
    sys.exit(app.exec_())

