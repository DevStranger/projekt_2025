from datetime import datetime
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = os.getenv("ZOOM_REDIRECT_URI")


def get_zoom_authorize_url():
    """
    Generates the Zoom authorization URL.
    """
    base_url = "https://zoom.us/oauth/authorize"
    return (
        f"{base_url}?response_type=code"
        f"&client_id={ZOOM_CLIENT_ID}"
        f"&redirect_uri={ZOOM_REDIRECT_URI}"
    )


def exchange_code_for_token(code):
    """
    Exchanges authorization code for access token.
    """
    url_token = "https://zoom.us/oauth/token"
    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": ZOOM_REDIRECT_URI,
    }
    creds = f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}"
    b64_creds = base64.b64encode(creds.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_creds}"
    }
    resp = requests.post(url_token, headers=headers, params=params)
    data = resp.json()
    if "access_token" not in data:
        raise Exception(f"Błąd wymiany code na token: {data}")
    return data


def get_zoom_meetings(access_token):
    """
    Fetches the user's Zoom meetings.
    """
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "meetings" not in data:
        raise Exception(f"Błąd podczas pobierania spotkań: {data}")

    now = datetime.utcnow()  # Aktualna data i czas (UTC)
    meetings = []

    for meeting in data["meetings"]:
        meeting_start_time = datetime.strptime(meeting["start_time"], "%Y-%m-%dT%H:%M:%SZ")
        if meeting_start_time > now:  # Tylko przyszłe spotkania
            meetings.append({
                "id": meeting["id"],
                "topic": meeting["topic"],
                "start_time": meeting["start_time"]
            })

    return meetings


def get_personal_meeting_details(access_token, personal_meeting_id):
    """
    Pobiera szczegóły konkretnego spotkania, np. personal meeting ID.
    """
    url = f"https://api.zoom.us/v2/meetings/{personal_meeting_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "id" not in data:
        raise Exception(f"Błąd podczas pobierania spotkania: {data}")
    return data


def get_zoom_participants(meeting_id, access_token):
    """
    Fetches the list of participants for a specific meeting.
    """
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "participants" not in data:
        return []
    return data["participants"]
