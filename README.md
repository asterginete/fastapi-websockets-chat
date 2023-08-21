# Chat Application with FastAPI and WebSockets

This is a basic chat application built using FastAPI and WebSockets.

## Project Structure

```
python-fastapi-websockets-chat/
│
├── app/
│   ├── main.py               # Main application file
│   └── core/
│       └── connection.py     # Connection manager for WebSocket
│
├── tests/                    # Directory for test cases
│
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Setup

### 1. Install Dependencies

Ensure you have `pipenv` installed. If not, install it using:

```bash
pip install pipenv
```

Navigate to the project directory and install the required packages:

```bash
pipenv install
```

This will install all the dependencies listed in the `Pipfile`.

### 2. Activate the Virtual Environment

Activate the `pipenv` virtual environment:

```bash
pipenv shell
```

### 3. Run the Application

With the virtual environment activated, run the application using:

```bash
uvicorn app.main:app --reload
```

## Code Overview

### `app/main.py`

```python
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
```

### `app/core/connection.py`

```python
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```

## Future Enhancements

- Add authentication and authorization.
- Implement persistence to save chat messages to a database.
- Introduce private messaging and group chats.
- Handle different message types (e.g., images, files).
- Implement rate limiting and other security measures.
