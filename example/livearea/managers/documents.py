import logging
from typing import Optional, Iterator

from livearea.entities import Document

logger = logging.getLogger(__name__)


class DocumentManager:
    def __init__(self, available_documents: Optional[dict[int, Document]] = None) -> None:
        self._documents = available_documents or {}

    def __len__(self) -> int:
        return len(self._documents)

    def __iter__(self) -> Iterator[Document]:
        return iter(self._documents.values())

    def __getitem__(self, document_id: int) -> Document:
        return self._documents[document_id]
