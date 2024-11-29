# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtCore import QUrl, QMetaObject, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QFontDatabase

from login import NaverLogin, KakaoLogin, FaceLogin
from pyinterface import PyInterface
from deskStandData import DeskStandData
from manual import ServoController
from userData import UserData
from ModalHandler import ModalHandler

from logout import LogoutHandler
from monthGraph import GraphHandler

import subprocess
# from gpiozero import Button
import time


class SubprocessGraph(QThread):
    completed = Signal(int)  # 작업 완료 시그널

    def run(self):
        remote_command = ["ssh", "orin@192.168.137.196", "python3", "/home/orin/test/score_graph.py"]
        try:
            result = subprocess.run(remote_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #stdout = result.stdout.strip()
            #stderr = result.stderr.strip()
            #print("stdout:", stdout)
            #print("stderr:", stderr)

            # 성공 시 0 반환
            #self.completed.emit(0)

        except subprocess.CalledProcessError as error:
            print(f"Failed to run remote command: {error}")
            # 오류 발생 시 -1 반환
            #self.completed.emit(-1)

    @Slot()
    def create_logout_file(self):
        remote_command = ["ssh", "orin@192.168.137.196", "bash", "-c", "'echo \"User logged out.\" > /home/orin/test/logout_info.txt'"]

        try:
            result = subprocess.run(remote_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(f"File created on remote server at /home/orin/test/logout_info.txt")
            else:
                print(f"Failed to create file on remote server. stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run remote command: {e}")

        #self.quit() # QThread 종료
        #self.wait() # QThread가 완전히 종료될 때까지 대기


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()

        base_path = Path(__file__).resolve().parent

        # 폰트 로드
        fontDB = QFontDatabase()
        font_paths = [
            "/font/Pretendard-Black.otf",
            "/font/Pretendard-Bold.otf",
            "/font/Pretendard-ExtraBold.otf",
            "/font/PretendardVariable.ttf"
        ]
        for font_path in font_paths:
            fontDB.addApplicationFont(str(base_path) + font_path)

        '''
        fontDB = QFontDatabase()
        fontDB.addApplicationFont(str(base_path) + "/font/Pretendard-Black.otf")
        fontDB.addApplicationFont(str(base_path) + "/font/Pretendard-Bold.otf")
        fontDB.addApplicationFont(str(base_path) + "/font/Pretendard-ExtraBold.otf")
        fontDB.addApplicationFont(str(base_path) + "/font/PretendardVariable.ttf")
        '''

        # QML에 Python 객체를 노출
        context = engine.rootContext()

        # 인스턴스 생성
        userData = UserData()
        naverLogin = NaverLogin(userData)
        kakaoLogin = KakaoLogin(userData)
        faceLogin  = FaceLogin(userData)
        logout = LogoutHandler(userData)
        monthGraph = GraphHandler(userData)
        deskStandData = DeskStandData(userData)
        pyinterface = PyInterface(deskStandData)
        servo_controller = ServoController()
        handler = ModalHandler(engine, base_path, pyinterface)
        graph = SubprocessGraph()

        context.setContextProperty("naverLogin", naverLogin)
        context.setContextProperty("kakaoLogin", kakaoLogin)
        context.setContextProperty("faceLogin", faceLogin)
        context.setContextProperty("logout", logout)
        context.setContextProperty("monthGraph", monthGraph)
        context.setContextProperty("pyinterface", pyinterface)
        context.setContextProperty("deskStandData", deskStandData)
        context.setContextProperty("servoController", servo_controller)
        context.setContextProperty("modalHandler", handler)
        context.setContextProperty("graph", graph)

        '''def onSubprocessCompleted(root_object, result_code):
            if result_code == 0:
                if userData.get_user_info().motion_number is None:
                    root_object.goToFaceIdSignUpPage()
                else:
                    root_object.goToDeskStandAdjustPage()
            else:
                print("SubprocessGraph execution failed.")
        '''

        def handleLoginSuccess(): #소셜 로그인 성공
            root_object = engine.rootObjects()[0]

            # SubprocessGraph 인스턴스 생성 및 실행
            #graph.completed.connect(lambda result_code: onSubprocessCompleted(root_object, result_code))
            #print(userData.get_user_info())

            if userData.get_user_info().get('motion_number') == None:
                root_object.goToFaceIdSignUpPage()
            else:
                root_object.goToDeskStandAdjustPage()

        naverLogin.naverLoginSuccess.connect(handleLoginSuccess)
        kakaoLogin.kakaoLoginSuccess.connect(handleLoginSuccess)

        '''def on_button_pressed():
            QMetaObject.invokeMethod(handler, "show_modal", Qt.QueuedConnection)

        # 비상정지
        button = Button(22)
        button.when_pressed = on_button_pressed
        '''

        engine.load(QUrl.fromLocalFile(str(base_path / "main.qml")))

        if not engine.rootObjects():
            sys.exit(-1)
        sys.exit(app.exec())
    except Exception as e:
            print(f"An error occurred: {e}")

    # finally:
    #     # 종료 시 button 할당 해제
    #     try:
    #         if 'button' in locals() and button is not None:
    #             time.sleep(2)  # 잠시 대기
    #             button.close()
    #     except Exception as ex:
    #         print(f"Error while closing button: {ex}")
    #     print("Resources have been released.")
