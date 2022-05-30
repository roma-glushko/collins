import logging

from fastapi import FastAPI

from livearea.consts import DOCUMENT_MAP
from livearea.managers import ConnectionManager, DocumentManager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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

    app.state.connections = ConnectionManager()
    app.state.documents = DocumentManager(DOCUMENT_MAP)
    app.state.templates = Jinja2Templates(directory="templates")


__all__ = ("app",)
