import logging

from fastapi import Request, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse

from livearea.app import app
from livearea.consts import DOCUMENT_MAP
from livearea.entities import Document
from livearea.managers import ConnectionManager

logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the Document Listing HTML page
    """
    templates = app.state.templates

    return templates.TemplateResponse("index.html", {"request": request}, media_type="text/html")


@app.get("/api/documents")
async def list_documents() -> list[Document]:
    return [
        doc
        for doc in DOCUMENT_MAP.values()
    ]


@app.websocket("/documents/{document_id}/")
async def websocket_endpoint(
        websocket: WebSocket,
        document_id: str,
        client_id: str = Query(...),
) -> None:
    connections: ConnectionManager = app.state.connections

    await connections.join(document_id, client_id, websocket)
    await connections.broadcast(document_id, f"#{client_id}: Joined the chat")

    try:
        while True:
            data = await websocket.receive_json()

            await connections.broadcast(document_id, f"#{client_id}: {data}")
    except WebSocketDisconnect:
        await connections.leave(document_id, client_id)
        await connections.broadcast(document_id, f"#{client_id}: Left the chat")
