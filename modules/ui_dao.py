from PyQt5 import QtWidgets, QtGui
from ui.home import Ui_MainWindow

# class myWindow(QtWidgets.QWidget,Ui_MainWindow):
class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        # self.setupUi(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_search.clicked.connect(self.hello)

    def hello(self):
        self.ui.plainTextEdit.appendPlainText("hello, World")
        print('hello')



# from PyQt5.QtCore import QObject,pyqtSlot
# from modules.get_data_from_Tushare import test
# from modules.admin_database import AdminDatabase
#
#
# class UIDao(QObject):
#     text = ''
#     def __init__(self):
#         super(UIDao,self).__init__()
#         self.send_text=''
#
#     @pyqtSlot(int, result=str)
#     def set_value(self, value):
#         return str(value + 20)
#
#     @pyqtSlot(str, result=str)
#     def send_msg(self, msg):  # UI -> python console -> UI
#         return str(self.send_text)
#
#     @pyqtSlot(str)  # UI -> python console
#     def send_msg_2(self,string):
#         print(string)
#
#     def print_stock_code(self, code):
#         self.send_text = "Get stock code: "+code
#         print("Get stock code: "+code)
#
#     # @staticmethod
#     def get_stock_code(self, stock_code):
#         # self.print_stock_code(stock_code)
#         self.send_text = test(stock_code)
#
#     def update_sz50(self):
#         self.send_text = AdminDatabase.update_data_sz50()
