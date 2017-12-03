from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from Apolo.modules.ui_dao import UIDao


def UI_main():
    pass


if __name__ == '__main__':
    path = './ui/main.qml'   # 加载的QML文件

    app = QGuiApplication([])
    view = QQuickView()
    dao = UIDao()
    # view.engine().quit.connect(app.quit)  # TODO: what's it
    rootContext = view.rootContext()
    rootContext.setContextProperty("dao", dao)
    view.setSource(QUrl(path))

    context = view.rootObject()
    context.sendStockCode.connect(dao.get_stock_code)   # 连接QML信号sendCLicked

    view.show()
    app.exec_()