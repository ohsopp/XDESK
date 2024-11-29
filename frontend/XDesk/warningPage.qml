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
    } // 배경색 끝

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
            id: warningText1
            color: "#ffffff"
            text: qsTr("긴급정지 하였습니다.")
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 80
            font.pointSize: 50
            font.family: "Pretendard Black"
        }

        Text {
            id: warningText2
            color: "#ffffff"
            text: qsTr("프로그램을 종료합니다.")
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: warningText1.bottom
            anchors.topMargin: 20
            font.pointSize: 50
            font.family: "Pretendard Light"
        }

        Rectangle {
            width: 700
            height: 100
            radius: 30
            anchors.top: warningText2.bottom
            anchors.topMargin: 50
            anchors.horizontalCenter: warningText2.horizontalCenter

            Text {
                text: qsTr("확인")
                font.family: "Pretendard Medium"
                font.pointSize: 35
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    stackView.clear()
                    stackView.push("FirstPage.qml")
                }
            }
        }


    } // 배경 앞 작은 사각형 끝
} // 배경 사각형 끝
