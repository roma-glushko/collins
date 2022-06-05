import logging

from livearea.entities.documents import Document
from livearea.entities.sessions import Session
from livearea.protocol.events import Message
from livearea.repositories.documents import DocumentRoomRepository
from livearea.repositories.sessions import SessionRepository, SessionMap

logger = logging.getLogger(__name__)


class DocumentRoomService:
    def __init__(self, sessions: SessionRepository, document_rooms: DocumentRoomRepository) -> None:
        self.sessions: SessionRepository = sessions
        self.document_rooms: DocumentRoomRepository = document_rooms

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
    pass
