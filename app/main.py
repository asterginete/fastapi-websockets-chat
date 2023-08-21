from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.core.connection import ConnectionManager

app = FastAPI()
connection_manager = ConnectionManager()

@app.websocket("/ws/{username}/")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"{username} left the chat")
