# Dokumentacja Backendu

**Wersja:** 1.0

**Data utworzenia:** 25.I.2025

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

- **`token.json`**  
  Plik zawierający tokeny uwierzytelniające, które pozwalają na autoryzację aplikacji do uzyskania dostępu do Google Calendar API

- **`/__pycache__`**  
  Folder generowany automatycznie przez Pythona, zawierający skompilowane pliki `.pyc` - są one tworzone w celu przyspieszenia ładowania aplikacji w przyszłości

## Funkcjonalności


## Proces rejestrowania i przetwarzania nagrania


## Proces generowania notatek


## Interfejs użytkownika (UI)


## Integracje


## Logowanie i alerty


## Bezpieczeństwo

