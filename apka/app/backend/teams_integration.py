import os
import requests
import pytz
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TENANT_ID = os.getenv("TEAMS_TENANT_ID")
CLIENT_ID = os.getenv("TEAMS_CLIENT_ID")
CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
TEAMS_REDIRECT_URI = os.getenv("TEAMS_REDIRECT_URI", "http://localhost:5000/teams/callback")


def format_event_datetime(dt_str):
    """ 
    Konwertuje datę z ISO 8601 (np. 2025-02-03T00:00:00.0000000Z)
    na czytelny format: DD.MM.YYYY, HH:MM w strefie Europe/Warsaw
    """
    if not dt_str:
        return "Brak daty"

    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))  
        dt_pl = dt.astimezone(pytz.timezone("Europe/Warsaw"))    
        return dt_pl.strftime("%d.%m.%Y, %H:%M")
    except Exception as e:
        print("Błąd konwersji daty:", e)
        return dt_str


def is_future_event(dt_str):
    """
    Sprawdza, czy data zdarzenia jest >= TERAZ (w strefie Europe/Warsaw).
    Zwraca True, jeśli wydarzenie jest w przyszłości.
    """
    if not dt_str:
        return False
    try:
        dt_utc = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        dt_warsaw = dt_utc.astimezone(pytz.timezone("Europe/Warsaw"))

        now_warsaw = datetime.now(pytz.timezone("Europe/Warsaw"))

        return dt_warsaw >= now_warsaw
    except Exception as e:
        print("Błąd w is_future_event:", e)
        return False


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

    return token_json


def get_teams_events(access_token):
    """
    Pobiera listę eventów z kalendarza (Teams/Outlook).
    Następnie zwraca TYLKO przyszłe wydarzenia, już z sformatowanymi datami.
    """
    url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()

    if "value" not in data:
        raise Exception(f"Błąd podczas pobierania eventów: {data}")

    all_events = data["value"]
    future_events = []

    for evt in all_events:
        start_dt = evt.get("start", {}).get("dateTime")
        if start_dt and is_future_event(start_dt):
            evt["start"]["dateTime"] = format_event_datetime(start_dt)

            end_dt = evt.get("end", {}).get("dateTime")
            if end_dt:
                evt["end"]["dateTime"] = format_event_datetime(end_dt)

            future_events.append(evt)

    return future_events


def get_teams_event_details(access_token, event_id):
    """
    Pobiera szczegółowe dane wybranego eventu po id, w tym attendees.
    GET /me/events/{event_id}
    (tutaj nie filtrujemy czy jest w przyszłości, bo to 'szczegóły')
    """
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()

    if "id" not in data:
        raise Exception(f"Nie znaleziono eventu lub błąd: {data}")

    s_dt = data.get("start", {}).get("dateTime")
    if s_dt:
        data["start"]["dateTime"] = format_event_datetime(s_dt)

    e_dt = data.get("end", {}).get("dateTime")
    if e_dt:
        data["end"]["dateTime"] = format_event_datetime(e_dt)

    return data
