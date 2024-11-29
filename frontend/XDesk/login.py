from PySide6.QtCore import QUrl, Signal, Slot, QObject
from PySide6.QtWebEngineWidgets import QWebEngineView
import json, requests
from userData import UserData

webView = None

class FaceLogin(QObject):
    faceLoginSucces =Signal()

    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData
        self.jwt_token = None
        self.user_info = None

class NaverLogin(QObject):
    naverLoginSuccess = Signal()

    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData
        self.jwt_token = None
        self.user_info = None

    @Slot()
    def openNaverLoginWindow(self):
        global webView
        login_url = 'https://i11a102.p.ssafy.io/api/v1/oauth/naver/login/'
        # login_url = 'http://localhost/api/v1/oauth/naver/login/'
        # 기존 창이 열려 있으면 닫기
        if webView is not None and webView.isVisible():
            webView.close()

        # 새로운 QWebEngineView 생성 및 설정
        webView = QWebEngineView()
        webView.setWindowTitle('Naver Login')
        webView.resize(1024, 600)

        webView.loadFinished.connect(self.onLoadFinished)

        webView.setUrl(QUrl(login_url))
        webView.show()

    # 로그인 성공시 데이터 가져오기
    def onLoadFinished(self, finished):
        global webView
        current_url = webView.url().toString()
        if 'https://i11a102.p.ssafy.io/api/v1/oauth/naver/login/callback' in current_url:
        # if 'http://localhost/api/v1/oauth/naver/login/callback' in current_url:
            webView.page().toPlainText(self.handlePageContent)

    @Slot(str)
    def handlePageContent(self, content):
        global webView
        try:
            data = json.loads(content)
            self.jwt_token = data.get("jwt_token")

            response = data.get("response", {}).get("body", "{}")
            self.user_info = json.loads(response)

            #지울 코드
            print("self.user_info: ",  self.user_info)

            # JWT 토큰 저장
            self.userData.set_jwt_token(self.jwt_token)


            self.naverLoginSuccess.emit()

            #창 닫기
            webView.close()

        except json.JSONDecodeError:
            print("Failed to decode JSON from message")


class KakaoLogin(QObject):
    kakaoLoginSuccess = Signal()

    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData
        self.jwt_token = None
        self.user_info = None

    @Slot()
    def openKakaoLoginWindow(self):
        global webView
        login_url = 'https://i11a102.p.ssafy.io/api/v1/oauth/kakao/login/'

        # 기존 창이 열려 있으면 닫기
        if webView is not None and webView.isVisible():
            webView.close()

        # 새로운 QWebEngineView 생성 및 설정
        webView = QWebEngineView()
        webView.setWindowTitle('Kakao Login')
        webView.resize(1024, 600)

        webView.loadFinished.connect(self.onLoadFinished)

        webView.setUrl(QUrl(login_url))
        webView.show()

    def onLoadFinished(self, finished):
        global webView
        current_url = webView.url().toString()
        if 'https://i11a102.p.ssafy.io/api/v1/oauth/kakao/login/callback' in current_url:
            webView.page().toPlainText(self.handlePageContent)

    @Slot(str)
    def handlePageContent(self, content):
        global webView
        try:
            data = json.loads(content)
            self.jwt_token = data.get("jwt_token")

            response = data.get("response", {}).get("body", "{}")
            self.user_info = json.loads(response)

            #지울 코드
            print("self.user_info: ",  self.user_info)

            # JWT 토큰 저장
            self.userData.set_jwt_token(self.jwt_token)


            self.kakaoLoginSuccess.emit()

            #창 닫기
            webView.close()

        except json.JSONDecodeError:
            print("Failed to decode JSON from message")
