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
    }

    Text {
        id: text1
        color: "#FFFFFF"
        text: "책상 및 노트북 거치대의 높이를 조정합니다"
        font.family: "Pretendard ExtraBold"
        font.bold: true
        font.pointSize: 35

        anchors.top: parent.top
        anchors.topMargin: 60
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Text {
        id: text2
        color: "#FFFFFF"
        text: "원하는 기능을 선택해주세요"
        font.family: "Pretendard Thin"
        font.bold: true
        font.pointSize: 28

        anchors.top: text1.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Row {
        spacing: 60
        anchors.top: text2.bottom
        anchors.topMargin: 50
        anchors.horizontalCenter: parent.horizontalCenter

        Rectangle {
            id: ai
            width: 260
            height: 310
            color: "#33FFFFFF"
            radius: 20
            border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
            border.width: 1

            Image {
                id: aiImg
                source: "img/auto.png"
                width: 100
                height: 100

                anchors.top: parent.top
                anchors.topMargin: 40
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: aiTitle
                text: "AI 추천"
                font.family: "Pretendard Medium"
                font.pointSize: 30
                color: "#FFFFFF"

                anchors.top: aiImg.bottom
                anchors.topMargin: 30
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: aiSub1
                text: "AI가 체형에 맞게"
                font.family: "Pretendard Light"
                font.pointSize: 14
                color: "#FFFFFF"

                anchors.top: aiTitle.bottom
                anchors.topMargin: 20
                anchors.horizontalCenter: parent.horizontalCenter

            }

            Text {
                id: aiSub2
                text:"높이를 맞춰줘요"
                font.family: "Pretendard Light"
                font.pointSize: 14
                color: "#FFFFFF"

                anchors.top: aiSub1.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.push("aiExample.qml")
                    transitionTimer.start()
                }
            }
        }

        Rectangle {
            id: store
            width:260
            height: 310
            color: "#33FFFFFF"
            radius: 20
            border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
            border.width: 1

            Image {
                id:storeImg
                source: "img/save.png"
                width: 100
                height: 100

                anchors.top: parent.top
                anchors.topMargin: 40
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: storeTitle
                color: "#FFFFFF"
                text: "저장소"
                font.family: "Pretendard Medium"
                font.pointSize: 30

                anchors.top: storeImg.bottom
                anchors.topMargin: 30
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: storeSub
                text: "저장된 데이터 불러오기"
                font.pointSize: 14
                font.family: "Pretendard Light"
                color: "#FFFFFF"

                anchors.top: storeTitle.bottom
                anchors.topMargin: 25
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.push("deskStandStore.qml")
                }
            }
        }

        Rectangle {
            id: none
            width: 260
            height: 310
            color: "#33FFFFFF"  // 투명도 20% 흰색
            radius: 20
            border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
            border.width: 1

            Image {
                id: noneImg
                source: "img/close-white.png"
                width: 100
                height: 100

                anchors.top: parent.top
                anchors.topMargin: 40
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: noneTitle
                color: "#FFFFFF"
                text: "사용 안함"
                font.pointSize: 30
                font.family: "Pretendard Medium"

                anchors.top: noneImg.bottom
                anchors.topMargin: 30
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: nonSub1
                text: "수동모드로 직접"
                font.family: "Pretendard Light"
                font.pointSize: 14
                color: "#FFFFFF"

                anchors.top: noneTitle.bottom
                anchors.topMargin: 20
                anchors.horizontalCenter: parent.horizontalCenter


            }

            Text {
                color: "#FFFFFF"
                text:"높이를 조절할 수 있어요"
                font.family: "Pretendard Light"
                font.pointSize: 14

                anchors.top: nonSub1.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.push("mainPage.qml")
                }
            }
        }
    }

    Timer { // 화면이 먼저 바뀐 후 책상 조절
        id: transitionTimer
        interval: 1000  // 1초 후에 실행
        repeat: false
        onTriggered: {
            pyinterface.runScript()
        }
    }

    Connections {
        target: pyinterface
        function onScriptFinished() {
            stackView.push("mainPage.qml")
        }
    }
} // 배경 사각형 끝

