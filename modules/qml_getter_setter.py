from PyQt5.QtCore import QObject,pyqtSlot


class GetterSetter(QObject):
    @pyqtSlot(int, result=str)
    def set_value(self, value):
        return str(value + 20)

    # @pyqtSlot(int, result=str)
    # @staticmethod
    def get_string(self, str_value):
        print(str_value)


def get_string(str_value):
    print(str_value)
