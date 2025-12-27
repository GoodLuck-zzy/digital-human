from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    await ws.send_text("WebSocket connected successfully")

    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"Server received: {msg}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")

