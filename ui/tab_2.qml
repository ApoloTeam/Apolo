import QtQuick 2.0
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.4

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
