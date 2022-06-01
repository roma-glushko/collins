import logging
from typing import Optional, Iterator

from livearea.entities.documents import Document
from livearea.entities.documents import DocumentId
from livearea.entities.sessions import Session, SessionId
from livearea.repositories.sessions import SessionMap

logger = logging.getLogger(__name__)

DocumentRoomMap = dict[DocumentId, SessionMap]


class DocumentRoomRepository:
    def __init__(self, initial_rooms: Optional[DocumentRoomMap] = None) -> None:
        self._doc_rooms: DocumentRoomMap = initial_rooms or {}

    async def get_by_document(self, document: Document) -> list[Session]:
        return list(self._doc_rooms.get(document.id, {}).values())

    async def register(self, document: Document, session: Session) -> None:
        sessions: SessionMap = self._doc_rooms.get(document.id, {}) or {}

        sessions[session.id] = session
        self._doc_rooms[document.id] = sessions

    async def unregister(self, document: Document, session: Session) -> None:
        session_id: SessionId = session.id
        sessions: SessionMap = self._doc_rooms.get(document.id, {})

        del sessions[session_id]

        self._doc_rooms[document.id] = sessions


class DocumentRepository:
    def __init__(self, available_documents: Optional[dict[int, Document]] = None) -> None:
        self._documents = available_documents or {}

    def __len__(self) -> int:
        return len(self._documents)

    def __iter__(self) -> Iterator[Document]:
        return iter(self._documents.values())

    def __getitem__(self, document_id: int) -> Document:
        return self._documents[document_id]
