from docx import Document
import re
from flask import Blueprint, Flask, jsonify, render_template, current_app, request, send_from_directory, session, redirect, url_for, flash
import requests
import pygetwindow as gw
from .recording import record_window, start_recording_thread, stop_recording, save_recording, setup_upload_folder
import os
from werkzeug.utils import secure_filename
from .note import process_audio_and_save_transcription
from .screenshot import extract_screenshots_from_video
import base64
from .teams_integration import get_teams_events
from . import db
from .models import db, Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
from flask import jsonify

# Import funkcji z plików integracyjnych
from .zoom_integration import (
    get_zoom_authorize_url,
    exchange_code_for_token,
    get_zoom_meetings,
    get_personal_meeting_details,
    get_zoom_participants
)
from .teams_integration import (
    exchange_code_for_token,
    get_teams_events,
    get_teams_event_details
)

from .google_calendar_integration import (
    get_google_authorize_url,
    exchange_code_for_token2,
    get_google_events,
    get_google_event_details
)

from dotenv import find_dotenv
load_dotenv()
print("Ścieżka do pliku .env:", find_dotenv())


ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = os.getenv("ZOOM_REDIRECT_URI")

TEAMS_TENANT_ID = os.getenv("TEAMS_TENANT_ID")
TEAMS_CLIENT_ID =  os.getenv("TEAMS_CLIENT_ID")
TEAMS_CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")
TEAMS_REDIRECT_URI = os.getenv("TEAMS_REDIRECT_URI")  
TEAMS_CLIENT_VALUE = os.getenv("TEAMS_CLIENT_VALUE")


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'recordings')
SCREENSHOT_FOLDER = os.path.join(UPLOAD_FOLDER, 'screenshots')
ALLOWED_EXTENSIONS = {'webm', 'mp4', 'avi'}

# Folder na notatki (DOCX)
NOTES_FOLDER = os.path.join(UPLOAD_FOLDER, 'notes')
os.makedirs(NOTES_FOLDER, exist_ok=True)

main = Blueprint('main', __name__, template_folder="../frontend/templates", static_folder="../frontend/static")


# STRONA GŁÓWNA
@main.route("/")
def index():
    return render_template("index.html")


# ZOOM INTEGRATION
def get_zoom_authorize_url():
    base_url = "https://zoom.us/oauth/authorize"
    print("ZOOM_CLIENT_ID =", ZOOM_CLIENT_ID)
    print("ZOOM_REDIRECT_URI =", ZOOM_REDIRECT_URI)
    
    return (
        f"{base_url}?"
        f"response_type=code"
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
    print("DEBUG: Odpowiedź Zoom:", data)

    if "access_token" not in data:
        raise Exception(f"Błąd wymiany code na token: {data}")

    return data['access_token']


@main.route("/zoom/login")
def zoom_login():
    # Generujemy URL autoryzacji i przekierowujemy
    auth_url = get_zoom_authorize_url()
    return redirect(auth_url)

@main.route("/zoom/callback")
def zoom_callback():
    code = request.args.get("code")
    if not code:
        return "Brak parametru 'code' w callbacku", 400

    try:
        token_data = exchange_code_for_token(code)
        session["zoom_access_token"] = token_data
        return render_template("my_events.html")
    except Exception as e:
        return f"Błąd podczas wymiany code na token: {e}", 400


@main.route("/zoom-events")
def zoom_events():
    # Pobieramy spotkania z Zoom
    access_token = session.get("zoom_access_token")
    if not access_token:
        return jsonify({"error": "Brak access_token – zaloguj się przez /zoom/login"}), 401

    try:
        meetings = get_zoom_meetings(access_token)
        return jsonify(meetings)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route("/zoom-meetings")
def zoom_meetings():
    try:
        access_token = session.get("zoom_access_token")
        meetings = get_zoom_meetings(access_token)
        return jsonify(meetings)  # np. [{topic, start_time, join_url}, ...]
    except Exception as e:
        print("Błąd w /zoom-meetings:", e)
        return jsonify({"error": str(e)}), 400


@main.route("/zoom-personal-meeting")
def zoom_personal_meeting():
    # Szczegóły personalnego meetingu Zoom
    access_token = session.get("zoom_access_token")
    if not access_token:
        return jsonify({"error": "Brak access_token – zaloguj się przez /zoom/login"}), 401

    personal_meeting_id = request.args.get("pmid")
    if not personal_meeting_id:
        return jsonify({"error": "Podaj ?pmid=... w URL"}), 400

    try:
        meeting_data = get_personal_meeting_details(access_token, personal_meeting_id)
        return jsonify(meeting_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main.route("/zoom-meeting-participants")
def zoom_meeting_participants():
    access_token = session.get("zoom_access_token")
    if not access_token:
        return jsonify({"error": "Nie jesteś zalogowany w Zoom."}), 401

    meeting_id = request.args.get("meetingId")
    if not meeting_id:
        return jsonify({"error": "Brak parametru meetingId"}), 400

    try:
        participants = get_zoom_participants(meeting_id, access_token)
        return jsonify(participants)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# TEAMS INTEGRATION

def get_teams_authorize_url():
    base_url = f"https://login.microsoftonline.com/{TEAMS_TENANT_ID}/oauth2/v2.0/authorize"
    scope = "Calendars.Read offline_access User.Read"  # minimalny zestaw do przykładu
    # scope = "Calendars.ReadWrite offline_access User.Read" jeśli potrzebujesz więcej
    return (
        f"{base_url}"
        f"?client_id={TEAMS_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={TEAMS_REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope={scope}"
    )
def exchange_code_for_token_teams(code):
    """
    Wymienia 'code' (otrzymany w /teams/callback) na token dostępu (access_token).
    """
    # Endpoint tokena dla danej dzierżawy (lub 'common' dla multi-tenant)
    token_url = f"https://login.microsoftonline.com/{TEAMS_TENANT_ID}/oauth2/v2.0/token"

    # Scope – minimalnie np. "User.Read" i "Calendars.Read". Może być też "offline_access".
    data = {
        "client_id": TEAMS_CLIENT_ID,
        "client_secret": TEAMS_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": TEAMS_REDIRECT_URI,
        "scope": "User.Read Calendars.Read offline_access"
    }

    resp = requests.post(token_url, data=data)
    token_json = resp.json()

    # Sprawdź czy jest access_token
    if "access_token" not in token_json:
        raise Exception(f"Błąd przy wymianie code na token: {token_json}")

    # Zwracamy cały obiekt np. { "access_token": ..., "refresh_token": ..., ... }
    return token_json


@main.route("/teams/login")
def teams_login():
    auth_url = get_teams_authorize_url()
    return redirect(auth_url)

@main.route("/teams/callback")
def teams_callback():
    code = request.args.get("code")
    if not code:
        return "Brak parametru 'code'", 400

    try:
        token_json = exchange_code_for_token_teams(code)
        # zapisz access_token do session
        print("test")
        session["teams_access_token"] = token_json["access_token"]
        return render_template("my_events2.html")
    except Exception as e:
        return f"Błąd: {e}", 400

@main.route("/teams-events")
def teams_events():
    access_token = session.get("teams_access_token")
    if not access_token:
        return jsonify({"error": "Niezalogowany w Teams"}), 401

    try:
        events = get_teams_events(access_token)
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/teams-event-details")
def teams_event_details_route():
    access_token = session.get("teams_access_token")
    if not access_token:
        return jsonify({"error": "Niezalogowany w Teams"}), 401

    event_id = request.args.get("eventId")
    if not event_id:
        return jsonify({"error": "Brak parametru eventId"}), 400

    try:
        event_details = get_teams_event_details(access_token, event_id)
        return jsonify(event_details)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# GOOGLE CALENDAR INTEGRATION
@main.route("/google-calendar/login")
def google_calendar_login():
    auth_url = get_google_authorize_url()
    print("przystanek")
    return redirect(auth_url)

@main.route("/google-calendar/callback")
def google_calendar_callback():
    code = request.args.get("code")
    print(code)
    if not code:
        return "Brak parametru 'code'", 400
    try:
        creds = exchange_code_for_token2(code)
        # Zapisz w session
        session["google_creds"] = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes
        }
        return render_template("my_google_calendar.html")
    except Exception as e:
        return f"Błąd: {e}", 400

@main.route("/google-calendar/events")
def google_calendar_events():
    if "google_creds" not in session:
        return jsonify({"error": "Niezalogowany w Google Calendar"}), 401

    creds_info = session["google_creds"]
    creds = Credentials(**creds_info)

    try:
        events = get_google_events(creds)
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/google-calendar/event-details")
def google_calendar_event_details():
    if "google_creds" not in session:
        return jsonify({"error": "Niezalogowany w Google Calendar"}), 401

    event_id = request.args.get("eventId")
    if not event_id:
        return jsonify({"error": "Brak parametru eventId"}), 400

    creds_info = session["google_creds"]
    creds = Credentials(**creds_info)

    try:
        event = get_google_event_details(creds, event_id)
        return jsonify(event)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/my_google_calendar")
def google_calendar_page():
    return render_template("my_google_calendar.html")


# OBSŁUGA NAGRYWANIA
@main.route("/record")
def record():
    return render_template("record.html")

@main.route("/list_windows", methods=["GET"])
def list_windows():
    """Zwróć listę okien."""
    windows = gw.getAllTitles()
    windows = [w for w in windows if w]
    return jsonify(windows)

@main.route("/record/record_window", methods=["POST"])
def record_window_route():
    setup_upload_folder()
    data = request.get_json()
    window_title = data.get("window_title")

    if not window_title:
        return jsonify({"message": "Nie podano tytułu okna."}), 400

    # Uruchom nagrywanie w osobnym wątku
    start_recording_thread(window_title)

    return jsonify({"message": f"Rozpoczęto nagrywanie okna: {window_title}"})

@main.route("/record/stop_recording", methods=["POST"])
def stop_recording_route():
    try:
        stop_recording()
        return jsonify({"message": "Nagrywanie zakończone pomyślnie."})
    except Exception as e:
        return jsonify({"message": f"Błąd podczas zatrzymywania nagrywania: {str(e)}"}), 500

@main.route('/save', methods=['POST'])
def save_recording_route():
    setup_upload_folder()
    """Zapisz nagranie i przekonwertuj na MP4, następnie wyciągnij screeny i przetwarzaj audio na notatki."""
    try:
        file = request.files['file']
        title = request.form.get('title', 'recording')
        mp4_path, wav_path = save_recording(file, title)

        # Zrzuty ekranu
        screenshots_folder = os.path.join(SCREENSHOT_FOLDER, title)
        os.makedirs(screenshots_folder, exist_ok=True)
        extract_screenshots_from_video(mp4_path, screenshots_folder, fps=1)

        # Generowanie notatek (DOCX)
        docx_folder = os.path.join(UPLOAD_FOLDER, 'notes')
        os.makedirs(docx_folder, exist_ok=True)
        process_audio_and_save_transcription(UPLOAD_FOLDER, docx_folder, screenshots_folder)

        return render_template('index.html', message="Nagranie zapisane!", path=mp4_path)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Nieoczekiwany błąd.', 'details': str(e)}), 500

@main.route('/my_recordings')
def show_recordings():
    setup_upload_folder()
    recordings = os.listdir(UPLOAD_FOLDER)
    recordings = [f for f in recordings if f.endswith(('.mp4'))]
    recordings = [os.path.splitext(file)[0] for file in recordings]
    return render_template('my_recordings.html', recordings=recordings)

@main.route('/recordings/<filename>')
def get_recording(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename + ".mp4")
    except FileNotFoundError:
        return "File not found", 404


# OBSŁUGA NOTATEK
@main.route('/generate_notes', methods=['POST'])
def generate_notes():
    """Generuj transkrypcję notatek na podstawie istniejącego pliku .wav."""
    try:
        title = request.form.get('title')
        if not title:
            return jsonify({'error': 'Brak nazwy pliku! Podaj tytuł pliku WAV.'}), 400

        wav_path = os.path.join(UPLOAD_FOLDER, f"{title}.wav")
        if not os.path.exists(wav_path):
            return jsonify({'error': f"Plik {title}.wav nie istnieje w katalogu recordings!"}), 404

        notes_folder = os.path.join(os.getcwd(), 'notes')
        if not os.path.exists(notes_folder):
            os.makedirs(notes_folder)

        # Generowanie transkrypcji
        process_audio_and_save_transcription(wav_path, notes_folder)

        return jsonify({
            'message': f"Transkrypcja wygenerowana dla {title}.wav!",
            'path': os.path.join(notes_folder, f"{title}.docx")
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Nieoczekiwany błąd.', 'details': str(e)}), 500


# WYSZUKIWANIE W NOTATKACH
def search_in_docx(file_path, query):
    """Sprawdza, czy dany plik .docx zawiera tekst pasujący do zapytania."""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if query in para.text.lower():
                return True
    except Exception as e:
        print(f"Błąd odczytu pliku {file_path}: {e}")
    return False

@main.route('/search_docx')
def search_docx():
    query = request.args.get('query', '').lower()
    matching_files = []

    if not query:
        return jsonify([])

    for filename in os.listdir(NOTES_FOLDER):
        if filename.endswith('.docx'):
            file_path = os.path.join(NOTES_FOLDER, filename)
            if search_in_docx(file_path, query):
                matching_files.append(filename.replace(".docx", ""))

    return jsonify(matching_files)


# OBSŁUGA WYŚWIETLANIA WYDARZEŃ
@main.route("/my_events")
def events_page():
    return render_template("my_events.html")
@main.route("/my_events2")
def events_page2():
    return render_template("my_events2.html")



# OBSŁUGA E-MAILI I NOTATEK
@main.route("/my_notes")
def show_notes():
    """
    Wyświetla listę wygenerowanych notatek (plików .docx)
    oraz listę adresów e-mail z bazy danych.
    """
    if not os.path.exists(NOTES_FOLDER):
        return render_template('my_notes.html', notes=[], emails=[])

    notes = [f for f in os.listdir(NOTES_FOLDER) if f.endswith('.docx')]
    notes = [os.path.splitext(file)[0] for file in notes]

    all_emails = Email.query.all()
    return render_template('my_notes.html', notes=notes, emails=all_emails)

@main.route("/add_email", methods=["POST"])
def add_email():
    """
    Dodaje nowy adres e-mail do bazy.
    """
    data = request.get_json()
    email_value = data.get("email", "").strip()

    if not email_value:
        return jsonify({"error": "Nie podano adresu e-mail!"}), 400

    existing_email = Email.query.filter_by(email=email_value).first()
    if existing_email:
        return jsonify({"error": "Ten adres e-mail już istnieje!"}), 409

    try:
        new_email = Email(email=email_value)
        db.session.add(new_email)
        db.session.commit()
        return jsonify({"message": "Adres e-mail dodany!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Wystąpił błąd podczas dodawania e-maila."}), 500

@main.route("/delete_email", methods=["POST"])
def delete_email():
    """
    Usuwa wybrane adresy e-mail z bazy danych.
    """
    try:
        data = request.get_json()
        email_addresses = data.get("emails", [])  

        if not email_addresses:
            return jsonify({"error": "Nie wybrano żadnych e-maili do usunięcia."}), 400

        for email in email_addresses:
            email_obj = Email.query.filter_by(email=email).first()
            if email_obj:
                db.session.delete(email_obj)
            else:
                print(f"E-mail {email} nie znaleziony w bazie.") 

        db.session.commit()
        return jsonify({"message": "E-maile zostały usunięte."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Błąd podczas usuwania e-maili: {str(e)}"}), 500

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)
@main.route('/send_notes', methods=['POST'])
def send_notes():
    data = request.json
    emails = data.get('emails', [])  # Lista zaznaczonych e-maili
    notes = data.get('notes', [])  # Lista zaznaczonych notatek

    print("Odebrane e-maile:", emails)
    print("Odebrane notatki:", notes)

    if not emails or not notes:
        return jsonify({'error': 'Brak wybranych notatek lub odbiorców'}), 400
    invalid_emails = [email for email in emails if not is_valid_email(email)]
    if invalid_emails:
        return jsonify({'error': f'Nieprawidłowe adresy e-mail: {invalid_emails}'}), 400
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    email_username = os.getenv('EMAIL_USERNAME')
    email_password = os.getenv('EMAIL_PASSWORD')

    print("SMTP_SERVER:", smtp_server)
    print("SMTP_PORT:", smtp_port)
    print("EMAIL_USERNAME:", email_username)

    if not smtp_server or not smtp_port or not email_username or not email_password:
        return jsonify({'error': 'Brakuje konfiguracji SMTP w pliku .env'}), 500

    try:
        smtp_port = int(smtp_port)  
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Uruchom TLS
            server.login(email_username, email_password) 

            for email in emails:
                msg = MIMEMultipart()
                msg['From'] = email_username
                msg['To'] = email
                msg['Subject'] = "Wybrane notatki"

                body = "Załączam wybrane notatki jako pliki."
                msg.attach(MIMEText(body, 'plain'))

                for note in notes:
                    file_path = os.path.join(NOTES_FOLDER, f"{note}.docx")
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEApplication(attachment.read(), Name=f"{note}.docx")
                            part['Content-Disposition'] = f'attachment; filename="{note}.docx"'
                            msg.attach(part)
                    else:
                        print(f"Plik {file_path} nie istnieje i nie zostanie dołączony.")

                server.sendmail(email_username, email, msg.as_string())

        return jsonify({'message': 'Notatki wysłane pomyślnie!'}), 200

    except ValueError as ve:
        print("Błąd konfiguracji SMTP:", ve)
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        print("Błąd podczas wysyłania e-maili:", e)
        return jsonify({'error': 'Wystąpił błąd podczas wysyłania e-maili'}), 500



@main.route('/notes/<filename>')
def get_note(filename):
    """
    Pobranie wygenerowanej notatki jako pliku do ściągnięcia.
    """
    try:
        return send_from_directory(NOTES_FOLDER, filename + ".docx", as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404
@main.route("/send_invitations", methods=["POST"])
def send_invitations():
    data = request.json
    recipients = data.get("recipients", [])
    subject = data.get("subject", "Zaproszenie")

    if not recipients:
        return jsonify({"error": "Nie podano odbiorców"}), 400

    try:
        # serwer smtp
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_username = os.getenv('EMAIL_USERNAME')
        email_password = os.getenv('EMAIL_PASSWORD')

        if not smtp_server or not email_username or not email_password:
            return jsonify({"error": "Brakuje konfiguracji SMTP w .env"}), 500
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_username, email_password)

            for recipient in recipients:
                message = f"Subject: {subject}\n\nZapraszamy na wydarzenie!"
                server.sendmail(email_username, recipient, message)

        return jsonify({"message": "Wiadomości wysłane pomyślnie!"}), 200
    except Exception as e:
        return jsonify({"error": f"Błąd podczas wysyłania: {str(e)}"}), 500

# Debug / test
@main.route('/debug/recordings')
def debug_recordings():
    return str(os.listdir(UPLOAD_FOLDER))
