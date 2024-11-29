import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle {  //배경
    width: 1024
    height: 600
    visible: true

    gradient: Gradient { //배경 색
            orientation: Gradient.Vertical
            GradientStop { position: 0.0; color: "#EB99F1" }
            GradientStop { position: 1.0; color: "#7682F0" }
    }

    Rectangle { // 콘텐츠
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
            text: "로그인에 실패하였습니다"
            font.styleName: "Regular"
            font.family: "Pretendard ExtraBold"
            font.pointSize: 46
            font.weight: Font.Normal
            color:"#FFFFFF"

            anchors.top: parent.top
            anchors.topMargin: 140
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            width: 700
            height: 100
            color: "#A2D2FF"
            radius: 30
            border.color: "#FFFFFF"
            border.width: 1

            anchors.top: text1.bottom
            anchors.topMargin: 90
            anchors.horizontalCenter: parent.horizontalCenter


            Text {
                color: "#ffffff"
                text: "확인"
                font.styleName: "Normal"
                font.family: "Pretendard ExtraBold"
                //font.weight: Font.bold
                font.pointSize: 32

                anchors.centerIn: parent
            }

            MouseArea { // 얼굴인식 실패시 로그인 페이지로 이동
                anchors.fill: parent
                onClicked: {
                    stackView.push("loginPage.qml")
                }
            }
        }

    }
}
