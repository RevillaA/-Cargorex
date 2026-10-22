"""Page controller (VIEW): serves the single HTML page via Jinja2."""
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Render the prototype page (form + assignments table)."""
    return templates.TemplateResponse(request, "index.html")
