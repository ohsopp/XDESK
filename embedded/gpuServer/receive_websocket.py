

import os
import asyncio
import websockets

recognize = 100
add = 200

async def receive_image(websocket, path):
    print("클라이언트와 연결되었습니다.")

    # 이미지 데이터를 수신하고 파일로 저장
    with open('received_image.jpg', 'wb') as f:
        while True:
            try:
                data = await websocket.recv()
                if not data:
                    break
                f.write(data)
            except websockets.ConnectionClosed:
                print("클라이언트 연결이 종료되었습니다.")
                break
        
    print("이미지가 'received_image.jpg'로 저장되었습니다.")

async def receive_data(websocket, path):
    mode = await websocket.recv()
    print("receive message")

    if(mode == recognize):
        
    elif(mode==add):
        

    imagesID = ""
    imageFiles = []
    while True:
        try:
            image_data = 




async def start_server():
    # 서버를 모든 네트워크 인터페이스의 포트 8888에서 실행
    async with websockets.serve(receive_data, "70.12.130.101", 8888):
        await asyncio.Future()  # 서버를 계속 실행

if __name__ == "__main__":
    asyncio.run(start_server())
