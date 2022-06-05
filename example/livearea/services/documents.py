import asyncio
import logging

from livearea.entities.documents import Document
from livearea.entities.sessions import Session
from livearea.protocol.events import Message
from livearea.repositories.documents import DocumentChannelRepository
from livearea.repositories.sessions import SessionRepository

logger = logging.getLogger(__name__)


class DocumentRoomService:
    def __init__(self, sessions: SessionRepository, document_rooms: DocumentChannelRepository) -> None:
        self.sessions: SessionRepository = sessions
        self.document_rooms: DocumentChannelRepository = document_rooms

    async def join(self, document: Document, session: Session) -> None:
        await session.connection.accept()

        await self.sessions.save(session)
        await self.document_rooms.register(document, session)

    async def leave(self, document: Document, session: Session) -> None:
        await self.document_rooms.unregister(document, session)
        await self.sessions.delete(session)

    async def broadcast(self, document: Document, message: Message) -> None:
        sessions: list[Session] = await self.document_rooms.get_by_document(document)

        for session in sessions:
            await session.connection.send_json(message.dict())


class SyncDocumentService:
    def __init__(self) -> None:
        self.is_closing: bool = False
        self.request_queue = asyncio.Queue()

    async def append(self, request) -> None:
        await self.request_queue.put(request)

    async def close(self) -> None:
        self.is_closing = True

    async def sync(self) -> None:
        while not self.is_closing:
            request = await self.request_queue.get()
            pass

