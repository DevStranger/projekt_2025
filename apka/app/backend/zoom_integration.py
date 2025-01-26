# zoom_integration.py
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
print("ZOOM_CLIENT_ID z .env to:", ZOOM_CLIENT_ID)  # Debug
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = os.getenv("ZOOM_REDIRECT_URI")

def get_zoom_authorize_url():
    """
    Zwraca URL do którego przekierujesz użytkownika,
    by uzyskać "code" w klasycznym OAuth2 flow.
    """
    base_url = "https://zoom.us/oauth/authorize"
    # Gdy user wchodzi na ten link, Zoom pyta go o zgodę i na końcu
    # wywołuje /zoom/callback?code=XYZ
    return f"{base_url}?response_type=code&client_id={ZOOM_CLIENT_ID}&redirect_uri={ZOOM_REDIRECT_URI}"

def exchange_code_for_token(code):
    """
    Otrzymuje "code" z query param w URL i wymienia go na access_token.
    """
    url_token = "https://zoom.us/oauth/token"
    # W OAuth user-level parametry:
    #   grant_type=authorization_code
    #   code=...
    #   redirect_uri=...
    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": ZOOM_REDIRECT_URI,
    }

    # Zoom wymaga Basic Auth z (client_id:client_secret)
    creds = f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}"
    b64_creds = base64.b64encode(creds.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_creds}"
    }

    resp = requests.post(url_token, headers=headers, params=params)
    data = resp.json()
    if "access_token" not in data:
        raise Exception(f"Błąd wymiany code na token: {data}")

    # data zawiera:
    # {
    #   "access_token": "...",
    #   "token_type": "bearer",
    #   "refresh_token": "...",
    #   "expires_in": 3599,
    #   ...
    # }
    return data  # Zwracamy cały JSON (możesz zapisać go w sesji, bazie, itp.)

def get_zoom_meetings(access_token):
    """
    Pobiera listę spotkań użytkownika Zoom
    korzystając z otrzymanego access_token.
    """
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    if "meetings" not in data:
        raise Exception(f"Błąd podczas pobierania spotkań: {data}")

    return data["meetings"]  # Zwracamy listę meetingów

def get_personal_meeting_details(access_token, personal_meeting_id):
    """
    Pobiera szczegóły konkretnego spotkania, np. personal meeting ID,
    jeśli chcesz np. /meetings/<meetingId>.
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
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.get(url, headers=headers)
    data = resp.json()
    # Gdy spotkanie jest jeszcze w toku, to 'report' nie zadziała
    # lub jeśli brakuje licencji/pro planu - sprawdź w doc. Zoom
    if "participants" not in data:
        # jeśli chcesz zwracać pustą listę zamiast błędu:
        return []
    return data["participants"]  # np. [{user_email: "..."}]

def get_zoom_authorize_url():
    base_url = "https://zoom.us/oauth/authorize"
    # Debug: sprawdź, co zostało wczytane
    print("ZOOM_CLIENT_ID =", ZOOM_CLIENT_ID)
    print("ZOOM_REDIRECT_URI =", ZOOM_REDIRECT_URI)
    
    return (
        f"{base_url}"
        f"?response_type=code"
        f"&client_id={ZOOM_CLIENT_ID}"
        f"&redirect_uri={ZOOM_REDIRECT_URI}"
    )

def exchange_code_for_token(code):
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

    print("DEBUG: Wysyłamy request do Zoom z parametrami:", params)
    print("DEBUG: Authorization:", headers["Authorization"])

    resp = requests.post(url_token, headers=headers, params=params)
    data = resp.json()
    print("DEBUG: Odpowiedź Zoom:", data['access_token'])

    if "access_token" not in data:
        raise Exception(f"Błąd wymiany code na token: {data['access_token']}")

    return data['access_token']
