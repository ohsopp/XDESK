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
        visible: true

        anchors.centerIn: parent

        Text {
            id: text1
            color: "#FFFFFF"
            text: "당신의 제스쳐를 기억하세요"
            font.family: "Pretendard ExtraBold"
            font.bold: true
            font.pointSize: 35

            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: text2
            color: "#FFFFFF"
            text: "Face ID 로그인 시 사용됩니다."
            font.family: "Pretendard Thin"
            font.bold: true
            font.pointSize: 35

            anchors.top: text1.top
            anchors.topMargin: 60
            anchors.horizontalCenter: parent.horizontalCenter
        }

        //제스쳐 사진
        Image {
            source: "img/ges.jpg"
            width: 500
            height: 270
            anchors.top: text2.bottom
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            width: 100
            height: 100
            color:"transparent"
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            Text {
                text: qsTr("확인")
                font.pixelSize: 40
                font.family: "Pretendard ExtraLight"
                color: "#FFFFFF"
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackview.push("deskStandAdjustPage.qml")
                }
            }
        }
    } // 배경 앞 작은 사각형 끝
} // 배경 사각형 끝
