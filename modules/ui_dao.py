from PyQt5.QtCore import QObject,pyqtSlot
from Apolo.modules.get_data_from_Tushare import test


class UIDao(QObject):
    text = ''
    def __init__(self):
        super(UIDao,self).__init__()
        self.send_text=''

    @pyqtSlot(int, result=str)
    def set_value(self, value):
        return str(value + 20)

    @pyqtSlot(str, result=str)
    def send_msg(self, msg):  # UI -> python console -> UI
        return str(self.send_text)

    @pyqtSlot(str)  # UI -> python console
    def send_msg_2(self,string):
        print(string)

    def print_stock_code(self, code):
        self.send_text = "Get stock code: "+code
        print("Get stock code: "+code)

    # @staticmethod
    def get_stock_code(self, stock_code):
        # self.print_stock_code(stock_code)
        self.send_text = test(stock_code)


