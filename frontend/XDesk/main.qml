import QtQuick
import QtQuick.Window
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 1024
    height: 600
    title: "Multi-Page QML Example"

    // 전체화면
    // flags:Qt.Window | Qt.FramelessWindowHint
    // visibility: Window.FullScreen

    // // 키 이벤트를 받을 요소
    // Rectangle {
    //     id: focusItem
    //     width: parent.width
    //     height: parent.height
    //     color: "transparent" // 배경이 투명하게 설정
    //     focus: true // focus 속성 설정

    //     Component.onCompleted: {
    //         focusItem.forceActiveFocus();
    //         focusItem.grabKeyboard(); // 키보드 입력을 항상 잡아둠
    //     }

    //     Keys.onPressed: {
    //         if (event.key === Qt.Key_Escape) {
    //             // console.log("Running Python script before exit...")
    //             event.accepted = true;
    //             Qt.quit(); // 애플리케이션 종료
    //         }
    //     }
    // }

    StackView {
        id: stackView
        initialItem: FirstPage {}
        anchors.fill: parent

        // 빈 Transition 설정
        pushEnter: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 1
                    to:1
                    duration: 200
                }
            }

        pushExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:1
                duration: 200
            }
        }

        popEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:1
                duration: 200
            }
        }

        popExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:1
                duration: 200
            }
        }

        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to: 1
                duration: 200
            }
        }

        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to: 1
                duration: 200
            }
        }

        function popToInitial() {
            while (stackView.depth > 1) {
                stackView.pop()
            }
        }
    }

    function goToDeskStandAdjustPage() {
        stackView.push("deskStandAdjust.qml")
    }

    function goToFaceIdSignUpPage(){
        stackView.push("askRecogFaceId.qml")
    }

    Component.onCompleted: {
        modalHandler.setStackView(stackView)
    }

    // onClosing: {
    //     // 애플리케이션 종료 전에 서보모터를 작동하는 스크립트 실행
    //     //runServoMotorScript()
    //     // console.log("Running Python script before exit...")
    // }

    // function runPythonScript() {
    //     console.log("Running Python script before exit...")
    //     var process = Qt.createQmlObject('import QtQuick 2.0; QtObject { id: scriptRunner }', stackView);
    //     process.start("python3", ["/home/pi/qtest/total/XDesk/servo_reset.py"]); // 스크립트 경로
    // }
}
