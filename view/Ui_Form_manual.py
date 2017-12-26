# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\software\python\project\early_warning\view\Form_manual.ui'
#
# Created by: PyQt5 view code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_manual(object):
    def setupUi(self, Form_manual):
        Form_manual.setObjectName("Form_manual")
        Form_manual.resize(400, 558)

        self.retranslateUi(Form_manual)
        QtCore.QMetaObject.connectSlotsByName(Form_manual)

    def retranslateUi(self, Form_manual):
        _translate = QtCore.QCoreApplication.translate
        Form_manual.setWindowTitle(_translate("Form_manual", "使用手册"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_manual = QtWidgets.QWidget()
    ui = Ui_Form_manual()
    ui.setupUi(Form_manual)
    Form_manual.show()
    sys.exit(app.exec_())

