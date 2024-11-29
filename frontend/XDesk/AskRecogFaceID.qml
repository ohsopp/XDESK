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

    Rectangle {
        id: rectangle // 배경 앞 작은 사각형
        width: 920
        height: 500
        color: "#33FFFFFF"  // 투명도 20% 흰색
        border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
        border.width: 1
        radius: 40

        anchors.centerIn: parent

        Text {
            id: text1
            color: "#fefefe"
            text: "얼굴과 제스쳐를 등록 하시겠습니까?"
            font.family: "Pretendard ExtraBold"
            font.bold: true
            font.pointSize: 35

            anchors.top: parent.top
            anchors.topMargin: 100
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: text2
            color: "#ffffff"
            text: "등록시 Face ID로 간편하게 로그인 할 수 있습니다"
            font.family: "Pretendard Thin"
            font.bold: true
            font.pointSize: 28

            anchors.top: text1.bottom
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            id: faceRect
            width: 700
            height: 100
            color: "#A2D2FF"
            radius: 30
            border.color: "#FFFFFF"
            border.width: 1

            anchors.top: text2.bottom
            anchors.topMargin: 80
            anchors.horizontalCenter: parent.horizontalCenter


            Text {
                color: "#ffffff"
                text: "얼굴 인식하기"
                font.styleName: "Normal"
                font.family: "Pretendard ExtraBold"
                font.weight: Font.bold
                font.pointSize: 25

                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.push("faceIdSignUp.qml")
                }
            }
        }

        Rectangle {
            width: 332
            height: 68
            color: "transparent"

            anchors.top: faceRect.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter

            Text {
                color: "#ffffff"
                text: "아니오 등록하지 않겠습니다"
                font.family: "Pretendard Light"
                font.weight: Font.ExtraLight
                font.pointSize: 20

                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.push("deskStandAdjust.qml")
                }
            }
        }
    }
}
