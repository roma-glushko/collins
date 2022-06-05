import logging

from fastapi import Request, WebSocket, HTTPException
from fastapi.responses import HTMLResponse

from livearea.app import app
from livearea.entities.documents import Document, LatestDocumentRevision
from livearea.entities.sessions import Session
from livearea.logger import setup_logger
from livearea.repositories.documents import DocumentRepository
from livearea.services.events import EventService

setup_logger(logging.DEBUG)

logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the Documents Listing HTML page
    """
    templates = app.state.templates

    return templates.TemplateResponse("index.html", {"request": request}, media_type="text/html")


@app.get("/documents/{document_id}/", response_class=HTMLResponse)
async def view_document(request: Request, document_id: str):
    templates = app.state.templates

    return templates.TemplateResponse(
        "document_view.html",
        {"request": request, "document_id": document_id},
        media_type="text/html"
    )


@app.get("/api/documents/")
async def list_documents() -> list[LatestDocumentRevision]:
    documents: DocumentRepository = app.state.document_repository

    return [
        LatestDocumentRevision.from_doc(doc)
        for doc in documents
    ]


@app.get("/api/documents/{document_id}/")
async def get_document(document_id: int) -> Document:
    try:
        document_repository: DocumentRepository = app.state.document_repository

        return document_repository[document_id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Documents '{document_id}' doesn't exist. Please double check the documentID",
        )


@app.websocket("/documents/{document_id}/")
async def websocket_endpoint(
    websocket: WebSocket,
    document_id: int,
) -> None:
    document_repository: DocumentRepository = app.state.document_repository
    event_service: EventService = app.state.event_service

    logger.info(f"Establishing a connection to a document", extra={"document_id": document_id})

    try:
        document: Document = document_repository[document_id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Documents '{document_id}' doesn't exist",
        )

    session: Session = Session(connection=websocket)
    logger.info(f"Allocating a new session", extra={"session_id": session.id})

    await event_service.watch(document, session)
