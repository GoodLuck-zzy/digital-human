import asyncio
import websockets


async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/chat"

    async with websockets.connect(uri) as websocket:
        # 接收服务端欢迎消息
        msg = await websocket.recv()
        print("server:", msg)

        # 发送消息
        await websocket.send("hello fastapi websocket")
        print("client: hello fastapi websocket")

        # 接收服务端回显
        reply = await websocket.recv()
        print("server:", reply)


if __name__ == "__main__":
    asyncio.run(test_ws())

