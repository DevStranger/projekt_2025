# ms_calendar_integration.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("MS_CALENDAR_TENANT_ID")
CLIENT_ID = os.getenv("MS_CALENDAR_CLIENT_ID")
CLIENT_SECRET = os.getenv("MS_CALENDAR_CLIENT_SECRET")
REDIRECT_URI = os.getenv("MS_CALENDAR_REDIRECT_URI", "http://localhost:5000/ms-calendar/callback")

TENANT_ID="f8cdef31-a31e-4b4a-93e4-5f571e91255a"
CLIENT_ID="3afebc81-6ecc-4b0c-921f-010ffcd0a5d4"
CLIENT_SECRET="v4p8Q~mBxM93merPgRvkXzHp.7Vr~X.OkWNtQcm7"
REDIRECT_URI="https://login.microsoftonline.com/common/oauth2/nativeclient"

def get_ms_calendar_authorize_url_ms():
    """
    Generuje link, gdzie user się loguje i wyraża zgodę na dostęp do kalendarza.
    Microsoft Identity Platform v2 endpoint:
    https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
    """
    base_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
    scope = "Calendars.Read offline_access"

    return (
        f"{base_url}"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope={scope}"
    )

def exchange_code_for_token_ms(code):
    """
    Wymienia code na access_token używając endpointu:
    POST /{tenant}/oauth2/v2.0/token
    """
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "scope": "Calendars.Read offline_access",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": CLIENT_SECRET
    }

    resp = requests.post(token_url, data=data)
    token_json = resp.json()
    if "access_token" not in token_json:
        raise Exception(f"Błąd wymiany code na token: {token_json}")
    return token_json

def get_ms_calendar_events_ms(access_token):
    """
    Pobiera listę wydarzeń z kalendarza użytkownika:
    GET https://graph.microsoft.com/v1.0/me/events
    """
    url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "value" not in data:
        raise Exception(f"Błąd przy pobieraniu eventów: {data}")
    return data["value"]

def get_ms_calendar_event_details_ms(access_token, event_id):
    """
    Pobiera szczegóły wybranego wydarzenia:
    GET /me/events/{event_id}
    Zwraca obiekt zawierający m.in. 'attendees', 'start', 'end', 'subject'
    """
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "id" not in data:
        raise Exception(f"Nie znaleziono eventu {event_id} lub błąd: {data}")
    return data
