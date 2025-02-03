from docx import Document
from flask import Blueprint, Flask, jsonify, render_template, current_app, request, send_from_directory, session, redirect
import requests
from .calendar_integration import get_calendar_events
import pygetwindow as gw
from .recording import record_window, start_recording_thread, stop_recording, save_recording, setup_upload_folder
import os
from werkzeug.utils import secure_filename
from .note import process_audio_and_save_transcription
from .screenshot import extract_screenshots_from_video
import base64
from .teams_integration import get_teams_events


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
from .ms_calendar_integration import (
    get_ms_calendar_authorize_url_ms,
    exchange_code_for_token_ms,
    get_ms_calendar_events_ms,
    get_ms_calendar_event_details_ms
)

from .google_calendar_integration import (
    get_google_authorize_url,
    exchange_code_for_token2,
    get_google_events,
    get_google_event_details
)

from google.oauth2.credentials import Credentials
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = os.getenv("ZOOM_REDIRECT_URI")

ZOOM_CLIENT_ID="FA1BsrIaTHyB5zmz2hukmg"
ZOOM_CLIENT_SECRET="dpQeeLxZBAqFFaEpevt2WmAv1J81jtmJ"
ZOOM_REDIRECT_URI="http://localhost:5000/zoom/callback"

TEAMS_TENANT_ID="40ad34a2-4df4-499f-a628-c865a29a7782"
TEAMS_CLIENT_ID="4aa51599-98de-4a0a-8006-6939d24a18f4"
TEAMS_CLIENT_SECRET="T5l8Q~_mmVp_.qHDlRkUKenBCELcceLYPFnDUcGF"
TEAMS_REDIRECT_URI="https://login.microsoftonline.com/common/oauth2/nativeclient"

def send_batch_email(recipients, subject):
    #do uzupelnienia
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    body = "Treść wiadomości..."
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, recipients, msg.as_string())
    server.connect(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

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

def get_teams_authorize_url():
    """
    Zwraca URL, na który przekierowujesz użytkownika,
    by uzyskać authorization code. W Microsoft v2 endpoint:
    https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
    """
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

main = Blueprint('main', __name__, template_folder="../frontend/templates", static_folder="../frontend/static")


@main.route("/my_events2")
def events_page2():
    return render_template("my_events2.html")

@main.route("/zoom-meetings")
def zoom_meetings():
    try:
        access_token = session.get("zoom_access_token")
        meetings = get_zoom_meetings(access_token)
        return jsonify(meetings)  # np. [{topic, start_time, join_url}, ...]
    except Exception as e:
        print("Błąd w /zoom-events:", e)
        return jsonify({"error": str(e)}), 400
    
@main.route("/zoom/login")
def zoom_login():
    # 1. Generujemy URL autoryzacji
    auth_url = get_zoom_authorize_url()
    # 2. Przekierowujemy usera do Zoom
    return redirect(auth_url)

@main.route("/zoom/callback")
def zoom_callback():
    # Zoom przekazuje "code" i "state" do tego endpointu
    code = request.args.get("code")
    print(code)
    if not code:
        return "Brak parametru 'code' w callbacku", 400

    try:
        token_data = exchange_code_for_token(code)

        # token_data m.in. "access_token" i "refresh_token"
        session["zoom_access_token"] = token_data
        #zoom_token = token_data
        # W realnej aplikacji lepiej trzymać refresh_token i odświeżać, gdy wygaśnie
        return render_template("my_events.html")
    except Exception as e:
        return f"Błąd podczas wymiany code na token: {e}", 400

@main.route("/zoom-events")
def zoom_events():
    # Tu pobieramy spotkania z Zoom dla zalogowanego usera
    access_token = session.get("zoom_access_token")
    if not access_token:
        return jsonify({"error": "Brak access_token – zaloguj się przez /zoom/login"}), 401

    try:
        access_token = session.get("zoom_access_token")
        meetings = get_zoom_meetings(access_token)
        return jsonify(meetings)  # np. [{topic, start_time, join_url}, ...]
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/zoom-personal-meeting")
def zoom_personal_meeting():
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

@main.route("/send_invitations", methods=["POST"])
def send_invitations():
    data = request.json
    recipients = data.get("recipients", [])
    subject = data.get("subject", "Temat wiadomości")

    if not recipients:
        return jsonify({"error": "Brak odbiorców"}), 400

    try:
        send_batch_email(recipients, subject)  # Twoja funkcja SMTP
        return jsonify({"message": "Wiadomości wysłane pomyślnie"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/zoom-meeting-participants")
def zoom_meeting_participants():
    access_token = session.get("zoom_access_token")
    if not access_token:
        return jsonify({"error": "Nie jesteś zalogowany w Zoom."}), 401

    meeting_id = request.args.get("meetingId")
    if not meeting_id:
        return jsonify({"error": "Brak parametru meetingId"}), 400

    try:
        # Tu musisz mieć funkcję get_zoom_participants, np.
        participants = get_zoom_participants(meeting_id, access_token)
        return jsonify(participants)  # np. [{ "user_email": "...", "name": "..." }, ...]
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
        token_json = exchange_code_for_token(code)
        # zapisz access_token do session
        session["teams_access_token"] = token_json["access_token"]
        return "Autoryzacja z Teams zakończona! Możesz pobrać swoje eventy."
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

@main.route("/ms-calendar/login")
def ms_calendar_login():
    # Wygeneruj link do logowania
    auth_url = get_ms_calendar_authorize_url_ms()
    return redirect(auth_url)

@main.route("/ms-calendar/callback")
def ms_calendar_callback():
    code = request.args.get("code")
    if not code:
        return "Brak parametru code w callbacku", 400
    try:
        token_json = exchange_code_for_token(code)
        # zapisz access_token w sesji
        session["ms_calendar_access_token"] = token_json["access_token"]
        return "Zalogowano do MS Calendar! Teraz możesz pobrać wydarzenia."
    except Exception as e:
        return f"Błąd: {e}", 400

@main.route("/ms-calendar/events")
def ms_calendar_events():
    # Pobiera listę wydarzeń
    access_token = session.get("ms_calendar_access_token")
    if not access_token:
        return jsonify({"error": "Brak zalogowania do MS Calendar"}), 401
    try:
        events_list = get_ms_calendar_events_ms(access_token)
        return jsonify(events_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/ms-calendar/event-details")
def ms_calendar_event_details_route():
    # Pobiera szczegóły jednego wydarzenia
    access_token = session.get("ms_calendar_access_token")
    if not access_token:
        return jsonify({"error": "Brak zalogowania do MS Calendar"}), 401

    event_id = request.args.get("eventId")
    if not event_id:
        return jsonify({"error": "Brak parametru eventId"}), 400

    try:
        event_data = get_ms_calendar_event_details_ms(access_token, event_id)
        return jsonify(event_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@main.route("/my_ms_calendar")
def ms_calendar_page():
    return render_template("my_ms_calendar.html")

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
        # Zapisz w session. credentials można serializować do dict:
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
    
    # Odtworzenie obiektu Credentials:
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

    # Odtworzenie obiektu Credentials
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


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/record")
def record():
    return render_template("record.html")

@main.route("/list_windows", methods=["GET"])
def list_windows():
    """Zwróć listę okien."""
    windows = gw.getAllTitles()
    windows = [w for w in windows if w]
    return jsonify(windows)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'recordings')
SCREENSHOT_FOLDER = os.path.join(UPLOAD_FOLDER, 'screenshots')
ALLOWED_EXTENSIONS = {'webm', 'mp4', 'avi'}

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
    """Zapisz nagranie i przekonwertuj na MP4."""
    try:
        file = request.files['file']
        title = request.form.get('title', 'recording')
        mp4_path, wav_path = save_recording(file, title)

        screenshots_folder = os.path.join(SCREENSHOT_FOLDER, title)
        os.makedirs(screenshots_folder, exist_ok=True)

        extract_screenshots_from_video(mp4_path, screenshots_folder, fps=1)  

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
        return send_from_directory(UPLOAD_FOLDER, filename+".mp4")
    except FileNotFoundError:
        return "File not found", 404

@main.route('/my_notes')
def show_notes():
    docx_folder = os.path.join(os.getcwd(), 'recordings', 'notes')  # Upewnij się, że folder istnieje w 'recordings/notes'
    if not os.path.exists(docx_folder):
        return render_template('my_notes.html', notes=[])

    # Pobierz pliki `.docx` z folderu
    notes = [f for f in os.listdir(docx_folder) if f.endswith('.docx')]
    notes = [os.path.splitext(file)[0] for file in notes]
    return render_template('my_notes.html', notes=notes)

@main.route('/debug/recordings')
def debug_recordings():
    return str(os.listdir(UPLOAD_FOLDER))


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

        return jsonify({'message': f"Transkrypcja wygenerowana dla {title}.wav!",
                        'path': os.path.join(notes_folder, f"{title}.docx")})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Nieoczekiwany błąd.', 'details': str(e)}), 500


@main.route('/notes/<filename>')
def get_note(filename):
    docx_folder = os.path.join(os.getcwd(), 'recordings', 'notes')
    try:
        return send_from_directory(docx_folder, filename + ".docx", as_attachment=True)  # Pobierz plik jako załącznik
    except FileNotFoundError:
        return "File not found", 404


@main.route('/search_docx')
def search_in_docx(file_path, query):
    try:
        doc = Document(file_path)
        has_text = False  # Flag to check if the document contains any text

        for para in doc.paragraphs:
            if para.text.strip():  # Check if the paragraph has non-whitespace text
                has_text = True
                if query in para.text.lower():
                    return True

        # If no text was found in the document
        if not has_text:
            print(f"The file '{file_path}' is empty or contains only images.")
            return False

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return False

def search_docx():
    query = request.args.get('query', '').lower()
    matching_files = []

    NOTES_DIR = os.path.join(os.getcwd(), 'recordings', 'notes')

    for filename in os.listdir(NOTES_DIR):
        if filename.endswith('.docx'):
            file_path = os.path.join(NOTES_DIR, filename)
            if search_in_docx(file_path, query):
                print(f"Searching for match: match found in file: {filename}")
                matching_files.append(filename)
    return jsonify(matching_files)


@main.route("/my_events")
def events_page():
    return render_template("my_events.html")

if __name__ == "__main__":
    main.run(debug=True)
