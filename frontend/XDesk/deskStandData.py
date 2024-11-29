from PySide6.QtCore import QObject, Slot, Signal, Property
import requests
import traceback
from userData import UserData

class DeskStandData(QObject):

    deskStandDataReceived = Signal(dict)

    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData
        self._deskHeight = 73
        self._standHeight = 0

    @Property(int)
    def deskHeight(self):
        return self._deskHeight

    @deskHeight.setter
    def deskHeight(self, value):
        self._deskHeight = value

    @Property(int)
    def standHeight(self):
        return self._standHeight

    @standHeight.setter
    def standHeight(self, value):
        self._standHeight = value

    @Slot(int)
    def addData(self, desk_index):
        jwt_token = self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = f'https://i11a102.p.ssafy.io/api/v1/xdesk/add/{desk_index}'
        data = {
            "desk_height": self._deskHeight,
            "stand_height": self._standHeight
        }
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # 요청이 성공적으로 완료되지 않으면 예외 발생
            print("Data received:", response.json())
        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()

    @Slot()
    def getData(self):
        jwt_token = self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = f'https://i11a102.p.ssafy.io/api/v1/xdesk/index'

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 요청이 성공적으로 완료되지 않으면 예외 발생
            print("Data received:", response.json())
            data = response.json()
            self.deskStandDataReceived.emit(data)
        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()

    @Slot(int)
    def updateData(self, desk_index):
        jwt_token = self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = f'https://i11a102.p.ssafy.io/api/v1/xdesk/update/{desk_index}'
        data = {
            # 현재 책상 높이 받아오기
            "desk_height": self._deskHeight,
            "stand_height": self._standHeight
        }
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # 요청이 성공적으로 완료되지 않으면 예외 발생
            print("Data received:", response.json())
        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()

    @Slot(int)
    def deleteData(self, desk_index):
        jwt_token = self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = f'https://i11a102.p.ssafy.io/api/v1/xdesk/delete/{desk_index}'

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()  # 요청이 성공적으로 완료되지 않으면 예외 발생
            print("Data received:", response.json())
        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()
