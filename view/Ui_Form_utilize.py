# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class Ui_utilize_info(object):

    def setupUi(self, utilize_info):

        utilize_info.setObjectName("utilize_info")
        utilize_info.resize(800, 600)
        self.VLayoutWidget = QtWidgets.QWidget(utilize_info)
        self.VLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.VLayoutWidget.setObjectName("VLayoutWidget")
        self.VLayout = QtWidgets.QVBoxLayout(self.VLayoutWidget)

        # tag select and button region
        self.Hlayout = QtWidgets.QHBoxLayout()
        self.label_wtgs = QtWidgets.QLabel('机组:')
        self.label_wtgs.setAlignment(QtCore.Qt.AlignCenter)
        self.combobox_wtgs = QtWidgets.QComboBox()
        self.combobox_wtgs.setMinimumWidth(20)
        self.query = QtWidgets.QPushButton('query')
        self.query.setObjectName("query")
        self.add = QtWidgets.QPushButton('add')
        self.add.setObjectName("add")
        self.save_btn = QtWidgets.QPushButton('save')
        self.save_btn.setObjectName("save")

        self.Hlayout.addWidget(self.label_wtgs, 2)
        self.Hlayout.addWidget(self.combobox_wtgs, 3)
        self.Hlayout.addWidget(self.query, 2)
        self.Hlayout.addWidget(self.add, 2)
        self.Hlayout.addWidget(self.save_btn, 2)

        # table
        self.info_table = QtWidgets.QTableWidget()
        self.info_table.setGeometry(QtCore.QRect(0, 0, 560, 630))
        self.info_table.setObjectName("info_table")
        # self.info_table.horizontalHeader().setSectionResizeMode(1)  # 1代表列，0代表行
        # self.info_table.verticalHeader().resizeContentsPrecision()
        # self.info_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.info_table.setSelectionBehavior(1)

        self.VLayout.addLayout(self.Hlayout)
        self.VLayout.addWidget(self.info_table)

        self.retranslateUi(utilize_info)
        QtCore.QMetaObject.connectSlotsByName(utilize_info)

    def retranslateUi(self, utilize_info):

        _translate = QtCore.QCoreApplication.translate
        utilize_info.setWindowTitle(_translate("utilize_info", "机组可利用率信息"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    utilize_info = QtWidgets.QDialog()
    ui = Ui_utilize_info()
    ui.setupUi(utilize_info)
    utilize_info.show()
    sys.exit(app.exec_())

