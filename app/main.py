"""FastAPI entry point.

Wires the MVC-adapted layers: mounts static assets (VIEW), includes the page and
API routers (CONTROLLER), creates tables and seeds fictional data at startup.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.routers import api, pages
from app.seed import seed

_STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """On startup: create tables and load fictional test data (idempotent)."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Cargorex - Prototipo de Validacion de Horas de Investigacion",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")
app.include_router(pages.router)
app.include_router(api.router)
