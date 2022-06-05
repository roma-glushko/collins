from typing import Optional

from pydantic import BaseModel, Field

from collins.changeset import Changeset

DocumentId = int


class Revision(BaseModel):
    changeset: Changeset
    text: str

    class Config:
        arbitrary_types_allowed = True


class Document(BaseModel):
    id: DocumentId
    title: str
    revisions: list[Revision] = Field(default_factory=list)


class LatestDocumentRevision(BaseModel):
    id: DocumentId
    title: str
    text: str
    revision_id: int

    @classmethod
    def from_doc(cls, document: Document) -> "LatestDocumentRevision":
        revision_id: int = len(document.revisions) - 1
        last_revision: Optional[Revision] = document.revisions[-1]

        return cls(
            id=document.id,
            title=document.title,
            text=last_revision.text,
            revision_id=revision_id,
        )


__all__ = ("Document", "LatestDocumentRevision")
