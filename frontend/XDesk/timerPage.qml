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

    property int timeInSeconds: 0 // 사용자가 지정 할 시간
    property int totalTime: 0 // 전체 시간 저장
    property int dragStartValue: 0 // 드래그 시작시 초기 값
    property int dragStartY: 0 //드래그 시작시 초기 마우스 위치

    // 시 텍스트
    Text {
        id: textH
        text: "시간"
        font.pixelSize: 60
        font.family: "Pretendard Medium"
        anchors.top : parent.top
        anchors.topMargin: 80
        anchors.bottom: rectH.top
        anchors.horizontalCenter: rectH.horizontalCenter
    }

    // 분 텍스트
    Text {
        id: textM
        text: "분"
        font.pixelSize: 60
        font.family: "Pretendard Medium"
        anchors.top : parent.top
        anchors.topMargin: 80
        anchors.bottom: rectM.top
        anchors.horizontalCenter: rectM.horizontalCenter
    }

    // 초 텍스트
    Text {
        text: "초"
        font.pixelSize: 60
        font.family: "Pretendard Medium"
        anchors.top : parent.top
        anchors.topMargin: 80
        anchors.bottom: rectS.top
        anchors.horizontalCenter: rectS.horizontalCenter
    }

    // 시간 숫자 설정 (시)
    Rectangle {
        id: rectH
        width: 120
        height: 400
        color: "transparent"
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.verticalCenter: parent.verticalCenter

        Text {
            id: hoursDisplay
            text: Math.floor(timeInSeconds / 3600).toString().padStart(2, '0') //HH 형식 출력
            font.pixelSize: 90
            font.family: "Pretendard Medium"
            anchors.centerIn: parent
        }

        // 시간 드래그 조정 (시)
        MouseArea {
            id: hoursArea
            anchors.fill: parent

            onPressed: {
                dragStartValue = timeInSeconds // 드래그 시작 시 시간 값을 저장
                dragStartY = mouse.y // 드래그 시작 시 Y 좌표를 저장
            }

            onPositionChanged: {
                let deltaY = mouse.y - dragStartY // 드래그된 거리 계산
                adjustTime("hours", -Math.round(deltaY / 10)) // 드래그된 거리만큼 시간 조정
                dragStartY = mouse.y // 새로운 Y 좌표를 드래그 시작 Y 좌표로 업데이트
            }
        }
    }

    // 첫번째 콜론(:)
    Rectangle {
        id: colonRect1
        width:30
        height: 400
        color: "transparent"
        anchors.left: rectH.right
        anchors.verticalCenter: rectH.verticalCenter

        Text {
            text: qsTr(":")
            font.pixelSize: 90
            font.family: "Pretendard Medium"
            anchors.centerIn: parent
        }
    }

    // 시간 숫자 설정 (분)
    Rectangle {
        id: rectM
        width: 120
        height: 400
        color: "transparent"
        anchors.left: colonRect1.right
        anchors.verticalCenter: colonRect1.verticalCenter

        Text {
            id: minutesDisplay
            text: Math.floor((timeInSeconds % 3600) / 60).toString().padStart(2, '0') //MM 형식 출력
            font.pixelSize: 90
            font.family: "Pretendard Medium"
            anchors.centerIn: parent
        }

        // 분 드래그 조정
        MouseArea {
            id: minutesArea
            anchors.fill: parent

            onPressed: {
                dragStartValue = timeInSeconds // 드래그 시작 시 시간 값을 저장
                dragStartY = mouse.y // 드래그 시작 시 Y 좌표를 저장
            }

            onPositionChanged: {
                let deltaY = mouse.y - dragStartY // 드래그된 거리 계산
                adjustTime("minutes", -Math.round(deltaY / 10)) // 드래그된 거리만큼 분 조정
                dragStartY = mouse.y // 새로운 Y 좌표를 드래그 시작 Y 좌표로 업데이트
            }
        }
    }

    // 두번째 콜론(:)
    Rectangle {
        id: colonRect2
        width:30
        height: 400
        color: "transparent"
        anchors.left: rectM.right
        anchors.verticalCenter: rectM.verticalCenter

        Text {
            text: qsTr(":")
            font.pixelSize: 90
            font.family: "Pretendard Medium"
            anchors.centerIn: parent
        }
    }

    // 시간 숫자 설정 (초)
    Rectangle {
        id: rectS
        width: 120
        height: 400
        color: "transparent"
        anchors.left: colonRect2.right
        anchors.verticalCenter: colonRect2.verticalCenter

        Text {
            id: secondsDisplay
            text: (timeInSeconds % 60).toString().padStart(2, '0')
            font.pixelSize: 90
            font.family: "Pretendard Medium"
            anchors.centerIn: parent
        }

        MouseArea {
            id: secondsArea
            anchors.fill: parent

            onPressed: {
                dragStartValue = timeInSeconds // 드래그 시작 시 시간 값을 저장
                dragStartY = mouse.y // 드래그 시작 시 Y 좌표를 저장
            }

            onPositionChanged: {
                let deltaY = mouse.y - dragStartY // 드래그된 거리 계산
                adjustTime("seconds", -Math.round(deltaY / 10)) // 드래그된 거리만큼 초 조정
                dragStartY = mouse.y // 새로운 Y 좌표를 드래그 시작 Y 좌표로 업데이트
            }
        }
    }


    // 위쪽 시간 텍스트 설정 (시)
    Text {
        id: upTextH
        text: ((parseInt(hoursDisplay.text) - 1 + 24) % 24).toString().padStart(2, '0') //시에서 1뺀 숫자
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.top : rectH.top
        anchors.topMargin: 50
        anchors.horizontalCenter: rectH.horizontalCenter
    }

    // 위쪽 시간 텍스트 설정 (분)
    Text {
        id: upTextM
        text: ((parseInt(minutesDisplay.text) - 1 + 60) % 60).toString().padStart(2, '0') //분에서 1뺀 숫자
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.top : rectM.top
        anchors.topMargin: 50
        anchors.horizontalCenter: rectM.horizontalCenter
    }

    // 위쪽 시간 텍스트 설정 (초)
    Text {
        id: upTextS
        text: ((parseInt(secondsDisplay.text) - 1 + 60) % 60).toString().padStart(2, '0') //초에서 1뺀 숫자
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.top : rectS.top
        anchors.topMargin: 50
        anchors.horizontalCenter: rectS.horizontalCenter
    }

    // 아래쪽 시간 텍스트 설정 (시)
    Text {
        id: downTextH
        text: ((parseInt(hoursDisplay.text) + 1) % 24).toString().padStart(2, '0')
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.bottom : rectH.bottom
        anchors.bottomMargin: 50
        anchors.horizontalCenter: rectH.horizontalCenter
    }

    // 아래쪽 시간 텍스트 설정 (분)
    Text {
        id: downTextM
        text: ((parseInt(minutesDisplay.text) + 1) % 60).toString().padStart(2, '0')
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.bottom : rectM.bottom
        anchors.bottomMargin: 50
        anchors.horizontalCenter: rectM.horizontalCenter
    }

    // 아래쪽 시간 텍스트 설정 (초)
    Text {
        id: downTextS
        text: ((parseInt(secondsDisplay.text) + 1) % 60).toString().padStart(2, '0')
        font.pixelSize: 90
        font.family: "Pretendard ExtraLight"
        color: "#797979"
        anchors.bottom : rectS.bottom
        anchors.bottomMargin: 50
        anchors.horizontalCenter: rectS.horizontalCenter
    }

    // 시작 버튼
    Button {
        id: startButton
        width: 480
        height: 80
        text: "시작"
        background: Rectangle {
            color: "#A2D2FF"
            radius: 50
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        font.family: "Pretendard Medium"
        font.pointSize: 35
        anchors.horizontalCenter: rectM.horizontalCenter

        onClicked: {
            //비활성화 버튼
            startButton.visible = false
            rect1M.visible = false
            rect5M.visible = false
            rect10M.visible = false
            rect30M.visible = false
            upTextH.visible = false
            upTextM.visible = false
            upTextS.visible = false
            downTextH.visible = false
            downTextM.visible = false
            downTextS.visible = false

            //활성화 버튼
            pauseButton.visible = true
            resetButton.visible = true

            //타이머 실행
            timer.running = true

            totalTime = timeInSeconds // 전체 시간 저장
            canvas.visible = true // 그래프 활성화
        }
    }

    // 중지 버튼
    Button {
        id: pauseButton
        width: 480
        height: 80
        text: "중지"
        background: Rectangle {
            color: "#A2D2FF"
            radius: 50
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        font.family: "Pretendard Medium"
        font.pointSize: 35
        anchors.horizontalCenter: rectM.horizontalCenter
        visible: false

        onClicked: {
            // 비활성화
            pauseButton.visible = false
            timer.running = false

            // 활성화
            reStartButton.visible = true
        }
    }

    // 재시작 버튼
    Button {
        id: reStartButton
        width: 480
        height: 80
        text: "재시작"
        background: Rectangle {
            color: "#A2D2FF"
            radius: 50
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        font.family: "Pretendard Medium"
        font.pointSize: 35
        anchors.horizontalCenter: rectM.horizontalCenter
        visible: false

        onClicked: {
            //비활성화
            reStartButton.visible = false

            //활성화
            pauseButton.visible = true
            timer.running = true
        }
    }

    // 초기화 버튼
    Button {
        id: resetButton
        width: 480
        height: 80
        text: "초기화"
        background: Rectangle {
            color: "#FFC8DD"
            radius: 50
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50
        font.family: "Pretendard Medium"
        font.pointSize: 35
        anchors.left: reStartButton.right
        anchors.leftMargin: 20
        visible: false

        onClicked: {
            //타이머 정지 및 초기화
            timer.stop()
            timeInSeconds = 0

            // 버튼 비활성화
            pauseButton.visible = false
            reStartButton.visible = false
            resetButton.visible = false

            //버튼 활성화
            startButton.visible = true
            rect1M.visible = true
            rect5M.visible = true
            rect10M.visible = true
            rect30M.visible = true
            upTextH.visible = true
            upTextM.visible = true
            upTextS.visible = true
            downTextH.visible = true
            downTextM.visible = true
            downTextS.visible = true

            canvas.requestPaint() // 원형 그래프 초기화
            canvas.visible = false // 그래프 비활성화
        }
    }


    // 5분 버튼(마진 기준)
    Button {
        id: rect5M
        width: 200
        height: 200
        text: "5분"
        font.family: "Pretendard Medium"
        font.pointSize: 40
        background: Rectangle {
            color: "#A498F1"
            radius: 100
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.right: parent.right
        anchors.rightMargin: 40
        anchors.top: parent.top
        anchors.topMargin: 80

        onClicked: {
            timeInSeconds += 300
        }
    }

    // 1분 버튼
    Button {
        id: rect1M
        width: 200
        height: 200
        text: "1분"
        font.family: "Pretendard Medium"
        font.pointSize: 40
        background: Rectangle {
            color: "#A498F1"
            radius: 100
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.right: rect5M.left
        anchors.rightMargin: 40
        anchors.verticalCenter: rect5M.verticalCenter

        onClicked: {
            timeInSeconds += 60
        }
    }

    // 10분 버튼
    Button {
        id: rect10M
        width: 200
        height: 200
        text: "10분"
        font.family: "Pretendard Medium"
        font.pointSize: 40
        background: Rectangle {
            color: "#A498F1"
            radius: 100
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.top: rect1M.bottom
        anchors.topMargin: 40
        anchors.horizontalCenter: rect1M.horizontalCenter

        onClicked: {
            timeInSeconds += 600
        }
    }

    // 30분 버튼
    Button {
        id: rect30M
        width: 200
        height: 200
        text: "30분"
        font.family: "Pretendard Medium"
        font.pointSize: 40
        background: Rectangle {
            color: "#A498F1"
            radius: 100
            border.color: "#ffffff"
            border.width: 5
        }
        anchors.top: rect5M.bottom
        anchors.topMargin: 40
        anchors.horizontalCenter: rect5M.horizontalCenter

        onClicked: {
            timeInSeconds += 1800
        }
    }

    Timer {
        id: timer
        interval: 1000 // 1초 간격
        repeat: true
        running: false // 처음에 실행되지 않도록
        onTriggered: {
            if (timeInSeconds > 0) {
                timeInSeconds -= 1  // 타이머가 트리거될 때마다 1초 감소
                canvas.requestPaint() // 원형 그래프 업데이트 요청
            } else {
                timer.stop() // 시간이 0이 되면 타이머를 멈춤
                timeoutDialog.open() // 모달을 띄움
            }
        }
    }

    // 원형 그래프 캔버스
    Canvas {
        id: canvas
        width: 400
        height: 400
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.top: parent.top
        anchors.topMargin: 50
        visible: false

        property real animatedRatio: 0.0 //애니메이션의 진행 정도(0 -> targetRatio 까지 변경)
        property Image image: img // 이미지 객체 참조

        Image {
            id: img
            source: "img/alarm.png" // 이미지 경로 설정
            visible: false // 화면에는 보이지 않게 설정
        }

        onPaint: { //캔버스가 다시 그려질 때마다 호출
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height) //캔버스 초기화

            // 전체 시간 대비 남은 시간의 비율 계산
            var targetRatio = timeInSeconds / totalTime
            var endAngle = -Math.PI / 2 + animatedRatio * 2 * Math.PI //원의 종료 각도

            // 남은 시간 도넛 그리기
            ctx.beginPath()
            ctx.lineWidth = 10
            ctx.lineCap = "round" // 모서리를 둥글게 설정
            ctx.arc(width / 2, height / 2, 170, -Math.PI / 2, endAngle, false) //도넛차트의 형태(arc)
            ctx.strokeStyle = "#80FFFFFF"
            ctx.stroke()

            // 이미지 그리기
            var imgWidth = 200; // 조절된 너비
            var imgHeight = 200; // 조절된 높이
            var imgX = (width - imgWidth) / 2
            var imgY = (height - imgHeight) / 2
            ctx.drawImage(img, imgX, imgY, imgWidth, imgHeight) // 크기를 지정하여 이미지 그리기

            // 애니메이션 업데이트
            if (Math.abs(animatedRatio - targetRatio) > 0.005) {
                animatedRatio += (targetRatio - animatedRatio) * 0.02
                requestAnimationFrame(canvas.requestPaint.bind(canvas))
            } else {
                animatedRatio = targetRatio
            }
        }

        Component.onCompleted: { // canvas 객체가 완성된 후 호출
            requestAnimationFrame(canvas.requestPaint.bind(canvas))
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
                stackView.pop()
            }
        }
    }




    // 드래그에 따라 시간 조정하는 함수
    function adjustTime(component, delta) {
        let hours = Math.floor(timeInSeconds / 3600) % 24
        let minutes = Math.floor((timeInSeconds % 3600) / 60) % 60
        let secs = timeInSeconds % 60

        if (component === "hours") {
            hours = (hours + delta + 24) % 24 // 시간 변경 (0-23 범위)
        } else if (component === "minutes") {
            minutes = (minutes + delta + 60) % 60 // 분 변경 (0-59 범위)
        } else if (component === "seconds") {
            secs = (secs + delta + 60) % 60 // 초 변경 (0-59 범위)
        }

        timeInSeconds = hours * 3600 + minutes * 60 + secs
    }

    // 타이머 종료 모달
    Dialog {
        id: timeoutDialog
        width: 400
        height: 200
        title: "타이머 종료"
        standardButtons: Dialog.Ok
        background: Rectangle {
            color: "#A498F1"  // 배경색 설정
            radius: 10        // 둥근 모서리 설정
            border.color: "#ffffff"
            border.width: 2
        }

        contentItem: Text {
            text: "타이머가 종료되었습니다."
            font.pixelSize: 20
            anchors.centerIn: parent
        }

        anchors.centerIn: parent
    }
}
