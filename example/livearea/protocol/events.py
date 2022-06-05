from enum import Enum

from pydantic import BaseModel

from livearea.entities.documents import LatestDocumentRevision


class EventTypes(str, Enum):
    DOCUMENT_OPENED = "document_opened"
    DOCUMENT_JOINED = "document_joined"
    DOCUMENT_LEFT = "document_left"

    COMMIT_CHANGES = "commit_changes"


class EventData(BaseModel):
    pass


class DocumentOpenedData(EventData):
    session_id: str
    document: LatestDocumentRevision
    other_viewers: list[str]


class DocumentJoinedData(EventData):
    session_id: str


class DocumentLeftData(EventData):
    session_id: str


class CommitChangesData(EventData):
    base_revision: int
    changeset: str


class Message(BaseModel):
    type: EventTypes
    data: EventData
