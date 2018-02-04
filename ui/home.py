# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.by_stock_code = QtWidgets.QGroupBox(self.centralwidget)
        self.by_stock_code.setGeometry(QtCore.QRect(10, 10, 401, 91))
        self.by_stock_code.setObjectName("by_stock_code")
        self.btn_search = QtWidgets.QPushButton(self.by_stock_code)
        self.btn_search.setGeometry(QtCore.QRect(130, 20, 75, 23))
        self.btn_search.setObjectName("btn_search")
        self.input_stock_code = QtWidgets.QLineEdit(self.by_stock_code)
        self.input_stock_code.setGeometry(QtCore.QRect(10, 20, 113, 20))
        self.input_stock_code.setObjectName("input_stock_code")
        self.btn_update_k_data = QtWidgets.QPushButton(self.by_stock_code)
        self.btn_update_k_data.setGeometry(QtCore.QRect(210, 20, 101, 23))
        self.btn_update_k_data.setObjectName("btn_update_k_data")
        self.btn_update_statement = QtWidgets.QPushButton(self.by_stock_code)
        self.btn_update_statement.setGeometry(QtCore.QRect(10, 50, 131, 31))
        self.btn_update_statement.setObjectName("btn_update_statement")
        self.rdb_bs = QtWidgets.QRadioButton(self.by_stock_code)
        self.rdb_bs.setGeometry(QtCore.QRect(150, 60, 101, 16))
        self.rdb_bs.setObjectName("rdb_bs")
        self.rdb_pl = QtWidgets.QRadioButton(self.by_stock_code)
        self.rdb_pl.setGeometry(QtCore.QRect(260, 60, 89, 16))
        self.rdb_pl.setCheckable(True)
        self.rdb_pl.setChecked(False)
        self.rdb_pl.setObjectName("rdb_pl")
        self.rdb_cash = QtWidgets.QRadioButton(self.by_stock_code)
        self.rdb_cash.setGeometry(QtCore.QRect(310, 60, 89, 16))
        self.rdb_cash.setObjectName("rdb_cash")
        self.by_stock_list = QtWidgets.QGroupBox(self.centralwidget)
        self.by_stock_list.setGeometry(QtCore.QRect(10, 120, 301, 91))
        self.by_stock_list.setObjectName("by_stock_list")
        self.btn_update_sz50 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_sz50.setGeometry(QtCore.QRect(10, 20, 81, 23))
        self.btn_update_sz50.setObjectName("btn_update_sz50")
        self.btn_update_hs300 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_hs300.setGeometry(QtCore.QRect(100, 20, 91, 23))
        self.btn_update_hs300.setObjectName("btn_update_hs300")
        self.btn_update_zz500 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_zz500.setGeometry(QtCore.QRect(200, 20, 91, 23))
        self.btn_update_zz500.setObjectName("btn_update_zz500")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 380, 681, 271))
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEdit.setOverwriteMode(False)
        self.textEdit.setObjectName("textEdit")
        self.for_all_stock = QtWidgets.QGroupBox(self.centralwidget)
        self.for_all_stock.setGeometry(QtCore.QRect(10, 220, 301, 151))
        self.for_all_stock.setCheckable(False)
        self.for_all_stock.setObjectName("for_all_stock")
        self.btn_update_divi_data = QtWidgets.QPushButton(self.for_all_stock)
        self.btn_update_divi_data.setGeometry(QtCore.QRect(10, 20, 141, 23))
        self.btn_update_divi_data.setObjectName("btn_update_divi_data")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(430, 10, 248, 197))
        self.calendarWidget.setObjectName("calendarWidget")
        self.output_curr_price = QtWidgets.QLineEdit(self.centralwidget)
        self.output_curr_price.setGeometry(QtCore.QRect(430, 220, 113, 20))
        self.output_curr_price.setObjectName("output_curr_price")
        self.btn_search_k_data = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search_k_data.setGeometry(QtCore.QRect(580, 220, 75, 23))
        self.btn_search_k_data.setObjectName("btn_search_k_data")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.by_stock_code.setTitle(_translate("MainWindow", "By Stock Code"))
        self.btn_search.setText(_translate("MainWindow", "Search"))
        self.btn_update_k_data.setText(_translate("MainWindow", "Update K data"))
        self.btn_update_statement.setText(_translate("MainWindow", "Update Statement"))
        self.rdb_bs.setText(_translate("MainWindow", "Balance Sheet"))
        self.rdb_pl.setWhatsThis(_translate("MainWindow", "P&L Statement"))
        self.rdb_pl.setText(_translate("MainWindow", "P&&L"))
        self.rdb_cash.setText(_translate("MainWindow", "Cash Flow"))
        self.by_stock_list.setTitle(_translate("MainWindow", "By Stock List"))
        self.btn_update_sz50.setText(_translate("MainWindow", "Update sz50"))
        self.btn_update_hs300.setText(_translate("MainWindow", "Update hs300"))
        self.btn_update_zz500.setText(_translate("MainWindow", "Update zz500"))
        self.for_all_stock.setTitle(_translate("MainWindow", "For All Stock"))
        self.btn_update_divi_data.setText(_translate("MainWindow", "Upate Dividend data"))
        self.btn_search_k_data.setText(_translate("MainWindow", "Search"))

