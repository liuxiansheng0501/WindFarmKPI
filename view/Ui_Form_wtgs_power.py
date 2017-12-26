# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as  FigureCanvas

class Ui_wtgs_power(object):

    def setupUi(self, wtgs_power):

        wtgs_power.setObjectName("wtgs_power")
        wtgs_power.resize(800, 600)
        self.VLayoutWidget = QtWidgets.QWidget(wtgs_power)
        self.VLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.VLayoutWidget.setObjectName("VLayoutWidget")
        self.VLayout = QtWidgets.QVBoxLayout(self.VLayoutWidget)

        # tag select and button region
        self.Hlayout = QtWidgets.QHBoxLayout()
        self.label_wtgs = QtWidgets.QLabel('机组:')
        self.label_wtgs.setAlignment(QtCore.Qt.AlignCenter)
        self.combobox_wtgs = QtWidgets.QComboBox()
        self.combobox_wtgs.setMinimumWidth(20)
        self.plt_btn = QtWidgets.QPushButton('plot')
        self.plt_btn.setObjectName("plt_btn")
        self.save_btn = QtWidgets.QPushButton('save')
        self.save_btn.setObjectName("save")

        self.Hlayout.addWidget(self.label_wtgs, 2)
        self.Hlayout.addWidget(self.combobox_wtgs, 3)
        self.Hlayout.addWidget(self.plt_btn, 2)
        self.Hlayout.addWidget(self.save_btn, 2)

        # figure region
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvas(self.figure)

        self.VLayout.addLayout(self.Hlayout)
        self.VLayout.addWidget(self.canvas)

        self.retranslateUi(wtgs_power)
        QtCore.QMetaObject.connectSlotsByName(wtgs_power)

    def retranslateUi(self, wtgs_power):
        _translate = QtCore.QCoreApplication.translate
        wtgs_power.setWindowTitle(_translate("wtgs_power", "机组发电量"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wtgs_power = QtWidgets.QDialog()
    ui = Ui_wtgs_power()
    ui.setupUi(wtgs_power)
    wtgs_power.show()
    sys.exit(app.exec_())

