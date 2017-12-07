import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: root
    width: 640; height: 380
    signal sendStockCode(string str) // 定义信号
    signal updateStockCode(string str) // 定义信号

    GridLayout {
        id: grid
        width: parent.width
        height: parent.height
        columns: 1
        rows: 1
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 12
        anchors.leftMargin: 12
        anchors.topMargin: 12
        anchors.bottomMargin: 12
        columnSpacing: 8
        rowSpacing: 8

        GroupBox {
            title: "Parameter"
            anchors.top: parent.top
            anchors.left: parent.left

            RowLayout {
                anchors.fill: parent

                Label {
                    id: lbl_Stock
                    text: qsTr("Stock Code")
                }

                TextField {
                    id: inp_stock
                    anchors.left: lbl_Stock.right
                    text: "603882"
                }
                Button {
                    id: btn_search
                    text: "Search"
                    anchors.left: inp_stock.right
                    MouseArea {
                        id: msa_search
                        anchors.fill: parent
                        onClicked: {
                            console.log("btn_search test...")
                            root.sendStockCode(inp_stock.getText(0,inp_stock.length))    // 发射信号到Python
                            txt_area.append(dao.send_msg("Searching"))
//                            txt_area.text = dao.set_value(20)
                        }
                    }
                }

                Button {
                    id: btn_update
                    text: "Update"
                    anchors.left: btn_search.right
                    MouseArea {
                        id: msa_update
                        anchors.fill: parent
                        onClicked: {
                            console.log("btn_update test...")
                            root.updateStockCode(inp_stock.getText(0,inp_stock.length))    // 发射信号到Python
                            txt_area.append(dao.send_msg("Updating"))
                        }
                    }
                }
            }
        }
        TextArea{
            id: txt_area
            width: parent.width
            height: 300
            anchors.bottom: parent.bottom
            transformOrigin: Item.Center
            Layout.fillHeight: false
            Layout.fillWidth: true
        }
    }
}


//TODO: Tab mode
//ApplicationWindow {
//    visible: true
//    width: 640
//    height: 480
//    title: "Apolo"

//    menuBar: MenuBar {
//        Menu {
//            title: qsTr("File")
//            MenuItem {
//                text: qsTr("&Open")
//                onTriggered: console.log("Open action triggered");
//            }
//            MenuItem {
//                text: qsTr("Exit")
//                onTriggered: Qt.quit();
//            }
//        }
//    }

//    TabView {
//        id: tab_view
//        anchors.fill: parent

//        Tab {
//            title: "tab_1"
//            source: "tab_1.qml"
//        }
//        Tab {
//            title: "tab_2"
//            source: "tab_1.qml"
//        }

//        //    Label {
//        //        text: qsTr("Hello World")
//        //        anchors.centerIn: parent
//        //    }

//    }
//}
