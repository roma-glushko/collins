import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()

        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        del self.active_connections[client_id]

    async def send_personal_message(self, client_id: str, message: str) -> None:
        websocket: WebSocket = self.active_connections[client_id]

        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for _, connection in self.active_connections.items():
            await connection.send_text(message)
