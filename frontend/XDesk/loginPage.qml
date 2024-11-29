import QtQuick 2.15
import QtQuick.Controls 2.15

//배경
Rectangle {
    id: rectangle
    width: 1024
    height: 600
    visible: true
    gradient: Gradient {
        orientation: Gradient.Vertical  // 배경색
        GradientStop { position: 0.0; color: "#EB99F1" }
        GradientStop { position: 1.0; color: "#7682F0" }
    }

    // 얼굴 로그인 버튼
    Rectangle {  // 얼굴 로그인 버튼 배경
        id: faceIdRect
        width: 300
        height: 300
        color: "#33FFFFFF"  // 투명도 20% 흰색
        border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
        border.width: 1
        radius: 30
        anchors.left: parent.left
        anchors.leftMargin: 130
        anchors.verticalCenter: parent.verticalCenter

        Image { // 얼굴 로그인 이모티콘
            anchors.centerIn: parent

            source: "img/faceId"
            width: 300
            height: 300
        }

        MouseArea { // 얼굴 로그인 버튼 동작
            anchors.fill: parent
            onClicked: {
                stackView.push("faceLoginPage.qml")
                transitionTimer.start()
            }
        }
    }

    Text {
        color: "#FFFFFF"
        text: "face ID 로그인"
        font.styleName: "Bold"
        font.pointSize: 30
        anchors.top: faceIdRect.bottom
        font.family: "Pretendard Thin"
        anchors.topMargin: 10
        anchors.horizontalCenter: faceIdRect.horizontalCenter
    }

    Rectangle{
        width: 425
        height: 100
        color: "transparent"
        anchors.top: parent.top
        anchors.topMargin: 160
        anchors.left: faceIdRect.right
        anchors.leftMargin: 80

        //네이버 로그인 버튼
        Image {
            source: "img/naverLogin.png"
            width: 425
            height: 100
            anchors.centerIn: parent
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                naverLogin.openNaverLoginWindow()
            }
        }
    }

    Rectangle{  //카카오 로그인 버튼
        width: 425
        height: 100
        color: "transparent"
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 160
        anchors.left: faceIdRect.right
        anchors.leftMargin: 80

        Image {
            source: "img/kakaoLogin.png"
            width: 425
            height: 100
            anchors.centerIn: parent
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                kakaoLogin.openKakaoLoginWindow()
            }
        }
    }

    Timer { // 화면이 먼저 바뀐 후 얼굴인식
        id: transitionTimer
        interval: 500
        repeat: false
        onTriggered: {
            faceLogin.faceIdRecog()
        }
    }

    Connections {
        target: faceLogin
        function onFaceRecogFinished() {
            stackView.push("gestureLoginPage.qml")
        }

        function onFaceLoginFailed() {
            stackView.push("faceLoginFail.qml")
        }
    }
}
