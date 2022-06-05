import logging

from fastapi import FastAPI

from livearea.consts import SAMPLE_DOCUMENTS
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from livearea.repositories.documents import DocumentRepository, DocumentChannelRepository
from livearea.repositories.sessions import SessionRepository
from livearea.services.documents import DocumentRoomService
from livearea.services.events import EventService

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Starting up the Livearea app..")

    app.state.templates = Jinja2Templates(directory="templates")

    app.state.session_repository = SessionRepository()
    app.state.document_repository = DocumentRepository(SAMPLE_DOCUMENTS)
    app.state.doc_room_repository = DocumentChannelRepository()

    app.state.doc_room_service = DocumentRoomService(app.state.session_repository, app.state.doc_room_repository)
    app.state.event_service = EventService(app.state.doc_room_service)


__all__ = ("app",)
