import os
import shutil
import asyncio
import websockets

def send_image(directory, server_uri, deleteConfirm=True):
    # async with websockets.connect(server_uri) as websocket:
    #     print("서버에 연결되었습니다.")

        # 이미지 파일 열기 및 전송
        for filename in os.listdir(directory):
            filePath = os.path.join(directory, filename)
            print(filePath)
            # with open(filePath, 'rb') as f:
            #     while (chunk := f.read(1024)):
            #         await websocket.send(chunk)
        if deleteConfirm:
            shutil.rmtree(directory)




def socket_send_image(directory, serverUri, deleteConfirm=True):
    asyncio.run(send_image(directory, serverUri))    