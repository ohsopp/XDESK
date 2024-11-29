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

    Rectangle { // 컨텐츠부분
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
            text: "정면 카메라를 응시해 주세요"
            font.family: "Pretendard ExtraBold"
            font.bold: true
            font.pointSize: 35

            anchors.top: parent.top
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Image {
            source: "img/faceLogin.png"
            width: 400
            height: 400

            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
    Timer { // 화면이 먼저 바뀐 후 얼굴인식
        id: transitionTimer
        interval: 500  // 1초 후에 실행
        repeat: false
        onTriggered: {
            faceLogin.gestureRecog()
        }
    }

    Connections {
        target: faceLogin
        function onFaceRecogFinished() {
            stackView.push("gestureLoginPage.qml")
            transitionTimer.start()
        }
    }

}
