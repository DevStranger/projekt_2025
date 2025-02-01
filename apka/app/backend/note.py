import os
from docx import Document
from whisper import load_model
import torchaudio
from pydub import AudioSegment
from docx.shared import Inches


# Inicjalizacja modelu Whisper
model = load_model("base") #ew "small"

def save_transcription_to_docx(transcription, docx_path, screenshots_folder):
    """
    Zapisuje transkrypcję i screenshoty w pliku .docx.
    """
    doc = Document()

    # Dodaj transkrypcję
    doc.add_paragraph("Transkrypcja wykładu:", style='Heading 1')
    doc.add_paragraph(transcription)

    # Dodaj screenshoty
    doc.add_paragraph("Zrzuty ekranu:", style='Heading 1')
    if os.path.exists(screenshots_folder):
        for screenshot in sorted(os.listdir(screenshots_folder)):
            screenshot_path = os.path.join(screenshots_folder, screenshot)
            doc.add_picture(screenshot_path, width=Inches(5))
    else:
        doc.add_paragraph("Brak zrzutów ekranu.")

    # Zapisz plik docx
    doc.save(docx_path)
    print(f"Zapisano plik .docx: {docx_path}")

# Funkcja do wczytania pliku audio i jego konwersji na WAV (16000 Hz, mono)
def load_and_convert_audio(audio_path):
    file_extension = os.path.splitext(audio_path)[1].lower()

    if file_extension == '.mp3':  # Konwersja MP3 na WAV
        wav_path = audio_path.replace('.mp3', '.wav')
        audio = AudioSegment.from_mp3(audio_path)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio.export(wav_path, format="wav")
        audio_path = wav_path

    signal, sample_rate = torchaudio.load(audio_path)
    if sample_rate != 16000:
        signal = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(signal)
    return signal, 16000

# Funkcja do transkrypcji mowy na tekst
def transcribe_audio(audio_path):
    signal, sample_rate = load_and_convert_audio(audio_path)
    transcription = model.transcribe(audio_path)
    return transcription['text']

# Funkcja do przetwarzania audio i zapisywania transkrypcji
def process_audio_and_save_transcription(audio_folder, docx_folder, screenshots_folder):
    if not os.path.exists(docx_folder):
        os.makedirs(docx_folder)

    for filename in os.listdir(audio_folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):  # Obsługuje pliki audio
            audio_file_path = os.path.join(audio_folder, filename)

            docx_filename = os.path.join(docx_folder, f"{os.path.splitext(filename)[0]}.docx")
            if os.path.exists(docx_filename):
                print(f"Pominięto {filename}, transkrypcja już istnieje.")
                continue  # Pomijamy przetwarzanie, jeśli plik istnieje

            try:
                transcription = transcribe_audio(audio_file_path)
                print(f"Zakończona transkrypcja: {filename}")

                # Nazwa pliku docx na podstawie nazwy pliku audio
                docx_filename = os.path.join(docx_folder, f"{os.path.splitext(filename)[0]}.docx")

                save_transcription_to_docx(transcription, docx_filename, screenshots_folder)
                print(f"Zapisano transkrypcję do: {docx_filename}")

            except Exception as e:
                print(f"Błąd przy przetwarzaniu {filename}: {e}")

if __name__ == "__main__":
    audio_folder = r"recordings"
    docx_folder = os.path.join(os.getcwd(), 'recordings', 'notes')
    screenshots_folder = os.path.join(os.getcwd(), 'recordings', 'screenshots')  # Folder zrzutów ekranu

    if not os.path.exists(docx_folder):
        os.makedirs(docx_folder)

    process_audio_and_save_transcription(audio_folder, docx_folder, screenshots_folder)