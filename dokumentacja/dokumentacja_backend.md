# Dokumentacja Backendu

**Wersja:** 3.0

**Data utworzenia:** 2025-01-25 T09:37:24Z

**Data ostatniej aktualizacji:** 2025-02-05 T19:33:17Z

## Zastosowane technologie

### 1. Flask

- lekki framework do budowy aplikacji webowych w Pythonie
- w naszym projekcie służy do obsługi backendu aplikacji, który pełni funkcje związane z obsługą żądań HTTP oraz renderowaniem szablonów HTML
- jest wykorzystywany do stworzenia głównego serwera aplikacji, który obsługuje różnorodne trasy, takie jak `/record`, `/events`, `/save` czy `/my_recordings`
- umożliwia również obsługę plików nagrań użytkownika, zapisując je w określonym folderze na serwerze
- w pliku `routes.py` znajdują się definicje tras, które odpowiadają za logikę związana z nagrywaniem, zapisywaniem i pobieraniem nagrań, generowaniem notatek oraz integracją z kalendarzem

### 2. Python

- główny język programowania backendu aplikacji, który zapewnia logikę przetwarzania danych oraz współpracuje z innymi technologiami
- został użyty do napisania całej logiki aplikacji backendowej, w tym m.in.:
    - obsługi przesyłania i zapisywania plików audio i wideo (w tym konwersji plików z formatu `webm` na `wav` oraz `mp4`)
    - obsługi transkrypcji mowy na tekst przy pomocy modelu Whisper (generowanie notatek)
    - integracji z Google Calendar API, które umożliwia pobieranie wydarzeń z kalendarza użytkownika
    - operacji na plikach, takich jak zapisywanie transkrypcji do plików `.docx` oraz przetwarzanie nagrań w formatach audio i wideo
    - zarządzania wątkami do nagrywania oraz przetwarzania danych audio w sposób asynchroniczny

### 3. Google Calendar API

- pozwala na integrację z kalendarzem Google, umożliwiając dostęp do wydarzeń z konta użytkownika
- w pliku `calendar_integration.py` zaimplementowano logikę do integracji z Google Calendar, umożliwiającą pobieranie nadchodzących wydarzeń
- wykorzystujemy odpowiednie poświadczenia (plik `credentials.json`) oraz tokeny autoryzacyjne zapisane w pliku `token.json`, aby uzyskać dostęp do kalendarza użytkownika
- dostępne jest również wywołanie trasy `/events`, która zwraca listę nadchodzących wydarzeń w formacie JSON oraz wyświetla je na stronie dla części frontendowej

### 4. Whisper

- model sztucznej inteligencji opracowany przez OpenAI, służący do transkrypcji mowy na tekst
- wykorzystuje najnowsze osiągnięcia w dziedzinie rozpoznawania mowy i jest w stanie zamienić mowę na tekst w różnych językach, w tym również po polsku
- jest załadowany w pliku `note.py` i wykorzystywany do transkrypcji plików audio, które są przesyłane do aplikacji

### 5. FFmpeg

- narzędzie do konwersji, edycji i streamingu plików audio i wideo
- wykorzystywane do konwersji nagrań z formatu `webm` na `wav` oraz na `mp4` w pliku `recording.py` (funkcja `save_recording()`)

### 6. PyDub i torchaudio

- biblioteki do przetwarzania dźwięku w Pythonie
- PyDub oferuje prostą obsługę formatów audio oraz możliwość ich konwersji, podczas gdy torchaudio zapewnia zaawansowane narzędzia do obróbki sygnałów audio
- **_PyDub_** jest wykorzystywana do konwersji plików audio z formatu mp3 na wav o ustalonej częstotliwości próbkowania i mono
- **_torchaudio_** jest używane do załadowania pliku audio do formy tensorów, co jest niezbędne do przetwarzania przez model `Whisper`

### 7. PyGetWindow

- biblioteka, która umożliwia interakcję z oknami aplikacji na systemach Windows i macOS
- pozwala nam uzyskać listę otwartych okien na systemie operacyjnym
- w naszym projekcie jest używana do pobierania listy wszystkich dostępnych okien na systemie operacyjnym za pomocą funkcji `gw.getAllTitles()`
- trasa `/list_windows` w `routes.py` wykorzystuje tę funkcjonalność, aby zwrócić użytkownikowi listę dostępnych okien do nagrywania, co umożliwia nagrywanie konkretnego okna na komputerze

## Struktura folderów i plików

- **`__init__.py`**  
  Inicjalizuje aplikację Flask, definiuje foldery dla statycznych plików i szablonów oraz rejestruje blueprinty - jest to główny plik, który uruchamia aplikację z backendu

- **`calendar_integration.py`**  
  Implementacja integracji z Google Calendar API - odpowiada za pobieranie nadchodzących wydarzeń z kalendarza użytkownika, umożliwiając ich wyświetlanie w aplikacji

- **`config.py`**  
  Pusty plik konfiguracyjny, który może zostać rozszerzony o ustawienia aplikacji, takie jak klucze API, konfiguracja bazy danych itd. 

- **`credentials.json`, `credentials_2.json`, `credentialsstare.json`**  
  Pliki z danymi uwierzytelniającymi dla Google API, umożliwiające dostęp do kalendarza użytkownika - każdy z tych plików może być używany w różnych konfiguracjach uwierzytelniania lub środowiskach

- **`note.py`**  
  Zawiera funkcje do transkrypcji plików audio na tekst za pomocą modelu Whisper - dodatkowo obsługuje zapisywanie transkrypcji do plików w formacie DOCX

- **`recording.py`**  
  Odpowiada za obsługę nagrywania okien systemowych, konwersję plików i przetwarzanie nagrań audio - używa narzędzi takich jak FFmpeg i PyDub do manipulacji plikami audio oraz wideo.

- **`routes.py`**  
  Definiuje trasy Flask, które odpowiadają za różne endpointy API, takie jak nagrywanie, generowanie notatek czy pobieranie plików z serwera

- **`test_routes.py`**  
  Plik zawierający testy jednostkowe do sprawdzania poprawności działania endpointów backendu - służy do zapewnienia jakości aplikacji, testując, czy odpowiedzi API są zgodne z oczekiwaniami

- **`screenshot.py`**
  Służy do generowania zrzutów ekranu z nagrań oraz wykrywania unikalnych klatek (tj. różnych slajdó), które dodawne są do notatek ze spotkania. Dzięki analizie obrazów obsługuje przycinanie obrazów do obszaru samej prezentacji i usuwanie duplikatów

- **`summary.py`**
  Ten plik odpowiada za automatyczne generowanie podsumowań treści plików w formacie `.docx`. Wykorzystuje model podsumowywania dostępny w bibliotece Transformers, aby przekształcić długie treści w skrócone wersje, zachowując istotne informacje

- **`teams_integration.py`**
  Plik, który umożliwia integrację z Microsoft Teams, co pozwala na pobieranie danych dotyczących wydarzeń kalendarza. Używa mechanizmu OAuth 2.0 do autoryzacji i wymiany kodu autoryzacyjnego na token dostępu

- **`zoom_integration.py`**
  Ten plik zapewnia integrację z platformą Zoom, umożliwiającą dostęp do danych o spotkaniach, szczegółach spotkań oraz uczestnikach. Podobnie jak w przypadku integracji z innymi platformami, wykorzystywany jest mechanizm OAuth 2.0.

- **`token.json`**  
  Plik zawierający tokeny uwierzytelniające, które pozwalają na autoryzację aplikacji do uzyskania dostępu do Google Calendar API

- **`/__pycache__`**  
  Folder generowany automatycznie przez Pythona, zawierający skompilowane pliki `.pyc` - są one tworzone w celu przyspieszenia ładowania aplikacji w przyszłości

## Funkcjonalności

### Proces rejestrowania i przetwarzania nagrania

#### Nagrywanie okna aplikacji

1. **Użycie biblioteki pygetwindow**  
   Aplikacja wykorzystuje bibliotekę `pygetwindow`, która umożliwia pobranie tytułów dostępnych okien na komputerze. Po podaniu tytułu okna, aplikacja uruchamia wątek odpowiedzialny za rejestrowanie aktywności w tym oknie.

2. **Format zapisanego nagrania**  
   Nagranie okna aplikacji jest zapisywane jako plik wideo w formacie `.webm`

#### Konwersja pliku

Po zapisaniu pliku wideo, aplikacja automatycznie konwertuje go na następujące formaty:
- **Audio** – format `.wav`
- **Wideo** – format `.mp4`

Do konwersji wykorzystywane jest narzędzie `FFmpeg`.

#### Przechowywanie plików

Wszystkie pliki (audio, wideo) oraz transkrypcje są przechowywane w folderze `recordings`

### Proces generowania notatek

#### Transkrypcja mowy na tekst

1. **Przekazywanie plików audio**  
   Pliki audio w formatach `.mp4` są przekazywane do funkcji `transcribe_audio`, która wykorzystuje model `Whisper` do przetwarzania mowy na tekst

2. **Zapis transkrypcji**  
   Transkrypcja mowy na tekst jest zapisywana w formacie `.docx` przy użyciu biblioteki `python-docx`

#### Automatyczne przetwarzanie wszystkich nagrań

Funkcja `process_audio_and_save_transcription` przetwarza wszystkie pliki audio znajdujące się w folderze `recordings`, generując odpowiednie notatki dla każdego pliku

#### Dodawanie zrzutów ekranu z prezentacją
Po zakończeniu nagrywania, proces generowania notatek przechodzi do automatycznego pobierania zrzutów ekranu z nagrania wideo:

1. **Ekstrakcja zrzutów ekranu**
    Funkcja `extract_screenshots_from_video` wykorzystuje narzędzie FFmpeg do wyodrębnienia zrzutów ekranu z pliku wideo w regularnych odstępach czasu (domyślnie 10 klatek na sekundę)

2. **Wykrywanie obszaru prezentacji**
    Po wygenerowaniu zrzutów ekranowych, funkcja `detect_presentation_area` analizuje każdy obraz, wykrywając największy kontur charakteryzujący się jasnym tłem (często występującym przy prezentacjach). Obszar ten zostaje przycięty, co poprawia jakość prezentowanych zrzutów i nie zajmują one niepotrzebnie nadmiarowo dużo miejsca w notatkach

3. **Eliminacja duplikatów**
    Aby uniknąć przechowywania wielu identycznych klatek, funkcja `is_duplicate_image` porównuje kolejne zrzuty ekranu (na podstawie `perceptual hash`) i usuwa duplikaty. Dzięki temu w folderze docelowym pozostają tylko unikalne zrzuty, które najlepiej reprezentują przebieg prezentacji

#### Tworzenie podsumowań treści
Moduł `summary.py` odpowiada za generowanie streszczeń z treści wygenerowanych notatek (plików `.docx` z transkrypcjami). Proces tworzenia podsumowań przebiega według następujących kroków:

1. **Podział tekstu na segmenty**
    Funkcja `split_text` dzieli długi tekst na mniejsze fragmenty (segmenty), co jest niezbędne dla efektywnego przetwarzania przez model podsumowujący. Dzięki temu model nie jest przeciążony nadmierną ilością danych na raz

2. **Generowanie podsumowania segmentów**
    Dla każdego segmentu tekstu wykorzystywany jest model podsumowujący, który generuje skróconą wersję treści. W przypadku błędów lub pustych segmentów, system odpowiednio je pomija

3. **Łączenie segmentów**
    Wygenerowane fragmenty podsumowania są łączone w jeden spójny dokument. Efekt końcowy zapisywany jest w pliku `.docx`, który stanowi zbiorcze podsumowanie treści transkrypcji

#### Przechowywanie plików z notatkami

Po wykonaniu transkrypcji mowy na tekst, wygenerowane pliki notatek w formacie .docx są przechowywane w folderzez `\recordings\notes`

## Interfejs użytkownika (UI)

### Strona główna (index.html)
Strona główna jest wejściem do aplikacji, na której użytkownik może:
- wejść na podstronę i rozpocząć nagrywanie
- wejść na pdostronę 'Moje notatki' lub 'Moje nagrania'
- wyświetlać wydarzenia z kalendarza

W przypadku przycisków do rozpoczęcia nagrywania lub wyświetlania kalendarza, frontend wysyła zapytania HTTP do backendu, który obsługuje te operacje. Flask dostarcza dane do strony za pomocą odpowiednich tras, np.:
- `/start_recording`
- `/get_events`

Backend zwraca dane w formacie JSON lub renderuje odpowiednie strony HTML.

### Nagrywanie (record.html)
Na tej stronie użytkownik ma możliwość:
- rozpoczęcia nagrywania
- zakończenia nagrywania okna aplikacji

Kiedy użytkownik naciśnie przycisk do rozpoczęcia nagrywania, frontend wysyła zapytanie do backendu (Flask), który uruchamia odpowiednią funkcję do nagrywania. Funkcje te są zawarte w pliku `recording.py`. Nagrania są następnie przesyłane do backendu w celu zapisania w folderze `recordings`.

Frontend (HTML) używa JavaScript do interakcji z backendem w sposób asynchroniczny, aby uzyskać odpowiedzi o stanie nagrywania bez przeładowania strony.

### Wydarzenia kalendarza (events.html)
Strona ta wyświetla nadchodzące wydarzenia z Google Calendar. Backend aplikacji, używając `calendar_integration.py`, integruje się z Google Calendar API, pobierając dane o wydarzeniach z konta użytkownika.

Strona `events.html` w frontendzie wyświetla te wydarzenia, a zapytania do backendu są realizowane przez Flask w trasie:
- `/get_calendar_events`

Po załadowaniu strony frontend wykonuje zapytanie GET do backendu, który zwraca dane o wydarzeniach w formacie JSON. JavaScript renderuje te dane w odpowiednim formacie na stronie.

### Notatki (my_notes.html)
Użytkownicy mogą przeglądać swoje wygenerowane transkrypcje notatek w formacie `.docx`. Backend aplikacji przechowuje te pliki w odpowiednim katalogu (`/recordings/notes`), a Flask udostępnia je użytkownikom za pomocą odpowiednich tras:
- `/get_note/<note_id>`

Strona `my_notes.html` w frontendzie prezentuje listę dostępnych notatek, wraz z ich rozmiarem, a użytkownik może pobrać je, klikając na odpowiedni link oraz wysłać do wybranych przez siebie osób. Backend obsługuje żądanie i zwraca odpowiedni plik `.docx` oraz wysyła e-mail (gmail) z wybraną notatką jako załącznik.

### Nagrania (my_recordings.html)
Użytkownicy mogą przeglądać swoje zapisane nagrania wideo i pobierać je. Pliki nagrań są przechowywane na serwerze w folderze `./recordings/` i mogą być dostępne z poziomu aplikacji webowej za pośrednictwem odpowiednich tras Flask:
- `/get_recording/<recording_id>`

Frontend (strona `my_recordings.html`) prezentuje listę dostępnych nagrań, które są powiązane z użytkownikiem. Kliknięcie na nazwę pliku powoduje uruchmienie odtwarzacza nagrania.

### Zrzuty ekranu (screenshots.py)

#### Obliczanie hashy obrazów:

- `calculate_image_hash(image_path)` – oblicza perceptual hash (średnia wartość hash) dla obrazu, co umożliwia porównywanie podobieństwa pomiędzy obrazami

#### Detekcja duplikatów:

- `is_duplicate_image(new_image_path, last_image_path)` – porównuje hash dwóch obrazów, aby ustalić, czy nowy zrzut ekranu jest duplikatem poprzedniego

#### Wykrywanie obszaru prezentacji:

- `detect_presentation_area(image_path)` – analizuje obraz w celu wykrycia obszaru, który najczęściej charakteryzuje się jasnym tłem (np. prezentacja) i przycina obraz do tego obszaru

#### Generowanie zrzutów ekranu z wideo:

- `extract_screenshots_from_video(video_path, output_folder, fps=10)` – wykorzystuje FFmpeg do wyodrębniania zrzutów ekranu z nagrania wideo w regularnych odstępach czasu, a następnie usuwa duplikaty uzyskane na podstawie porównania hashy obrazów

### Podsumowanie notatek (summary.py)

#### Podział tekstu na segmenty:

- `split_text(text, max_length=1000)` – dzieli długi tekst na mniejsze fragmenty, dzięki czemu model podsumowujący może efektywniej przetworzyć całość treści

#### Generowanie podsumowania:

- `generate_summary(docx_path, summary_docx_path)` – wczytuje treść z pliku DOCX, ekstraktuje fragmenty (np. wyodrębniając tekst znajdujący się pomiędzy znacznikami „Transkrypcja wykładu:” a „Zrzuty ekranu:” jeśli występują), dzieli tekst na segmenty, przetwarza je modelem podsumowującym, a następnie zapisuje wynik do pliku `.docx`

## Bezpieczeństwo

### Dane uwierzytelniające (Google API)
Dane uwierzytelniające do Google API są przechowywane w plikach `credentials.json` oraz `token.json`. Te pliki umożliwiają aplikacji dostęp do konta Google użytkownika, jednak są chronione przed publicznym dostępem. 

### Walidacja przesyłanych plików  
Aplikacja zapewnia walidację plików przesyłanych przez użytkownika. Akceptowane są tylko określone rozszerzenia plików, takie jak:
   - `.webm`
   - `.mp4`
   - `.avi`

### Ochrona danych wrażliwych
W celu ochrony danych wrażliwych, aplikacja stosuje odpowiednie mechanizmy autoryzacji oraz kontroluje dostęp do zasobów. Na przykład:
   - Generowanie notatek jest możliwe tylko na podstawie przesłanych plików audio, zapewniając, że dostęp do transkrypcji i danych mają tylko uprawnieni użytkownicy

## Autorzy i kontakt
- Aleksandra Adamiak (aadamiak@student.agh.edu.pl)
- Maja Chlipała (majachlipala@student.agh.edu.pl)
- Joanna Furtak (joannafurtak@student.agh.edu.pl)
- Julia Mikrut (mikrut@student.agh.edu.pl)

---

| ![logoo](https://github.com/user-attachments/assets/4b34cc5f-8992-45bb-b354-4a69a66a5189) | **Zespół NoteWriter Girls Inc.** | **👑 Ola 🐝 Maja 🐝 Asia 🐝 Julka** |
|:--:|:--:|:--:|
