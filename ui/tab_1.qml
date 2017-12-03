import QtQuick 2.5
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.4

Item {
    id: root
    width: 640; height: 380
    signal sendClicked(string str) // 定义信号

    GridLayout {
        id: grid
        width: parent.width
        height: parent.height
        columns: 1
        rows: 3
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
                    text: "123456"
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
                            root.sendClicked(inp_stock.getText(0,inp_stock.length))    // 发射信号到Python
                        }
                    }
                }

                Button {
                    id: btn_update
                    text: "Update"
                    anchors.left: btn_search.right
                    MouseArea {
                        id: mouse_area_1
                        anchors.fill: parent
                        onClicked: {
                            console.log("btn_update test...")
                            txt1.text = con.returnValue(20)
                        }
                    }
                }

            }
        }
        TextArea{
            id: txt1
            width: parent.width
            height: parent.height
            anchors.bottom: parent.bottom
            transformOrigin: Item.Center
            Layout.fillHeight: false
            Layout.fillWidth: true
        }
    }
}
