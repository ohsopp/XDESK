import os
import asyncio
import shutil
import websockets

async def send_image(directory, serverUri, deleteConfirm=True):
    async with websockets.connect(serverUri) as websocket:
        print("서버에 연결되었습니다.")

        # 이미지 파일 열기 및 전송
        for filename in os.listdir(directory):
            filePath = os.path.join(directory, filename)
            with open(filePath, 'rb') as f:
                while (chunk := f.read(1024)):
                    await websocket.send(chunk)
        if deleteConfirm:
            shutil.rmtree(directory)

async def send_command(command, serverUri):
    async with websockets.connect(server_Uri) as websocket:
        # 명령 보내기
        await websocket.send(command)
        print(f"Sent command: {command}")

        # 서버로부터 응답 받기
        response = await websocket.recv()
        print(f"Received response: {response}")


def socket_send_image(directory, serverUri, deleteConfirm=True):
    asyncio.run(send_image(directory, serverUri))        


def socket_send_command(command, server_uri):
    asyncio.run(send_command(command, server_uri))

    # ws://70.12.130.101:8888