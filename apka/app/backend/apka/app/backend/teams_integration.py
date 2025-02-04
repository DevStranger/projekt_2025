import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TEAMS_TENANT_ID")
CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
TEAMS_REDIRECT_URI = os.getenv("TEAMS_REDIRECT_URI", "http://localhost:5000/teams/callback")


def exchange_code_for_token(code):
    """
    Wymienia code (otrzymany w /teams/callback) na access_token.
    """
    url_token = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "scope": "Calendars.Read offline_access User.Read",
        "code": code,
        "redirect_uri": TEAMS_REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": CLIENT_SECRET
    }

    resp = requests.post(url_token, data=data)
    token_json = resp.json()
    if "access_token" not in token_json:
        raise Exception(f"Błąd przy wymianie code na token: {token_json}")

    return token_json  # Zwraca np. { "access_token": "...", "refresh_token": "...", ... }

def get_teams_events(access_token):
    """
    Pobiera listę eventów z kalendarza (Teams/Outlook).
    W Microsoft Graph: GET https://graph.microsoft.com/v1.0/me/events
    """
    url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "value" not in data:
        raise Exception(f"Błąd podczas pobierania eventów: {data}")

    return data["value"]  # lista eventów

def get_teams_event_details(access_token, event_id):
    """
    Pobiera szczegółowe dane wybranego eventu po id, w tym attendees.
    GET /me/events/{event_id}
    """
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "id" not in data:
        raise Exception(f"Nie znaleziono eventu lub błąd: {data}")
    return data
