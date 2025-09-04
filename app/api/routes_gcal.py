# app/api/routes_gcal.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.gcal import get_auth_url, get_demo_events
from app.models.db import get_session
from fastapi.templating import Jinja2Templates
from app.models.widget_state import WidgetState

router = APIRouter(prefix="/gcal", tags=["gcal"])
templates = Jinja2Templates(directory="app/ui/templates")

@router.get("/auth")
async def start_auth(request: Request):
    """Start OAuth flow"""
    redirect_uri = str(request.url_for('oauth_callback'))
    auth_url = get_auth_url(redirect_uri)
    return RedirectResponse(auth_url)

@router.get("/callback")
async def oauth_callback(request: Request, code: str, session=Depends(get_session)):
    """Handle OAuth callback"""
    # Exchange code for token...
    # Store token in widget_state...
    return RedirectResponse('/')

# demo events, fix later
@router.get("/partial", response_class=HTMLResponse)
def calendar_partial(request: Request):
    events = get_demo_events()
    return templates.TemplateResponse(
        "calendar_widget.html",
        {"request": request, "events": events}
    )