from PyQt5 import QtWidgets, QtGui
import sys
from modules.ui_dao import myWindow

app = QtWidgets.QApplication(sys.argv)
home = myWindow()

home.show()
sys.exit(app.exec_())


# w = QtWidgets.QWidget()
# w.resize(480,320)
# w.setWindowTitle("hello")


# from PyQt5.QtCore import QUrl
# from PyQt5.QtGui import QGuiApplication
# from PyQt5.QtQuick import QQuickView
# from modules.ui_dao import UIDao
# class UI:
#     path = './ui/main.qml'  # 加载的QML文件
#     app = QGuiApplication([])
#     view = QQuickView()
#     dao = UIDao()
#
#     rootContext = view.rootContext()
#     rootContext.setContextProperty("dao", dao)
#     view.setSource(QUrl(path))
#     context = view.rootObject()
#
#     def connections(self):
#         self.context.sendStockCode.connect(self.dao.get_stock_code)  # 连接QML信号sendCLicked
#         self.context.updateStockCode.connect(self.dao.print_stock_code)  # 连接QML信号sendCLicked
#         # self.context.updateSZ50.connect(self.dao.update_sz50())
#
#     def show(self):
#         self.view.show()
#         self.app.exec_()
#
#     def ui_main(self):
#         self.connections()
#         self.show()
#
#
# if __name__ == '__main__':
#     ui = UI()
#     ui.ui_main()
