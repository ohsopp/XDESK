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

    Rectangle { // 저장 페이지 배경
        width: 470
        height: 370
        color: "#33FFFFFF"  // 투명도 20% 흰색
        border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
        border.width: 1
        radius: 40
        anchors.centerIn: parent

        Rectangle {
            width: 50
            height: 50
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.topMargin: 15
            anchors.rightMargin: 15
            radius: 20
            opacity: 1
            color: "transparent"

            Image {
                source: "img/x-white.png"
                width: 30
                height: 30
                anchors.centerIn: parent
            }
        }

        Rectangle { // 제목 입력 사각형
            id: titleRect
            width: 330
            height: 50
            radius: 20
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top : parent.top
            anchors.topMargin: 70


            TextField {
                color: "#eb99f1" // 제목 입력 필드
                font.pointSize: 18
                font.family: "Pretendard Light"
                placeholderText: "제목을 입력해주세요"
                anchors.centerIn: parent
            }
        }

        Text {
            id: deskText
            text: qsTr("책상 높이: 200cm")
            anchors.top : titleRect.bottom
            anchors.topMargin: 20
            font.family: "Pretendard Medium"
            font.pointSize: 18
            color:"#FFFFFF"
            anchors.horizontalCenter: titleRect.horizontalCenter
        }


        Text {
            id: standText
            text: qsTr("거치대 높이: 100cm")
            anchors.top : deskText.bottom
            anchors.topMargin: 10
            font.family: "Pretendard Medium"
            font.pointSize: 18
            color:"#FFFFFF"
            anchors.horizontalCenter: deskText.horizontalCenter
        }

        Rectangle {
            width: 200
            height: 100
            radius: 20
            color: "#F9F2FD"

            anchors.top : standText.bottom
            anchors.horizontalCenter: standText.horizontalCenter
            anchors.topMargin: 30

            Text {
                text: qsTr("저장")
                font.pointSize: 30
                font.family: "Pretendard SemiBold"
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.pop()
                }
            }
        }
    }

}
