from PySide6.QtCore import QObject, Slot, Signal
import requests
import traceback
from userData import UserData
import base64
import os 

class LogoutHandler(QObject):

    LogoutDataReceived = Signal(str)
    def __init__(self, userData: UserData):
        super().__init__()
        self.userData = userData

    @Slot()
    def getData(self):
        jwt_token =  self.userData.get_jwt_token()
        if not jwt_token:
            print("JWT token is not set.")
            return

        url = 'https://i11a102.p.ssafy.io/api/v2/logout'

        # 오늘 자세 비율 보낼 곳 (수정필요)
        posture_percentage = 45  
        payload = {
        "posture_percentage": posture_percentage
        }
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        self.userData.delete_graph_data()
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  
            
            # 오늘의 그래프 만들 곳(수정필요)
            nodata_path = os.path.join(os.path.dirname(__file__), 'nodata.png')
            with open(nodata_path, 'rb') as image_file:
                today_image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

            self.LogoutDataReceived.emit(today_image_base64)

        except requests.RequestException as e:
            print("Exception occurred:", str(e))
            traceback.print_exc()
   