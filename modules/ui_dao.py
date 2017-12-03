from PyQt5.QtCore import QObject,pyqtSlot
from Apolo.modules.get_data_from_Tushare import test


class UIDao(QObject):

    @pyqtSlot(int, result=str)
    def set_value(self, value):
        return str(value + 20)

    @pyqtSlot(str, result=str)
    def send_msg(self, msg):
        return str(msg)

    def print_stock_code(self, code):
        print("Get stock code: "+code)

    # @pyqtSlot(int, result=str)s
    # @staticmethod
    def get_stock_code(self, stock_code):
        self.print_stock_code(stock_code)
        t = test(stock_code)
        self.send_msg(t)



def get_string(str_value):
    print("Get shock code: " + str_value)
    return str_value

