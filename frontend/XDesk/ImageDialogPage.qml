import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: mainWindow
    visible: false
    width: 800
    height: 480
    flags: Qt.FramelessWindowHint

    Dialog {
        id: imageDialog
        width: parent.width 
        height: parent.height 
        modal: true
        closePolicy: Popup.CloseOnEscape 

        Rectangle {
            anchors.fill: parent
            color: "skyblue"

            Text {
                id: titleText
                text: "3개월 간 자세는 이랬어요"
                font.pointSize: 20
                font.bold: true
                color: "black"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 2
            }

            Image {
                id: popupImage
                anchors.centerIn: parent
                source: "data:image/png;base64," + imageBase64
                fillMode: Image.PreserveAspectFit
                width: parent.width
                height: parent.height
                visible: imageBase64 !== ""  
            }

            Rectangle {
                width: 30
                height: 30
                color: "transparent"
                anchors.top: parent.top
                anchors.topMargin: 5 
                anchors.right: parent.right
                anchors.rightMargin: 10 

                Image {
                    source: "img/x-white.png"
                    rotation: 180
                    width: 30
                    height: 30
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        imageDialog.close()
                    }
                }
            }
        }

        onOpened: {
            mainWindow.visible = true
        }

        onClosed: {
            mainWindow.visible = false
        }
    }

    Component.onCompleted: {
        monthGraph.GraphDataReceived.connect(function(imageBase64String) {
            imageBase64 = imageBase64String
            imageDialog.open()
        })
    }

    property string imageBase64: ""
}
