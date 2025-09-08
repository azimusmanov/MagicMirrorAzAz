from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.gcal import get_demo_events, get_auth_url, get_events
from app.models.db import get_session
from app.models.widget_state import WidgetState
from google_auth_oauthlib.flow import Flow
from datetime import datetime, timedelta
from sqlmodel import select
import json
import os

templates = Jinja2Templates(directory="app/ui/templates")
router = APIRouter(prefix="/gcal", tags=["gcal"])
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@router.get("/auth")
async def start_auth(request: Request):
    """Start OAuth flow"""
    # Build the redirect_uri dynamically from the request
    redirect_uri = str(request.base_url)
    if not redirect_uri.endswith('/'):
        redirect_uri += '/'
    redirect_uri += "gcal/callback"
    
    auth_url = get_auth_url(redirect_uri)
    return RedirectResponse(auth_url)

@router.get("/callback")
async def oauth_callback(request: Request, code: str, session=Depends(get_session)):
    """Handle OAuth callback"""
    # Build the redirect_uri dynamically - must match what we used in /auth
    redirect_uri = str(request.base_url)
    if not redirect_uri.endswith('/'):
        redirect_uri += '/'
    redirect_uri += "gcal/callback"
    
    # Create flow instance to exchange auth code for token
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri)
    
    # Exchange code for token
    flow.fetch_token(code=code)
    
    # Store credentials
    credentials = flow.credentials
    credentials_json = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    # Save to widget state
    state = session.exec(select(WidgetState).where(WidgetState.key == "gcal_auth")).first()
    if not state:
        state = WidgetState(key="gcal_auth")
    state.state_json = json.dumps(credentials_json)
    session.add(state)
    session.commit()
    
    return RedirectResponse('/')

USE_DEMO = os.getenv("USE_DEMO_CALENDAR", "false").lower() == "true"

@router.get("/partial", response_class=HTMLResponse)
def calendar_partial(request: Request, days: int = Query(1), session=Depends(get_session)):
    """
    Get calendar widget HTML
    days: Number of days to display (default: 1 = today only)
    """
    if USE_DEMO:
        # Show empty list to trigger the connect button
        return templates.TemplateResponse(
            "calendar_widget.html",
            {"request": request, "events": [], "days": days}
        )
    try:
        # Try to get credentials from widget state
        state = session.exec(select(WidgetState).where(WidgetState.key == "gcal_auth")).first()
        if state and state.state_json and os.path.exists(CLIENT_SECRETS_FILE):
            credentials_json = json.loads(state.state_json)
            raw_events = get_events(credentials_json, days=days)
            
            # Process and format events
            events = []
            today = datetime.now().date()
            
            for event in raw_events:
                start = event.get('start', {})
                time_str = start.get('dateTime', start.get('date', ''))
                
                # Skip if no time info
                if not time_str:
                    continue
                
                # Handle dateTime (specific time) vs date (all-day)
                if 'T' in time_str:  # Has time component
                    event_time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    local_time = event_time.astimezone()
                    
                    # Filter for requested days
                    days_diff = (local_time.date() - today).days
                    if days_diff < 0 or days_diff >= days:
                        continue
                    
                    # Get end time
                    end = event.get('end', {}).get('dateTime', '')
                    end_time = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone() if end else local_time + timedelta(hours=1)
                    
                    events.append({
                        'summary': event.get('summary', 'No title'),
                        'time': local_time.strftime("%I:%M %p").lstrip("0"),
                        'end': end_time.strftime("%I:%M %p").lstrip("0"),
                        'date': local_time.strftime("%a %b %d")
                    })
                else:
                    # All-day event
                    event_date = datetime.fromisoformat(time_str).date()
                    days_diff = (event_date - today).days
                    if days_diff < 0 or days_diff >= days:
                        continue
                    
                    events.append({
                        'summary': event.get('summary', 'No title'),
                        'time': "All day",
                        'end': "",
                        'date': datetime.fromisoformat(time_str).strftime("%a %b %d")
                    })
            
            # Sort by time
            events.sort(key=lambda x: "00:00" if x['time'] == "All day" else x['time'])
            
            return templates.TemplateResponse(
                "calendar_widget.html",
                {"request": request, "events": events, "days": days}
            )
            
    except Exception as e:
        print(f"Error fetching calendar: {str(e)}")
    
    # Fallback to demo events with filtering
    all_events = get_demo_events()
    today_str = datetime.now().strftime("%a %b %d")
    filtered_events = [e for e in all_events if e['date'] == today_str]
    
    return templates.TemplateResponse(
        "calendar_widget.html",
        {"request": request, "events": filtered_events, "days": days}
    )