from enum import Enum
from pydantic import BaseModel

from livearea.entities.documents import Document


class EventTypes(str, Enum):
    DOCUMENT_OPENED = "document_opened"
    DOCUMENT_JOINED = "document_joined"
    DOCUMENT_LEFT = "document_left"


class EventData(BaseModel):
    pass


class DocumentOpenedData(EventData):
    session_id: str
    document: Document


class DocumentJoinedData(EventData):
    session_id: str


class DocumentLeftData(EventData):
    session_id: str


class Message(BaseModel):
    type: EventTypes
    data: EventData
