import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle {  //배경 사각형
    width: 1024
    height: 600

    Image {
        source: "img/beginBack.png" // 표시할 이미지 파일 경로
        anchors.fill: parent
        fillMode: Image.PreserveAspectCrop // 이미지를 화면에 꽉 차게 유지하면서 비율을 유지
    }

    Row {

        anchors.centerIn: parent
        spacing: 70

        Column {
            anchors.verticalCenter: parent.verticalCenter

            Text {
                id: c1
                text: "XD"
                font.family: "Pretendard Black"
                color: "#404040"
                font.pointSize: 60
                font.weight: Font.Bold
            }

            Text {
                text: "Liberating"
                font.family: "Pretendard Black"
                color: "#404040"
                font.pointSize: 60
                font.weight: Font.Bold
            }

            Text {
                text: "Comfort"
                font.family: "Pretendard Black"
                color: "#404040"
                font.pointSize: 60
                font.weight: Font.Bold
            }

        }


        Image {
            anchors.verticalCenter: parent.verticalCenter

            id: i1
            source: "img/desk.png"
            width: 400
            height: 400
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            stackView.push("loginPage.qml")
        }
    }
}
