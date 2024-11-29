import argparse
import asyncio
import websockets
import cv2
import time
import base64

async def send_message(message, user_id, server_uri):
    async with websockets.connect(server_uri) as websocket:
        print("서버에 연결되었습니다.")

        # 메시지 전송 (addFace)
        await websocket.send(message)
        print(f"메시지 {message}가 성공적으로 전송되었습니다.")

        await websocket.send(user_id)
        print(f"유저id {user_id}가 성공적으로 전송되었습니다.")

        # 이미지 캡처 및 전송
        cap = cv2.VideoCapture(0)
        for i in range(30):
            ret, frame = cap.read()
            if not ret:
                print("캡처 실패")
                continue

            # 이미지 jpg로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')

            # 이미지 전송
            await websocket.send(image_data)

            # await asyncio.sleep(0.1)
        
        # cap.release()
        print("이미지 전송 완료")
        
        # Used only for recognizeFace, recognizeMotion
        while True:
            print("waiting")
            message = await websocket.recv()
            print(f"{message}")
            break

        # 43번째 줄에 message를 "192.168.137.50:8765"로 전송
        async with websockets.connect("ws://192.168.137.50:8888") as new_websocket:
            await new_websocket.send(message)
            print(f"message {message}가 192.168.137.50:8765로 성공적으로 전송되었습니다.")

def main(user_id):
    server_uri = 'ws://70.12.130.101:8765'
    message = 'recognizeFace'

    asyncio.run(send_message(message, user_id, server_uri))

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--_id', required=True)
    # args = parser.parse_args()

    # user_id = args.id
    user_id = "dayun_test"
    main(user_id)
