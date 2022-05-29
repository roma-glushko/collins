from pydantic import BaseModel


class Document(BaseModel):
    id: int
    title: str
    body: str


__all__ = ("Document", )