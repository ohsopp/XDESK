import os
import asyncio
import websockets
import nest_asyncio
import base64
import shutil
import sys
import numpy as np
import cv2
import model_execution



nest_asyncio.apply()

keyword = None

async def recognize_motion(websocket, user_id):
    global keyword
    #Save for AVI
    folder_path = "/home/j-i11a102/jeonghyeon/saved_video/motion.mp4"

    frame_count = 0
    video_frames = []
    
    if keyword == "recognizeMotion":
        print("Receiving video frames...")
        while True:
            try:
                # 이미지 데이터 수신
                image_data = await websocket.recv()
                
                # Base64로 인코딩된 데이터를 디코딩
                image_data = base64.b64decode(image_data)
                
                # 이미지 데이터를 numpy 배열로 변환
                np_arr = np.frombuffer(image_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    video_frames.append(frame)
                    frame_count += 1
    
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

    # 수신한 모든 프레임을 비디오 파일로 저장
        if video_frames:
            height, width, layers = video_frames[0].shape
            video = cv2.VideoWriter('received_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    
            for frame in video_frames:
                video.write(frame)
            
            video.release()
            print(f"Video saved as 'received_video.avi' with {frame_count} frames.")
        else:
            print("No frames received.")

        result = None
        result = model_execution.main()
        # 모션 결과 jetson으로 리턴
        try:
            await websocket.send(result)
            print(result)
        except websockets.ConnectionClosed:
            print("closed")

        # 이미지 수신 끝나면 키워드 초기화
        keyword = None

async def recognize_image(websocket, user_id):
    global keyword
    folder_path = 'recognize_image'

    
    if keyword == "recognizeFace":
        print("from jetson to gpu success ")

        if os.path.exists(folder_path):
            # 폴더 내의 모든 파일과 폴더를 가져와 삭제
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # 파일 또는 심볼릭 링크 삭제
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            print(f"기존 폴더 {folder_path}의 내용 삭제")
        else:
            print(f"{folder_path} 폴더가 존재하지 않습니다.")
        
        for i in range(30):
            try:
                image_data = await websocket.recv()
                if image_data:
                    decoded_data = base64.b64decode(image_data)
                    file_path = os.path.join(folder_path, f'{i}.jpg')
                    with open(file_path, 'wb') as f:
                        f.write(decoded_data)
                    print(f"이미지 {i} 머시깽이 저장")
                else:
                    print("수신된 이미지가 없어용 ㅜㅠㅠ")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

        #recognize_image
        # result = recognize_img.main()
        # result_id = ''
        # result_max = 0
        # for r in result:
        #     if r != 0:
        #         split_values = r.split(":")
        #         if float(split_values[1]) > result_max:
        #             result_max = float(split_values[1])
        #             result_id = split_values[0]
        resultId = "test"
        ##서버에게 메세지 보기기
        try:
            await websocket.send(resultId)
            print(resultId)
        except websockets.ConnextionClosed:
            print("closed")

        # 이미지 수신 끝나면 키워드 초기화
        keyword = None


async def add_face(websocket, user_id):
    global keyword
    folder_path = 'data/new_persons'

    if keyword == "addFace":
        print("from jetson to gpu success ")

        folder_path = f"datasets/new_persons/{user_id}"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"폴더 {folder_path}가 생성되었습니다.")
        else:
            print(f"폴더 {folder_path}가 이미 존재합니다.")
        
        for i in range(30):
            try:
                image_data = await websocket.recv()
                if image_data:
                    decoded_data = base64.b64decode(image_data)
                    file_path = os.path.join(folder_path, f'{i}.jpg')
                    with open(file_path, 'wb') as f:
                        f.write(decoded_data)
                    print(f"이미지 {i} 머시깽이 저장")
                else:
                    print("수신된 이미지가 없어용 ㅜㅠㅠ")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break


        #add image
        add_person.execute()
        keyword = None

        
async def receive_message(websocket, path):
    global keyword

    user_id = None
    
    while True:
        try:
            message = await websocket.recv()

            if keyword is None:
                if message in ["recognizeFace", "addFace", "recognizeMotion"]:
                    keyword = message
                    print("command received : ", keyword)
                    user_id = await websocket.recv()
                    print("user_id received : ", user_id)
                    if keyword == "recognizeFace":
                        await recognize_image(websocket, user_id)
                        print("recongnize_image")
                    elif keyword == "addFace":
                        await add_face(websocket, user_id)
                    elif keyword == "recognizeMotion":
                        await recognize_motion(websocket, user_id)
                else:
                    print("unknown command : ", message)
            else:
                if user_id is None:
                    print("user_id 수신 필요")
                    break
                # await receive_image(websocket, user_id)
        except websockets.ConnectionClosed:
            print("Connection closed")
            break
            
async def start_server():
    server = await websockets.serve(receive_message, "70.12.130.101", 8886)
    print("server started")
    return server

# async def main():
#     server = await start_server()
    
async def main():
    server = await start_server()
    
    if server:  # 서버가 None이 아닌지 확인
        print("Server is running...")

        try:
            # 서버가 계속 실행되도록 대기
            await asyncio.Future()  # 이 줄은 서버가 종료될 때까지 무한 대기 상태로 유지
        except KeyboardInterrupt:
            print("Server shutdown requested")
        finally:
            await server.close()
            await server.wait_closed()
            print("GPU server closed")

if __name__ == "__main__":
    asyncio.run(main())

