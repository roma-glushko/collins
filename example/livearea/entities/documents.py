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


__all__ = ("Document",)
