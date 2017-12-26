# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_progress_bar_ib=QtWidgets.QLabel(self.centralwidget)
        self.label_progress_bar_ib.setGeometry(QtCore.QRect(20, 600, 45, 20))
        self.label_progress_bar_ib.setObjectName("label_progress_bar_ib")

        self.progress_bar_ib = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar_ib.setGeometry(QtCore.QRect(70, 600, 150, 20))
        self.progress_bar_ib.setObjectName("progress_bar_ib")

        self.label_progress_bar_bd = QtWidgets.QLabel(self.centralwidget)
        self.label_progress_bar_bd.setGeometry(QtCore.QRect(20, 640, 45, 20))
        self.label_progress_bar_bd.setObjectName("label_progress_bar_bd")

        self.progress_bar_bd = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar_bd.setGeometry(QtCore.QRect(70, 640, 150, 20))
        self.progress_bar_bd.setObjectName("progress_bar_bd")

        self.label_progress_bar_golden = QtWidgets.QLabel(self.centralwidget)
        self.label_progress_bar_golden.setGeometry(QtCore.QRect(20, 680, 45, 20))
        self.label_progress_bar_golden.setObjectName("label_progress_bar_golden")

        self.progress_bar_golden = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar_golden.setGeometry(QtCore.QRect(70, 680, 150, 20))
        self.progress_bar_golden.setObjectName("progress_bar_golden")

        self.pushButton_cal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cal.setGeometry(QtCore.QRect(20, 500, 200, 30))
        self.pushButton_cal.setObjectName("pushButton_cal")

        self.pushButton_query = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_query.setGeometry(QtCore.QRect(20, 550, 200, 30))
        self.pushButton_query.setObjectName("pushButton_query")

        self.label_farm = QtWidgets.QLabel(self.centralwidget)
        self.label_farm.setGeometry(QtCore.QRect(20, 230, 91, 20))
        self.label_farm.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_farm.setObjectName("label_farm")

        self.comboBox_farm = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_farm.setGeometry(QtCore.QRect(20, 260, 200, 22))
        self.comboBox_farm.setObjectName("comboBox_farm")

        self.label_wtgs = QtWidgets.QLabel(self.centralwidget)
        self.label_wtgs.setGeometry(QtCore.QRect(22, 290, 91, 22))
        self.label_wtgs.setObjectName("label_wtgs")

        self.comboBox_wtgs = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_wtgs.setGeometry(QtCore.QRect(20, 320, 200, 22))
        self.comboBox_wtgs.setObjectName("comboBox_wtgs")

        self.label_start_time = QtWidgets.QLabel(self.centralwidget)
        self.label_start_time.setGeometry(QtCore.QRect(20, 350, 91, 22))
        self.label_start_time.setObjectName("label_start_time")

        self.label_end_time = QtWidgets.QLabel(self.centralwidget)
        self.label_end_time.setGeometry(QtCore.QRect(20, 420, 91, 22))
        self.label_end_time.setObjectName("label_end_time")

        self.dateTimeEdit_startdate = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_startdate.setGeometry(QtCore.QRect(20, 380, 200, 22))
        self.dateTimeEdit_startdate.setObjectName("dateTimeEdit_startdate")

        self.dateTimeEdit_enddate = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_enddate.setGeometry(QtCore.QRect(20, 450, 200, 22))
        self.dateTimeEdit_enddate.setObjectName("dateTimeEdit_enddate")

        self.main_table = QtWidgets.QTableWidget(self.centralwidget)
        self.main_table.setGeometry(QtCore.QRect(240, 20, 940, 400))
        self.main_table.setObjectName("main_table")
        self.main_table.horizontalHeader().setSectionResizeMode(1)#1代表列，0代表行
        self.main_table.verticalHeader().resizeContentsPrecision()
        self.main_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.main_table.setSelectionBehavior(1)
        #
        # self.sub_table = QtWidgets.QTableWidget(self.centralwidget)
        # self.sub_table.setGeometry(QtCore.QRect(700, 20, 480, 300))
        # self.sub_table.setObjectName("sub_table")
        # self.sub_table.horizontalHeader().setSectionResizeMode(1)  # 1代表列，0代表行
        # self.sub_table.verticalHeader().resizeContentsPrecision()
        # self.sub_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.sub_table.setSelectionBehavior(1)
        # self.sub_table = QtWidgets.QTableWidget(self.centralwidget)
        # self.sub_table.setGeometry(QtCore.QRect(700, 20, 480, 300))
        # self.sub_table.setObjectName("sub_table")
        # self.sub_table.horizontalHeader().setSectionResizeMode(1)  # 1代表列，0代表行
        # self.sub_table.verticalHeader().resizeContentsPrecision()
        # self.sub_table.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.sub_table.setSelectionBehavior(1)

        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(1100, 670, 80, 30))
        self.btn_save.setObjectName("btn_save")

        self.log_window = QtWidgets.QTextBrowser(self.centralwidget)
        # self.log_window.setMaximumSize(1000000)
        self.log_window.setGeometry(QtCore.QRect(240, 430, 940, 230))
        self.log_window.setObjectName("log_window")

        self.check_power = QtWidgets.QCheckBox(self.centralwidget)
        self.check_power.setGeometry(QtCore.QRect(20, 30, 93, 28))
        self.check_power.setObjectName("power")

        self.check_power_ib = QtWidgets.QCheckBox(self.centralwidget)
        self.check_power_ib.setGeometry(QtCore.QRect(50, 60, 93, 28))
        self.check_power_ib.setObjectName("power_ib")

        self.check_power_bd = QtWidgets.QCheckBox(self.centralwidget)
        self.check_power_bd.setGeometry(QtCore.QRect(100, 60, 93, 28))
        self.check_power_bd.setObjectName("power_bd")

        self.check_power_golden = QtWidgets.QCheckBox(self.centralwidget)
        self.check_power_golden.setGeometry(QtCore.QRect(170, 60, 93, 28))
        self.check_power_golden.setObjectName("power_golden")

        self.check_fault_info = QtWidgets.QCheckBox(self.centralwidget)
        self.check_fault_info.setGeometry(QtCore.QRect(20, 90, 93, 28))
        self.check_fault_info.setObjectName("check_fault_times")

        self.check_utilize = QtWidgets.QCheckBox(self.centralwidget)
        self.check_utilize.setGeometry(QtCore.QRect(20, 120, 93, 28))
        self.check_utilize.setObjectName("check_utilize")

        self.check_quality = QtWidgets.QCheckBox(self.centralwidget)
        self.check_quality.setGeometry(QtCore.QRect(20, 150, 93, 28))
        self.check_quality.setObjectName("check_quality")

        self.check_avg_speed = QtWidgets.QCheckBox(self.centralwidget)
        self.check_avg_speed.setGeometry(QtCore.QRect(20, 180, 93, 28))
        self.check_avg_speed.setObjectName("check_avg_speed")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1159, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.set = QtWidgets.QMenu(self.menubar)
        self.set.setObjectName("set")

        self.weekreport = QtWidgets.QMenu(self.menubar)
        self.weekreport.setObjectName("weekreport")

        self.stas = QtWidgets.QMenu(self.menubar)
        self.stas.setObjectName("stas")

        self.tag_series = QtWidgets.QMenu(self.menubar)
        self.tag_series.setObjectName("tag_series")

        self.help = QtWidgets.QMenu(self.menubar)
        self.help.setObjectName("help")

        self.more_info = QtWidgets.QMenu(self.menubar)
        self.more_info.setObjectName("more_info")
        
        self.set_ib = QtWidgets.QAction(MainWindow)
        self.set_ib.setObjectName("set_ib")

        self.set_model = QtWidgets.QAction(MainWindow)
        self.set_model.setObjectName("set_model")

        self.generate = QtWidgets.QAction(MainWindow)
        self.generate.setObjectName("generate")

        self.wtgs_type = QtWidgets.QAction(MainWindow)
        self.wtgs_type.setObjectName("warning_update")

        self.moreinfo_model = QtWidgets.QAction(MainWindow)
        self.moreinfo_model.setObjectName("moreinfo_model")

        self.help_manual = QtWidgets.QAction(MainWindow)
        self.help_manual.setObjectName("help_manual")

        self.help_maintain = QtWidgets.QAction(MainWindow)
        self.help_maintain.setObjectName("help_maintain")

        self.set_exit = QtWidgets.QAction(MainWindow)
        self.set_exit.setStatusTip("")
        self.set_exit.setObjectName("set_exit")

        self.warning_query = QtWidgets.QAction(MainWindow)
        self.warning_query.setObjectName("warning_query")

        self.set_action_list = QtWidgets.QAction(MainWindow)
        self.set_action_list.setObjectName("set_action_list")

        self.set.addAction(self.set_ib)
        self.set.addSeparator()
        self.set.addAction(self.set_action_list)
        self.set.addSeparator()
        self.set.addAction(self.set_exit)

        self.weekreport.addAction(self.generate)

        self.stas.addAction(self.wtgs_type)
        self.stas.addSeparator()

        self.help.addAction(self.help_manual)
        self.help.addSeparator()
        self.help.addAction(self.help_maintain)

        self.more_info.addAction(self.moreinfo_model)

        self.menubar.addAction(self.set.menuAction())
        self.menubar.addAction(self.weekreport.menuAction())
        self.menubar.addAction(self.stas.menuAction())
        self.menubar.addAction(self.tag_series.menuAction())
        self.menubar.addAction(self.more_info.menuAction())
        self.menubar.addAction(self.help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "明阳智能风场KPI统计系统"))
        self.pushButton_cal.setText(_translate("MainWindow", "计   算"))
        self.btn_save.setText(_translate("MainWindow", "保   存"))
        self.label_progress_bar_ib.setText(_translate("MainWindow", "ib:"))
        self.label_progress_bar_bd.setText(_translate("MainWindow", "集控:"))
        self.label_progress_bar_golden.setText(_translate("MainWindow", "庚顿:"))
        self.check_avg_speed.setText(_translate("MainWindow", "风速"))
        self.pushButton_query.setText(_translate("MainWindow", "查   询"))
        self.label_farm.setText(_translate("MainWindow", "风场:"))
        self.label_wtgs.setText(_translate("MainWindow", "机组:"))
        self.label_start_time.setText(_translate("MainWindow", "开始时间:"))
        self.label_end_time.setText(_translate("MainWindow", "结束时间:"))
        self.check_power.setText(_translate("MainWindow", "发电量"))
        self.check_power_ib.setText(_translate("MainWindow", "ib"))
        self.check_power_bd.setText(_translate("MainWindow", "集控"))
        self.check_power_golden.setText(_translate("MainWindow", "庚顿"))
        self.check_fault_info.setText(_translate("MainWindow", "故障信息"))
        self.check_utilize.setText(_translate("MainWindow", "可利用率"))
        self.check_quality.setText(_translate("MainWindow", "通讯情况"))
        self.set.setTitle(_translate("MainWindow", "设置"))
        self.weekreport.setTitle(_translate("MainWindow", "报表"))
        self.stas.setTitle(_translate("MainWindow", "统计"))
        self.help.setTitle(_translate("MainWindow", "帮助"))
        self.more_info.setTitle(_translate("MainWindow", "备注"))
        self.tag_series.setTitle(_translate("MainWindow", "时间序列"))
        self.set_ib.setText(_translate("MainWindow", "数据库(IB)"))
        self.set_model.setText(_translate("MainWindow", "模型"))
        self.generate.setText(_translate("MainWindow", "生成"))
        self.wtgs_type.setText(_translate("MainWindow", "机型"))
        self.moreinfo_model.setText(_translate("MainWindow", "记录"))
        self.help_manual.setText(_translate("MainWindow", "教程"))
        self.help_maintain.setText(_translate("MainWindow", "维护"))
        self.set_exit.setText(_translate("MainWindow", "退出"))
        self.warning_query.setText(_translate("MainWindow", "查询"))
        self.set_action_list.setText(_translate("MainWindow", "数据库(Actionlist)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

