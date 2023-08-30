from typing import List, Dict
from fastapi import WebSocket
from app.models.user import User

class ConnectionManager:
    def __init__(self):
        # A dictionary to manage active connections. The key is the username, and the value is the WebSocket.
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user.username] = websocket

    def disconnect(self, user: User):
        if user.username in self.active_connections:
            del self.active_connections[user.username]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_private_message(self, sender: User, recipient_username: str, message: str):
        if recipient_username in self.active_connections:
            recipient_socket = self.active_connections[recipient_username]
            await recipient_socket.send_text(f"{sender.username}: {message}")

    async def send_group_message(self, sender: User, group: List[str], message: str):
        for username in group:
            if username in self.active_connections:
                recipient_socket = self.active_connections[username]
                await recipient_socket.send_text(f"[Group] {sender.username}: {message}")
