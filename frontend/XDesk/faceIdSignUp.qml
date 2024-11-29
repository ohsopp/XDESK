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
            text: "Face ID를 생성중입니다"
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
            text: "정면을 쳐다봐주세요"
            font.family: "Pretendard ExtraLight"
            font.bold: true
            font.pointSize: 35

            anchors.top: text1.top
            anchors.topMargin: 60
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Image {
            source: "img/faceLogin.png"
            width: 400
            height: 350

            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
        }
    } // 배경 앞 작은 사각형 끝

    Connections { // 페이스 아이디 회원가입 끝나면 제스쳐 확인 페이지로 이동
        target: faceLogin
        function onFaceIdSingUpSuccess() {
            stackView.push("gesture.qml")
        }
    }
} // 배경 사각형 끝
