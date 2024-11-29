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
                    stackView.pop()
                }
            }
        }

        Rectangle {
            id: faceIdRect
            width: 350
            height: 350
            radius: 30
            color: "#EBC5F2"
            border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
            border.width: 1
            anchors.left: parent.left
            anchors.leftMargin: 75
            anchors.verticalCenter: parent.verticalCenter

            Image { // 얼굴 로그인 이모티콘
                anchors.centerIn: parent

                source: "img/faceId"
                width: 300
                height: 300
            }
        }

        Text {
            color: "#FFFFFF"
            text: "face ID 로그인"
            font.styleName: "Bold"
            font.pointSize: 30
            anchors.top: faceIdRect.bottom
            font.family: "Pretendard Medium"
            anchors.horizontalCenter: faceIdRect.horizontalCenter
        }

        Rectangle {
            id: graphRect
            width: 350
            height: 350
            radius: 30
            color: "#f3c8df"
            border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
            border.width: 1
            anchors.right: parent.right
            anchors.rightMargin: 75
            anchors.verticalCenter: parent.verticalCenter

            Image { // 얼굴 로그인 이모티콘
                anchors.centerIn: parent

                source: "img/graph"
                width: 300
                height: 300
            }
        }

        Text {
            color: "#FFFFFF"
            text: "자세 그래프"
            font.styleName: "Bold"
            font.pointSize: 30
            anchors.top: graphRect.bottom
            font.family: "Pretendard Medium"
            anchors.horizontalCenter: graphRect.horizontalCenter
        }


    } // 배경 앞 작은 사각형 끝
} //배경 사각형 끝
