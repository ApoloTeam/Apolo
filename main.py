from PyQt5.QtCore import QUrl,QObject,pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

class MyClass(QObject):
    @pyqtSlot(int, result=str)
    def returnValue(self, value):
        return str(value+20)

    @pyqtSlot(int, result=str)
    def outputString(string):
        print(string)

def outputString():
    print('hi')


if __name__ == '__main__':
    path='./ui/main.qml'
    app = QGuiApplication([])
    view=QQuickView()
    con = MyClass()

    rootContext=view.rootContext()
    rootContext.setContextProperty("con", con)

    view.setSource(QUrl(path))

    rootObject = view.rootObject()
    # rootObject.sendClicked()
    # view.engine().quit.connect(app.quit)
    view.show()
    app.exec_()


# if __name__ == '__main__':
#     path = './ui/tab_2.qml'   # 加载的QML文件
#
#     app = QGuiApplication([])
#     view = QQuickView()
#     view.engine().quit.connect(app.quit)
#     view.setSource(QUrl(path))
#     view.show()
#     context = view.rootObject()
#     context.sendClicked.connect(outputString)   # 连接QML信号sendCLicked
#     app.exec_()