from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from livearea.connection_manager import ConnectionManager

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="templates")
connection_manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(client_id, websocket)
    await connection_manager.broadcast(f"#{client_id}: Joined the chat")

    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(client_id, f"You: {data}")
            await connection_manager.broadcast(f"#{client_id}: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
        await connection_manager.broadcast(f"#{client_id}: Left the chat")
