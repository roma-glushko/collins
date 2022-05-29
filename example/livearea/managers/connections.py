import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)

DocumentId = str
ClientId = str

ConnectionMap = dict[ClientId, WebSocket]
DocumentRoomMap = dict[DocumentId, ConnectionMap]


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: DocumentRoomMap = {}
        self.connections: ConnectionMap = {}

    async def join(self, document_id: DocumentId, client_id: ClientId, websocket: WebSocket) -> None:
        await websocket.accept()

        connection_map: ConnectionMap = self.rooms.get(document_id, {})
        connection_map[client_id] = websocket

        self.rooms[document_id] = connection_map
        self.connections[client_id] = websocket

    async def leave(self, document_id: DocumentId, client_id: ClientId) -> None:
        connection_map: ConnectionMap = self.rooms.get(document_id, {})

        del connection_map[client_id]
        del self.connections[client_id]

        self.rooms[document_id] = connection_map

    async def send_message_to_client(self, client_id: str, message: str) -> None:
        websocket: WebSocket = self.connections[client_id]

        await websocket.send_text(message)

    async def broadcast(self, document_id: DocumentId, message: str) -> None:
        connection_map: ConnectionMap = self.rooms.get(document_id, {})

        for connection in connection_map.values():
            await connection.send_text(message)
