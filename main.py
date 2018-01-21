from PyQt5 import QtWidgets
import sys
from modules.ui_dao import ApoloWindow

app = QtWidgets.QApplication(sys.argv)
home = ApoloWindow()

home.show()
sys.exit(app.exec_())
