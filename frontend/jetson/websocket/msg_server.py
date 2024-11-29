import asyncio
import websockets

# 서버에서 호출될 함수 정의
def func1():
    print("hello1")

async def handle_message(websocket, message):
    if message == "func1":
        func1()  # func1 함수를 호출하여 "hello1" 출력
        response = "func1 executed"
    else:
        response = f"Echo: {message}"
    
    await websocket.send(response)

async def echo(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            await handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected")

# 웹소켓 서버 실행
start_server = websockets.serve(echo, "192.168.137.157", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://192.168.137.157:8765")
asyncio.get_event_loop().run_forever()

