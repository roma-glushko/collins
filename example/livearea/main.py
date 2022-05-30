import logging

from fastapi import Request, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.responses import HTMLResponse

from livearea.app import app
from livearea.entities import Document
from livearea.managers import ConnectionManager, DocumentManager

logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the Document Listing HTML page
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
async def list_documents() -> list[Document]:
    documents: DocumentManager = app.state.documents

    return [
        doc
        for doc in documents
    ]


@app.get("/api/documents/{document_id}/")
async def get_document(document_id: int) -> Document:
    try:
        documents: DocumentManager = app.state.documents

        return documents[document_id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{document_id}' doesn't exist. Please double check the documentID",
        )


@app.websocket("/documents/{document_id}/")
async def websocket_endpoint(
    websocket: WebSocket,
    document_id: int,
    client_id: str = Query(...),
) -> None:
    documents: DocumentManager = app.state.documents
    connections: ConnectionManager = app.state.connections

    try:
        document = documents[document_id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{document_id}' doesn't exist",
        )

    await connections.join(document_id, client_id, websocket)
    await connections.broadcast(document_id, f"Client \"{client_id}\" has joined the \"{document.title}\" document")

    try:
        while True:
            data = await websocket.receive_json()

            await connections.broadcast(document_id, f"#{client_id}: {data}")
    except WebSocketDisconnect:
        await connections.leave(document_id, client_id)
        await connections.broadcast(document_id, f"Client \"{client_id}\" has left the \"{document.title}\" document")
