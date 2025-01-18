import datetime
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_events():
    # Ścieżka do pliku token.json w folderze `app`
    token_path = os.path.join(os.path.dirname(__file__), "token.json")

    # Usuń istniejący plik token.json, jeśli istnieje
    if os.path.exists(token_path):
        print(f"Removing existing token file at {token_path}...")
        os.remove(token_path)

    creds = None

    # Zawsze generuj nowy token
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(os.path.dirname(__file__), "credentials.json"), SCOPES
    )
    creds = flow.run_local_server(port=5001, access_type="offline", prompt="consent")

    # Zapisz nowo wygenerowany token
    with open(token_path, "w") as token:
        print(f"Saving new token file to {token_path}...")
        token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        formatted_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "Brak nazwy wydarzenia")
            
            # Konwertuj datę i godzinę na czytelny format
            if "T" in start:  # Jeśli jest pełna data i godzina
                start_time = parser.parse(start).strftime("%Y-%m-%d %H:%M")
            else:  # Jeśli tylko data
                start_time = start

            formatted_events.append({"start": start_time, "summary": summary})

        return formatted_events
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []