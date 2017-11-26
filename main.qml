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

    }

    Item {
        id: tab1
        anchors.top: tab_view.bottom
        width: parent.width
        height:parent.height

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
                        text: qsTr("Stock Code")
                        //                        Font.pixelSize: 12
                    }
                    TextField {
                        id: inp_stock
                    }
                    Button {
                        text: "Search"
                    }
                    Button {
                        text: "Update"
                    }
                }
            }

            TextArea{
                width: parent.width
                height: parent.height
                anchors.bottom: parent.bottom
                transformOrigin: Item.Center
                Layout.fillHeight: false
                Layout.fillWidth: true

            }
        }
        //    Label {
        //        text: qsTr("Hello World")
        //        anchors.centerIn: parent
        //    }
    }
}
