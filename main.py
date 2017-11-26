from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from Apolo.modules.qml_getter_setter import GetterSetter
from Apolo.modules.qml_getter_setter import get_string


if __name__ == '__main__':
    path = './ui/main.qml'   # 加载的QML文件

    app = QGuiApplication([])
    view = QQuickView()
    con = GetterSetter()
    # view.engine().quit.connect(app.quit)  # TODO: what's it
    rootContext=view.rootContext()
    rootContext.setContextProperty("con", con)
    view.setSource(QUrl(path))
    view.show()
    context = view.rootObject()
    context.sendClicked.connect(get_string)   # 连接QML信号sendCLicked
    app.exec_()