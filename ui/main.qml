import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Apolo"

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("&Open")
                onTriggered: console.log("Open action triggered");
            }
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    TabView {
        id: tab_view
        anchors.fill: parent

        Tab {
            title: "tab_1"
            source: "tab_1.qml"
        }
        Tab {
            title: "tab_2"
            Rectangle {
                id: root
                width: 320; height: 240
                color: "lightgray"
                signal sendClicked(string str) // 定义信号

                Text {
                    id: txt
                    text: "Clicked me"
                    font.pixelSize: 20
                    anchors.centerIn: parent
                    MouseArea {
                        id: mouse_area
                        anchors.fill: parent  // 有效区域
                        onClicked: {
                            root.sendClicked("Hello, Python3")    // 发射信号到Python
                        }
                    }
                }

                TextField {
                    id: inp_stock
                    text: "123456"
                }
                Button {
                    id: btn_search
                    text: "Search"
                    anchors.top: inp_stock.bottom
                    MouseArea {
                        id: mouse_area_1
                        anchors.fill: parent
                        onClicked: {
                            console.log("test...")
                            root.sendClicked(inp_stock.getText(0,inp_stock.length))    // 发射信号到Python
                        }
                    }
                }
            }
        }

        //    Label {
        //        text: qsTr("Hello World")
        //        anchors.centerIn: parent
        //    }

    }
}
