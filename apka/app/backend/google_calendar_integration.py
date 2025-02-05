# google_calendar_integration.py
import os
import requests
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
import pytz


load_dotenv()

GOOGLE_CLIENT_ID = "907999041253-2eqttdeuvd1inb1oh6a81vptdk1sh9ao.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:5000/google-calendar/callback"

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_google_authorize_url():
    """
    Generuje link do logowania w Google.
    """
    print("DEBUG REDIRECT URI =", GOOGLE_REDIRECT_URI)
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )
    print(auth_url)
    return auth_url

def exchange_code_for_token2(code):
    """
    Wymienia 'code' na obiekt Credentials (zawierający access_token).
    """
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    print("credentials",creds)
    return creds  # obiekt Credentials

def get_google_events(credentials):
    """
    Pobiera listę wydarzeń z kalendarza.
    Zwraca tablicę obiektów  [ {summary, start, end, attendees, ...}, ... ]
    """
    service = build("calendar", "v3", credentials=credentials)
    now = datetime.now(timezone.utc).isoformat()

    # Wydarzenia z 'primary' kalendarza
    events_result = service.events().list(
        calendarId="primary",
        maxResults=10,
        singleEvents=True,
        orderBy="startTime",
        timeMin=now   # example, usun lub param
    ).execute()
    events = events_result.get("items", [])
    
    for event in events:
        start = event.get("start", {})
        end = event.get("end", {})

        event["start"] = format_event_datetime(start.get("dateTime") or start.get("date"))
        event["end"] = format_event_datetime(end.get("dateTime") or end.get("date"))

    return events

def get_google_event_details(credentials, event_id):
    """
    Pobiera szczegóły jednego wydarzenia z ID = event_id.
    """
    service = build("calendar", "v3", credentials=credentials)
    event = service.events().get(calendarId="primary", eventId=event_id).execute()
    return event


def format_event_datetime(dt_str):
    """ Konwertuje datę z ISO 8601 na czytelny format DD.MM.YYYY, HH:MM """
    if not dt_str:
        return "Brak daty"
    
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))  # Obsługa UTC
        dt = dt.astimezone(pytz.timezone("Europe/Warsaw"))  # Konwersja do PL
        return dt.strftime("%d.%m.%Y, %H:%M")  # Format DD.MM.YYYY, HH:MM
    except Exception as e:
        print("Błąd konwersji daty:", e)
        return dt_str  # Zwraca oryginalną wartość w razie błędu