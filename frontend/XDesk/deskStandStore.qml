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

    property var rect1Data: null
    property var rect2Data: null
    property var rect3Data: null

    Component.onCompleted: { //초기화 시 책상 거치대 데이터 가져오기
        deskStandData.getData()
        servoController.start()
    }

    Connections { // 각 저장소 데이터 나눠주기
        target: deskStandData
        function onDeskStandDataReceived(data) {
            if (data.xdesk && data.xdesk[0]) {
                rect1Data = data.xdesk[0]
            }
            if (data.xdesk && data.xdesk[1]) {
                rect2Data = data.xdesk[1]
            }
            if (data.xdesk && data.xdesk[2]) {
                rect3Data = data.xdesk[2]
            }
        }
    }

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
                servoController.stop()
                stackView.pop()
            }
        }
    } // 뒤로가기 버튼 끝

    Text {
        id: text1
        color: "#FFFFFF"
        text: "책상 및 노트북 거치대의 데이터를 불러옵니다"
        font.family: "Pretendard ExtraBold"
        font.bold: true
        font.pointSize: 35
        anchors.top: parent.top
        anchors.topMargin: 60
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Text {
        id: text2
        color: "#FFFFFF"
        text: "원하는 설정을 선택해주세요"
        font.family: "Pretendard Thin"
        font.bold: true
        font.pointSize: 28
        anchors.top: text1.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
    }

    //데이터 공간
    Row {
        spacing: 60
        anchors.top: text2.bottom
        anchors.topMargin: 50
        anchors.horizontalCenter: parent.horizontalCenter

        Item{ // 데이터 표시 공간 1
            width: 260
            height: 345

            Rectangle {
                id: rect1
                width: 260
                height: 310
                color: "#33FFFFFF"  // 투명도 20% 흰색
                radius: 20
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Rectangle { // 데이터가 있을 때 보여지는 이미지와 텍스트
                    id: hasData1
                    width: 220
                    height: 290
                    color: "transparent"
                    visible: rect1Data !== null
                    anchors.centerIn: parent
                    // 이미지
                    Image {
                        id: img1
                        width: 100
                        height: 100
                        source: "img/miniDesk.png"
                        anchors.top: parent.top
                        anchors.topMargin: 50
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                    }

                    Text {
                        id: deskHeight1
                        text: "책상 높이:" + String(rect1Data.desk_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: img1.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: img1.bottom
                        anchors.topMargin: 10
                        font.family: "Pretendard Light"
                        font.pointSize: 17
                    }

                    Text {
                        text: "거치대 높이:" + String(rect1Data.stand_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: deskHeight1.bottom
                        font.pointSize: 17
                        font.family: "Pretendard Light"
                    }
                }

                Image { // 저장된 데이터가 없을 때 표시할 기본 이미지
                    source: "img/plus-white.png"
                    width: 100
                    height: 100
                    visible: rect1Data === null
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (rect1Data === null){
                            deskStandData.addData(1)
                            stackView.replace("deskStandStore.qml")
                        } else {
                            //불러온 데이터로 책상 조절하는 함수 필요
                            servoController.save_desk(rect1Data.desk_height)
                            servoController.save_stand(rect1Data.stand_height)
                            servoController.stop()
                            stackView.replace("mainPage.qml")
                        }
                    }
                }
            }

            Row { // 데이터를 수정, 삭제 할 수 있는 버튼
                id: row1
                anchors.top: rect1.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: rect1.horizontalCenter
                spacing: 20
                visible: rect1Data !== null

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#A2D2FF"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("덮어쓰기")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.updateData(1)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#FFC8DD"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("삭제")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.deleteData(1)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }
            }
        }

        Item{ // 데이터 표시 공간 2
            width: 260
            height: 345

            Rectangle {
                id: rect2
                width: 260
                height: 310
                color: "#33FFFFFF"  // 투명도 20% 흰색
                radius: 20
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Rectangle { // 데이터가 있을 때 보여지는 이미지와 텍스트
                    id: hasdata2
                    width: 220
                    height: 290
                    color: "transparent"
                    visible: rect2Data !== null //데이터가 있다면 보임
                    anchors.centerIn: parent
                    // 이미지
                    Image {
                        id: img2
                        width: 100
                        height: 100
                        source: "img/miniDesk.png"
                        anchors.top: parent.top
                        anchors.topMargin: 50
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                    }

                    Text {
                        id: deskHeight2
                        text: "책상 높이:" + String(rect2Data.desk_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: img2.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: img2.bottom
                        anchors.topMargin: 10
                        font.family: "Pretendard Light"
                        font.pointSize: 17
                    }

                    Text {
                        text: "거치대 높이:" + String(rect2Data.stand_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: deskHeight2.bottom
                        font.pointSize: 17
                        font.family: "Pretendard Light"
                    }
                }

                Image { // 저장된 데이터가 없을 때 표시할 기본 이미지
                    source: "img/plus-white.png"
                    width: 100
                    height: 100
                    visible: rect2Data === null  //데이터가 없다면 보임
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (rect2Data === null){
                            deskStandData.addData(2)
                            stackView.replace("deskStandStore.qml")
                        } else {
                            //불러온 데이터로 책상 조절하는 함수 필요
                            servoController.save_desk(rect2Data.desk_height)
                            servoController.save_stand(rect2Data.stand_height)
                            servoController.stop()
                            stackView.replace("mainPage.qml")
                        }
                    }
                }
            }

            Row { // 데이터를 수정, 삭제 할 수 있는 버튼
                id: row2
                anchors.top: rect2.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: rect2.horizontalCenter
                spacing: 20
                visible: rect2Data !== null // 데이터가 있다면 보임

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#A2D2FF"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("덮어쓰기")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.updateData(2)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#FFC8DD"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("삭제")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.deleteData(2)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }
            }
        }

        Item{ // 데이터 표시 공간 3
            width: 260
            height: 345

            Rectangle {
                id: rect3
                width: 260
                height: 310
                color: "#33FFFFFF"  // 투명도 20% 흰색
                radius: 20
                border.color: "#80FFFFFF" //투명도 50% 흰색 테두리
                border.width: 1

                Rectangle { // 데이터가 있을 때 보여지는 이미지와 텍스트
                    id: hasdata3
                    width: 220
                    height: 290
                    color:"transparent"
                    visible: rect3Data !== null
                    anchors.centerIn: parent
                    // 이미지
                    Image {
                        id: img3
                        width: 100
                        height: 100
                        source: "img/miniDesk.png"
                        anchors.top: parent.top
                        anchors.topMargin: 50
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                    }

                    Text {
                        id: deskHeight3
                        text: "책상 높이:" + String(rect3Data.desk_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: img3.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: img3.bottom
                        anchors.topMargin: 10
                        font.family: "Pretendard Light"
                        font.pointSize: 17
                    }

                    Text {
                        text: "거치대 높이:" + String(rect3Data.stand_height) + "cm"
                        color: "black"
                        anchors.horizontalCenter: parent.horizontalCenter // 부모의 수평 중앙에 정렬
                        anchors.top: deskHeight3.bottom
                        font.pointSize: 17
                        font.family: "Pretendard Light"
                    }
                }

                Image { // 저장된 데이터가 없을 때 표시할 기본 이미지
                    source: "img/plus-white.png"
                    width: 100
                    height: 100
                    visible: rect3Data === null
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (rect3Data === null){
                            deskStandData.addData(3)
                            stackView.replace("deskStandStore.qml")
                        } else {
                            //불러온 데이터로 책상 조절하는 함수
                            servoController.save_desk(rect3Data.desk_height)
                            servoController.save_stand(rect3Data.stand_height)
                            servoController.stop()
                            stackView.replace("mainPage.qml")
                        }
                    }
                }
            }

            Row { // 데이터를 수정, 삭제 할 수 있는 버튼
                id: row3
                anchors.top: rect3.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: rect3.horizontalCenter
                spacing: 20
                visible: rect3Data !== null

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#A2D2FF"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("덮어쓰기")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.updateData(3)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }

                Rectangle{
                    width: 80
                    height:30
                    radius: 20
                    color: "#FFC8DD"
                    border.color: "#FFFFFF"

                    Text {
                        text: qsTr("삭제")
                        font.pointSize: 11
                        font.family: "Pretendard Medium"
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            deskStandData.deleteData(3)
                            stackView.replace("deskStandStore.qml")
                        }
                    }
                }
            }
        }
    }

    //json 데이터를 문자열로 변환
    function getStringData(data, index) {
        if (data[index] !== null && data[index] !== undefined) {
            return JSON.stringify(data[index]);
        }
        return "No data";
    }
}
