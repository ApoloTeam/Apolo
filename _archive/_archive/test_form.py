from PyQt5 import QtWidgets, QtGui
import sys
from Apolo.ui.form import Ui_Form   #  导入生成form.py里生成的类
from Apolo.ui.Test_text import return_text

class mywindow(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    #  定义槽函数
    def hello(self):
        a=return_text()
        print(a+'def')
        self.textEdit.setText("123")

app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.show()
sys.exit(app.exec_())
