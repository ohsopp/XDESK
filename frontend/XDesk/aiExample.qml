import QtQuick 2.15
import QtQuick.Controls 2.15

//배경
Rectangle {
    id: rectangle
    width: 1024
    height: 600

    gradient: Gradient {
        orientation: Gradient.Vertical  // 배경색
        GradientStop { position: 0.0; color: "#EB99F1" }
        GradientStop { position: 1.0; color: "#7682F0" }
    }

    // Rectangle { // 배경 블라인드 처리
    //     width: 1024
    //     height: 600
    //     color: "#FFFFFF"
    //     opacity: 0.6
    //     visible: true
    // }

    Rectangle {
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
            text: qsTr("화면과 같이 자세를 취해주세요")
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top : parent.top
            anchors.topMargin: 40
            font.family: "Pretendard Black"
            font.pointSize: 40
            color:"#FFFFFF"
        }

        Image {
            source: "img/pic.png"
            width: 600
            height: 350
            anchors.top: text1.bottom
            anchors.horizontalCenter: text1.horizontalCenter
            anchors.topMargin: 20
        }
    }

}
