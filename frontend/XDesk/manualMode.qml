import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle {  //배경 사각형
    width: 1024
    height: 600
    visible: true

    gradient: Gradient { //배경 색
            orientation: Gradient.Vertical
            GradientStop { position: 0.0; color: "#EB99F1" }
            GradientStop { position: 1.0; color: "#7682F0" }
    } //배경 색 종료

    Rectangle { // 배경 앞 작은 사각형
        id: rectangle
        width: 920
        height: 500
        color: "#33FFFFFF"  // 투명도 20% 흰색
        border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
        border.width: 1
        radius: 40
        visible: true

        anchors.centerIn: parent

        Component.onCompleted: {
            servoController.start()
            deskTextContent.text = servoController.update_height("desk")
            standTextContent.text = servoController.update_height("laptop")
        }

        Row { //Row
            width: 920
            height: 500
            anchors.centerIn: parent
            Item { //책상 조절 부분(item1)
                id: item1
                width: 460
                height: 500

                Image {
                    id: deskImg
                    source: "img/desk.png"
                    width: 400
                    height: 300
                    anchors.horizontalCenter: item1.horizontalCenter
                    anchors.top: item1.top
                    anchors.topMargin: 50
                }

                Rectangle {
                    id: deskText
                    width: 300
                    height: 50
                    color: "transparent"
                    border.color: "transparent"
                    anchors.top : deskImg.top
                    anchors.topMargin: 270
                    anchors.horizontalCenter: deskImg.horizontalCenter
                    Text {
                        id: deskTextContent
                        color: "#ffffff"
                        text: qsTr("50cm")
                        font.pointSize: 40
                        font.family: "Pretendard Light"
                        anchors.centerIn: parent
                    }
                }

                Rectangle {
                    id: deskUp
                    width: 100
                    height: 100
                    radius: 30
                    color: "#73FFFFFF"  // 투명도 20% 흰색
                    border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                    anchors.top: item1.top
                    anchors.topMargin: 10
                    anchors.horizontalCenter: item1.horizontalCenter

                    Image {
                        source: "img/arrow.png"
                        width: 50
                        height: 50
                        rotation: 270
                        anchors.centerIn: parent
                    }

                    MouseArea { // 버튼 동작
                        anchors.fill: parent
                        onPressed: {
                            deskUp.color = "#CCFFFFFF"
                            deskTimer.start()
                            servoController.move_desk("up")
                        }
                        onReleased: {
                            deskUp.color = "#73FFFFFF"
                            servoController.stop_desk()
                            deskTimer.stop()
                            deskTextContent.text = servoController.update_height('desk') //수동 조절 후 높이 저장
                            deskStandData.deskHeight = deskTextContent.text
                        }
                    }
                }

                Rectangle {
                    id: deskDown
                    width: 100
                    height: 100
                    radius: 30
                    color: "#73FFFFFF"  // 투명도 20% 흰색
                    border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                    anchors.bottom: item1.bottom
                    anchors.bottomMargin: 10
                    anchors.horizontalCenter: item1.horizontalCenter

                    Image {
                        source: "img/arrow.png"
                        rotation: 90
                        width: 50
                        height: 50
                        anchors.centerIn: parent
                    }

                    MouseArea { // 버튼 동작
                        anchors.fill: parent
                        onPressed: {
                            deskDown.color = "#CCFFFFFF"
                            deskTimer.start()
                            servoController.move_desk("down")
                        }
                        onReleased: {
                            deskDown.color = "#73FFFFFF"
                            servoController.stop_desk()
                            deskTimer.stop()
                            deskTextContent.text = servoController.update_height('desk') //수동 조절 후 높이 저장
                            deskStandData.deskHeight = deskTextContent.text
                        }
                    }
                }

                Timer {
                    id: deskTimer
                    interval: 100 // 100ms 간격으로 업데이트
                    repeat: true
                    onTriggered: {
                        var result = servoController.update_height("desk")
                        deskTextContent.text = result !== undefined ? result : "Unknown"
                    }
                }
            } //책상 조절 부분(item1) 끝

            Item { //거치대 조절 부분(item2)
                id: item2
                width: 460
                height: 500

                // 뒤로가기 버튼
                Rectangle {
                    width:80
                    height: 80
                    color: "transparent"
                    anchors.right: parent.right

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
                            servoController.stop()
                            stackView.pop()
                        }
                    }
                }

                Image {
                    id: standImg
                    source: "img/stand.png"
                    width: 400
                    height: 200
                    anchors.horizontalCenter: item2.horizontalCenter
                    anchors.top: item2.top
                    anchors.topMargin: 120
                }

                Rectangle {
                    id: standText
                    width: 300
                    height: 50
                    color: "transparent"
                    border.color: "transparent"
                    anchors.top:item2.top
                    anchors.topMargin: 320
                    anchors.horizontalCenter: standImg.horizontalCenter
                    Text {
                        id: standTextContent
                        color: "#ffffff"
                        text: qsTr("10cm")
                        font.pointSize: 40
                        font.family: "Pretendard Light"
                        anchors.centerIn: parent
                    }
                }

                Rectangle {
                    id:standUp
                    width: 100
                    height:100
                    radius: 30
                    color: "#73FFFFFF"  // 투명도 20% 흰색
                    border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                    anchors.top: item2.top
                    anchors.topMargin: 10
                    anchors.horizontalCenter: item2.horizontalCenter

                    Image {
                        source: "img/arrow.png"
                        width: 50
                        height: 50
                        rotation: 270
                        anchors.centerIn: parent
                    }

                    MouseArea { // 버튼 동작
                        anchors.fill: parent
                        onPressed: {
                            standUp.color = "#CCFFFFFF"
                            standTimer.start()
                            servoController.move_stand("up")
                        }
                        onReleased: {
                            standUp.color = "#73FFFFFF"
                            servoController.stop_stand()
                            standTimer.stop()
                            standTextContent.text = servoController.update_height('laptop') //수동 조절 후 높이 저장
                            deskStandData.standHeight = standTextContent.text
                        }
                    }
                }

                Rectangle {
                    id: standDown
                    width: 100
                    height: 100
                    radius: 30
                    color: "#73FFFFFF"  // 투명도 20% 흰색
                    border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                    anchors.bottom: item2.bottom
                    anchors.bottomMargin: 10
                    anchors.horizontalCenter: item2.horizontalCenter

                    Image {
                        source: "img/arrow.png"
                        rotation: 90
                        width: 50
                        height: 50
                        anchors.centerIn: parent
                    }

                    MouseArea { // 버튼 동작
                        anchors.fill: parent
                        onPressed: {
                            standDown.color = "#CCFFFFFF"
                            standTimer.start()
                            servoController.move_stand("down")
                        }
                        onReleased: {
                            standDown.color = "#73FFFFFF"
                            servoController.stop_stand()
                            standTimer.stop()
                            standTextContent.text = servoController.update_height('laptop') //수동 조절 후 높이 저장
                            deskStandData.standHeight = standTextContent.text
                        }
                    }
                }

                Timer {
                    id: standTimer
                    interval: 100 // 100ms 간격으로 업데이트
                    repeat: true
                    onTriggered: {
                        var result = servoController.update_height("laptop");
                        standTextContent.text = result !== undefined ? result : "Unknown";
                    }
                }
            } //거치대 조절 부분(item2) 끝
        } //Row 끝
    } // 배경 앞 작은 사각형 끝
} //배경 사각형 끝
