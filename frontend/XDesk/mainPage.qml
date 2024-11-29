import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {  // 배경 사각형
    width: 1024
    height: 600
    visible: true

    gradient: Gradient { // 배경 색
        orientation: Gradient.Vertical
        GradientStop { position: 0.0; color: "#EB99F1" }
        GradientStop { position: 1.0; color: "#7682F0" }
    }

    property bool doNotDisturb: false // 전역 방해금지 상태

    ImageDialogPage {
        id: imageDialogComponent
    }

    LogoutDialogPage {
        id: logoutDialogComponent
    }


    Column {
        width: 820
        height: 490
        spacing: 50

        anchors.centerIn: parent
        Row {
            width: 820
            height: 220
            spacing: 80
            anchors.horizontalCenter: parent.horizontalCenter

            // 방해금지 버튼
            Rectangle {
                id: disturbButton
                width: 220
                height: 220
                color: "#33FFFFFF"  // 투명도 20% 흰색
                radius: 30
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img1
                    source: "img/close-white.png"
                    width: 120
                    height: 120
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                }

                Text {
                    id: text1
                    text: qsTr("방해금지")
                    anchors.top: img1.bottom
                    anchors.topMargin: 20
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"
                    anchors.horizontalCenter: img1.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        doNotDisturb = !doNotDisturb
                        if (doNotDisturb) {
                            text1.color = "black"
                            img1.source = "img/close-black.png"
                            disturbButton.color = "#CCFFFFFF"
                        } else {
                            text1.color = "#FFFFFF"
                            img1.source = "img/close-white.png"
                            disturbButton.color = "#33FFFFFF"
                        }
                    }
                }
            }

            // 수동모드 버튼
            Rectangle {
                width: 220
                height: 220
                radius: 30
                color: "#33FFFFFF"  // 투명도 20% 흰색
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img2
                    source: "img/height.png"
                    width: 120
                    height: 120
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                }

                Text {
                    text: qsTr("수동모드")
                    anchors.top: img2.bottom
                    anchors.topMargin: 20
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"

                    anchors.horizontalCenter: img2.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    enabled: !doNotDisturb
                    onClicked: {
                        stackView.push("manualMode.qml")
                    }
                }
            }

            // 저장소 버튼
            Rectangle {
                width: 220
                height: 220
                radius: 30
                color: "#33FFFFFF"  // 투명도 20% 흰색
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img3
                    source: "img/save.png"
                    width: 120
                    height: 120
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                }

                Text {
                    text: qsTr("저장소")
                    anchors.top: img3.bottom
                    anchors.topMargin: 20
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"

                    anchors.horizontalCenter: img3.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    enabled: !doNotDisturb
                    onClicked: {
                        stackView.push("deskStandStore.qml")
                    }
                }
            }
        }

        Row {
            width: 820
            height: 220
            spacing: 80
            anchors.horizontalCenter: parent.horizontalCenter

            // 타이머 버튼
            Rectangle {
                width: 220
                height: 220
                radius: 30
                color: "#33FFFFFF"  // 투명도 20% 흰색
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img4
                    source: "img/clock-white.png"
                    width: 120
                    height: 120
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                }

                Text {
                    text: qsTr("타이머")
                    anchors.top: img4.bottom
                    anchors.topMargin: 20
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"
                    anchors.horizontalCenter: img4.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    enabled: !doNotDisturb
                    onClicked: {
                        stackView.push("timerPage.qml")
                    }
                }
            }

            // 내 그래프 버튼
            Rectangle {
                width: 220
                height: 220
                radius: 30
                color: "#33FFFFFF"  // 투명도 20% 흰색
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img5
                    source: "img/graph"
                    width: 150
                    height: 150
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 10
                }

                Text {
                    text: qsTr("자세 그래프")
                    anchors.top: img5.bottom
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"
                    anchors.horizontalCenter: img5.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    enabled: !doNotDisturb
                    onClicked: {
                        monthGraph.getData()
                    }
                }
            }

            // 종료 버튼
            Rectangle {
                width: 220
                height: 220
                radius: 30
                color: "#33FFFFFF"  // 투명도 20% 흰색
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Image {
                    id: img6
                    source: "img/turn-off.png"
                    width: 120
                    height: 120
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                }

                Text {
                    text: qsTr("로그아웃")
                    anchors.top: img6.bottom
                    anchors.topMargin: 20
                    font.family: "Pretendard ExtraBold"
                    font.pointSize: 27
                    color: "#FFFFFF"
                    anchors.horizontalCenter: img6.horizontalCenter
                }

                MouseArea {
                    anchors.fill: parent
                    enabled: !doNotDisturb
                    onClicked: {
                        stackView.clear()
                        stackView.push("FirstPage.qml")
                    }
                }
            }
        }
    }
}
