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
    

async def send_message(message, anonymous, server_uri):
    async with websockets.connect(server_uri) as websocket:
        # 메시지 전송 (addFace)
        await websocket.send(message)

        await websocket.send(anonymous)

        # 이미지 캡처 및 전송
        video_device_number = get_video_device_number()  # 첫 번째 비디오 장치 번호 가져오기
        cap = cv2.VideoCapture(video_device_number)
        
        for i in range(5):
            ret, frame = cap.read()
            if not ret:
                continue

            # 이미지 jpg로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')

            # 이미지 전송
            await websocket.send(image_data)

            await asyncio.sleep(0.1)
        
        cap.release()

        while True:
            message = await websocket.recv()
            print(f"{message}")
            break


def main():
    server_uri = 'ws://70.12.130.101:8765'
    message = 'recognizeFace'
    anonymous = "user_id"
    asyncio.run(send_message(message, anonymous, server_uri))

if __name__ == "__main__":
    main()
