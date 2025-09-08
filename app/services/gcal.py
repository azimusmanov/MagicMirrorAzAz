# filepath: /Users/azimusmanov/Documents/MagicMirrorAzAz/app/services/gcal.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta

# Temporary demo events function - keep this for fallback
def get_demo_events(days: int = 3):
    """Return demo events until OAuth is implemented."""
    now = datetime.now().replace(second=0, microsecond=0)
    
    # Demo events with variety
    items = [
        {"summary": "Morning Standup", "start": now.replace(hour=9, minute=0)},
        {"summary": "Gym", "start": now.replace(hour=18, minute=0)},
        {"summary": "Dinner", "start": now.replace(hour=20, minute=30)},
        {"summary": "Flight", "start": (now + timedelta(days=1)).replace(hour=11, minute=45)},
        {"summary": "Doctor Appointment", "start": (now + timedelta(days=2)).replace(hour=14, minute=30)},
        {"summary": "Birthday Party", "start": (now + timedelta(days=2)).replace(hour=19, minute=0)},
    ]
    
    events = []
    for it in items:
        start = it["start"]
        end = start + timedelta(hours=1)
        events.append({
            "summary": it["summary"],
            "time": start.strftime("%I:%M %p").lstrip("0"),
            "end": end.strftime("%I:%M %p").lstrip("0"),
            "date": start.strftime("%a %b %d"),
        })
    return events

# Constants
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'  # You'll need this file later

def get_auth_url(redirect_uri):
    """Generate OAuth authorization URL"""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri)
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return auth_url

def get_events(credentials_json, days=7):
    """Get upcoming calendar events"""
    credentials = Credentials.from_authorized_user_info(credentials_json, SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    
    # Fix the deprecated utcnow
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    end_date = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat().replace('+00:00', 'Z')
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end_date,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    return events_result.get('items', [])