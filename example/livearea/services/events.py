import json
import logging
from typing import Any

from fastapi import WebSocketDisconnect

from livearea.entities.documents import Document, LatestDocumentRevision
from livearea.entities.sessions import Session
from livearea.protocol.events import Message, EventTypes, DocumentOpenedData, DocumentLeftData, DocumentJoinedData, \
    CommitChangesData
from livearea.services.documents import DocumentRoomService

logger = logging.getLogger(__name__)


class EventService:
    def __init__(self, doc_room_service: DocumentRoomService) -> None:
        self.doc_room_service: DocumentRoomService = doc_room_service

    async def watch(self, document: Document, session: Session) -> None:
        await self._join_document(document, session)

        try:
            while True:
                data: dict[Any, Any] = await session.connection.receive_json()

                type: EventTypes = data.get("type")
                data: dict[str, Any] = data.get("data", {})

                logger.info(f"[{session.id}] {type}: {json.dumps(data)}")

                if type == EventTypes.COMMIT_CHANGES:
                    await self._commit_doc_changes(document, session, CommitChangesData(**data))

        except WebSocketDisconnect:
            await self._left_document(document, session)

    async def _join_document(self, document: Document, session: Session) -> None:
        await self.doc_room_service.broadcast(document, Message(
            type=EventTypes.DOCUMENT_JOINED.value,
            data=DocumentJoinedData(session_id=session.id),
        ))

        await self.doc_room_service.join(document, session)

        all_viewers: list[Session] = await self.doc_room_service.document_rooms.get_by_document(document)

        other_viewers: list[str] = [
            viewer.id
            for viewer in all_viewers
            if viewer.id != session.id
        ]

        await session.send_message(Message(
            type=EventTypes.DOCUMENT_OPENED.value,
            data=DocumentOpenedData(
                session_id=session.id,
                document=LatestDocumentRevision.from_doc(document),
                other_viewers=other_viewers,
            )
        ))

    async def _left_document(self, document: Document, session: Session) -> None:
        await self.doc_room_service.leave(document, session)

        await self.doc_room_service.broadcast(document, Message(
            type=EventTypes.DOCUMENT_LEFT.value,
            data=DocumentLeftData(session_id=session.id)
        ))

    async def _commit_doc_changes(self, document: Document, session: Session, changes: CommitChangesData) -> None:
        logger.info(f"{session.id} sent the following changeset: {changes.changeset}")
        pass
