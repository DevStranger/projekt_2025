import torch
from whisper import load_model
import torchaudio
import os
from pydub import AudioSegment

# Inicjalizacja modelu
model = load_model("base")  # Model Whisper

def load_and_convert_audio(audio_path):
    """Funkcja wczytująca plik audio, konwertując go na WAV (16000 Hz, mono), jeśli jest to plik MP3"""
    file_extension = os.path.splitext(audio_path)[1].lower()

    # Jeśli plik jest MP3, konwertujemy go do WAV
    if file_extension == '.mp3':
        wav_path = audio_path.replace('.mp3', '.wav')
        audio = AudioSegment.from_mp3(audio_path)
        audio = audio.set_frame_rate(16000)  # Ustawienie częstotliwości próbkowania na 16000
        audio = audio.set_channels(1)  # Ustawienie liczby kanałów na 1 (mono)
        audio.export(wav_path, format="wav")
        audio_path = wav_path  # Ustawiamy ścieżkę na nowo skonwertowany plik WAV

    signal, sample_rate = torchaudio.load(audio_path)
    # Jeśli wymagana jest zmiana częstotliwości próbkowania
    if sample_rate != 16000:
        signal = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(signal)
    return signal, 16000

def transcribe_audio(audio_path):
    """Funkcja do transkrypcji mowy na tekst"""
    signal, sample_rate = load_and_convert_audio(audio_path)
    transcription = model.transcribe(audio_path)
    return transcription

def process_audio(audio_path):
    """Główna funkcja przetwarzająca plik audio"""
    transcription = transcribe_audio(audio_path)
    return transcription

if __name__ == "__main__":
    audio_file = r"audio_files\test2.mp3"  # ścieżka do pliku audio
    try:
        transcription = process_audio(audio_file)
        print("Transkrypcja:", transcription)
    except Exception as e:
        print(f"Błąd: {e}")
