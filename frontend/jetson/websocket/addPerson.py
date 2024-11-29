import argparse
import asyncio
import websockets
import cv2
import time
import base64
import os

# 비디오 캡처 초기화 함수
def get_video_device_number():
    video_devices = [int(f[-1]) for f in os.listdir('/dev') if f.startswith('video')]
    if not video_devices:
        print("No video devices found.")
        exit()
    return min(video_devices)


async def send_message(message, user_id, server_uri):
    async with websockets.connect(server_uri) as websocket:
#        print("서버에 연결되었습니다.")

        # 메시지 전송 (addFace)
        await websocket.send(message)
 #       print(f"메시지 {message}가 성공적으로 전송되었습니다.")

        await websocket.send(user_id)
        print(f"유저id {user_id}가 성공적으로 전송되었습니다.")

        # 이미지 캡처 및 전송
        video_device_number = get_video_device_number()  # 첫 번째 비디오 장치 번호 가져오기
        cap = cv2.VideoCapture(video_device_number)
        
        for i in range(5):
            ret, frame = cap.read()
            if not ret:
    #            print("캡처 실패")
                continue

            # 이미지 jpg로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')

            # 이미지 전송
            await websocket.send(image_data)

            await asyncio.sleep(0.1)
        
        cap.release()
     #   print("이미지 전송 완료")

        while True:
      #      print("waiting")
            message = await websocket.recv()
            print(f"{message}")
            break



def main(user_id):
    server_uri = 'ws://70.12.130.101:8765'
    message = 'addFace'
    user_id = user_id

    asyncio.run(send_message(message, user_id, server_uri))

if __name__ == "__main__":
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--_id', required=True)
#    args = parser.parse_args()

#    user_id = args._id
    user_id = "qewrqwer"
    main(user_id)

# import argparse
# import asyncio
# import websockets

# async def send_message(message, image_path, server_uri):
#     async with websockets.connect(server_uri) as websocket:
#         print("서버에 연결되었습니다.")

#         await websocket.send(message)
#         print(f"메시지 {message}가 성공적으로 전송되었습니다.")

#         # 이미지 파일 열기 및 전송
#         with open(image_path, 'rb') as f:
#             while (chunk := f.read(1024)):
#                 await websocket.send(chunk)

#         print("이미지가 성공적으로 전송되었습니다.")

# def main(user_id, image_path):
#     server_uri = 'ws://70.12.130.101:8887'
#     message = 'addFace'

#     asyncio.run(send_message(message, image_path, server_uri))

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--_id', required=True)
#     args = parser.parse_args()

#     user_id = args._id
#     main(user_id)
