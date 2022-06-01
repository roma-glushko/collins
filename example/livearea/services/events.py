from typing import Any

from fastapi import WebSocketDisconnect

from livearea.entities.documents import Document
from livearea.entities.sessions import Session
from livearea.protocol.events import Message, EventTypes, DocumentOpenedData, DocumentLeftData
from livearea.services.documents import DocumentRoomService


class EventService:
    def __init__(self, doc_room_service: DocumentRoomService) -> None:
        self.doc_room_service: DocumentRoomService = doc_room_service

    async def watch(self, document: Document, session: Session) -> None:
        await self.doc_room_service.broadcast(document, Message(
            type=EventTypes.DOCUMENT_JOINED.value,
            data=DocumentLeftData(session_id=session.id),
        ))

        await self.doc_room_service.join(document, session)

        await session.send_message(Message(
            type=EventTypes.DOCUMENT_OPENED.value,
            data=DocumentOpenedData(
                session_id=session.id,
                document=document,
            )
        ))

        try:
            while True:
                data: dict[Any, Any] = await session.connection.receive_json()
                message: Message = Message(**data)

                # TODO:
        except WebSocketDisconnect:
            await self.doc_room_service.leave(document, session)

            await self.doc_room_service.broadcast(document, Message(
                type=EventTypes.DOCUMENT_LEFT.value,
                data=DocumentLeftData(session_id=session.id)
            ))
