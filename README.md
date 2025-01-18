# Aplikacja do Sporządzania Notatek ze Spotkań

Aplikacja umożliwia nagrywanie spotkań, tworzenie z nich notatek oraz informowanie nieobecnych uczestników o ich przebiegu.

## Wymagania

Przed uruchomieniem aplikacji należy zainstalować wymagane zależności oraz skonfigurować środowisko. Szczegóły poniżej.

### Instalacja zależności

1. **Z katalogu projekt_2025/apka i projekt_2025/apka/app**, uruchom następujące polecenia w terminalu:

   ```bash
   pip install -r requirements.txt
   ```

2. **Zainstaluj FFmpeg (Essentials Build):**
   
   Przejdź do katalogu `/app` i wykonaj polecenie:

   ```bash
   winget install "FFmpeg (Essentials Build)"
   ```

   Po zakończeniu instalacji zamknij i ponownie otwórz terminal. Przejdź do katalogu `/app` i wpisz:

   ```bash
   ffmpeg
   ```

   Jeśli pojawią się informacje o rozszerzeniu FFmpeg, oznacza to, że instalacja przebiegła pomyślnie.

### Możliwy błąd z FFmpeg

W niektórych przypadkach ścieżka do FFmpeg może wymagać ręcznej modyfikacji. Jeśli napotkasz problemy z uruchomieniem, otwórz plik `recording.py` znajdujący się w folderze `backend` i zmodyfikuj linię 67:

Z:

```python
'ffmpeg'
```

Na:

```python
'ffmpeg/bin/ffmpeg'
```

## Uruchamianie aplikacji

1. Z katalogu proejkt_2025/apka/app uruchom aplikację poleceniem:

   ```bash
   python -m main
   ```

2. Aplikacja powinna uruchomić się i być gotowa do użycia.

## Funkcjonalności aplikacji

- **Nagrywanie spotkań:** Możliwość rejestrowania audio.
- **Tworzenie notatek:** Generowanie notatek na podstawie nagranych materiałów.

## Uwagi

- Upewnij się, że wszystkie wymagania zostały poprawnie zainstalowane
- W razie problemów z FFmpeg, sprawdź ścieżkę i upewnij się, że jest poprawna

---
