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
        self.by_stock_code.setGeometry(QtCore.QRect(10, 10, 681, 91))
        self.by_stock_code.setObjectName("by_stock_code")
        self.btn_search = QtWidgets.QPushButton(self.by_stock_code)
        self.btn_search.setGeometry(QtCore.QRect(130, 20, 75, 23))
        self.btn_search.setObjectName("btn_search")
        self.input_stock_code = QtWidgets.QLineEdit(self.by_stock_code)
        self.input_stock_code.setGeometry(QtCore.QRect(10, 20, 113, 20))
        self.input_stock_code.setObjectName("input_stock_code")
        self.btn_update = QtWidgets.QPushButton(self.by_stock_code)
        self.btn_update.setGeometry(QtCore.QRect(210, 20, 75, 23))
        self.btn_update.setObjectName("btn_update")
        self.by_stock_list = QtWidgets.QGroupBox(self.centralwidget)
        self.by_stock_list.setGeometry(QtCore.QRect(10, 110, 681, 91))
        self.by_stock_list.setObjectName("by_stock_list")
        self.btn_update_sz50 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_sz50.setGeometry(QtCore.QRect(10, 20, 81, 23))
        self.btn_update_sz50.setObjectName("btn_update_sz50")
        self.btn_update_hs300 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_hs300.setGeometry(QtCore.QRect(100, 20, 91, 23))
        self.btn_update_hs300.setObjectName("btn_update_hs300")
        self.btn_update_hs300_2 = QtWidgets.QPushButton(self.by_stock_list)
        self.btn_update_hs300_2.setGeometry(QtCore.QRect(200, 20, 91, 23))
        self.btn_update_hs300_2.setObjectName("btn_update_hs300_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 450, 681, 191))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 210, 681, 231))
        self.textBrowser.setObjectName("textBrowser")
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
        self.btn_update.setText(_translate("MainWindow", "Update"))
        self.by_stock_list.setTitle(_translate("MainWindow", "By Stock List"))
        self.btn_update_sz50.setText(_translate("MainWindow", "Update sz50"))
        self.btn_update_hs300.setText(_translate("MainWindow", "Update hs300"))
        self.btn_update_hs300_2.setText(_translate("MainWindow", "Update zz500"))

