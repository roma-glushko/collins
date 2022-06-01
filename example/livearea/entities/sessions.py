from uuid import uuid4

from pydantic import BaseModel, Field
from fastapi import WebSocket

from livearea.protocol.events import Message

SessionId = str


class Session(BaseModel):
    id: SessionId = Field(default_factory=lambda: str(uuid4()))
    connection: WebSocket

    class Config:
        arbitrary_types_allowed = True

    async def send_message(self, message: Message) -> None:
        await self.connection.send_json(message.dict())