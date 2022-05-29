import logging
from typing import Optional

from livearea.entities import Document

logger = logging.getLogger(__name__)


class DocumentManager:
    def __init__(self, available_documents: Optional[dict[str, Document]] = None) -> None:
        self.documents = available_documents or {}