from pydantic import BaseModel

DocumentId = int


class Document(BaseModel):
    id: DocumentId
    title: str
    body: str


__all__ = ("Document",)
