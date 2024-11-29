from PySide6.QtCore import QObject, Slot, Signal
import requests
import traceback
from userData import UserData
import base64


class GraphHandler(QObject):
    
    GraphDataReceived = Signal(str)
    
    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData

    @Slot()
    def getData(self):
        # 캐시된 그래프 데이터가 있다면 바로 사용
        cached_data = self.userData.get_graph_data()
        if cached_data:
            self.GraphDataReceived.emit(cached_data)
            return

        jwt_token = self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = 'https://i11a102.p.ssafy.io/api/v2/graph'
        # url = 'http://localhost/api/v2/graph'

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # 요청이 성공적으로 완료되지 않으면 예외 발생
            
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            self.userData.set_graph_data(image_base64)
            self.GraphDataReceived.emit(image_base64)

        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()
