import asyncio
import websockets
import cv2
import base64
import time
import os

# 비디오 캡처 초기화 함수
def get_video_device_number():
    video_devices = [int(f[-1]) for f in os.listdir('/dev') if f.startswith('video')]
    if not video_devices:
        print("No video devices found.")
        exit()
    return min(video_devices)



async def send_video():
    uri = "ws://70.12.130.101:8765"
    message = "recognizeMotion"
    user_id ="motion"


    # 카메라 설정
    video_device_number = get_video_device_number()  # 첫 번째 비디오 장치 번호 가져오기
    cap = cv2.VideoCapture(video_device_number)
    cap.set(cv2.CAP_PROP_FPS, 60)

    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        await websocket.send(user_id)

        frame_count = 0
        while frame_count < 120:  # 120프레임 촬영
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break
            
            # 이미지를 JPEG로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')
            
            # 이미지 전송
            await websocket.send(image_data)
            frame_count += 1
            
            # 정확한 프레임 속도 유지
            elapsed_time = time.time() - start_time
            await asyncio.sleep(max(0, (1/30) - elapsed_time))

   #     print(f"Sent {frame_count} frames to the server.")
        cap.release()

        while True:
            pwd = await websocket.recv()
            print(f"{pwd}")
            break


# 웹소켓 클라이언트 실행
asyncio.get_event_loop().run_until_complete(send_video())

