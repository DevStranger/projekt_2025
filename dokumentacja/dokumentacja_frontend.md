# Dokumentacja Frontendu

**Wersja:** 1.0

**Data utworzenia:** 25.I.2025

## Zastosowane technologie

### 1. HTML

- podstawowa technologia wykorzystywana do strukturyzowania stron aplikacji
- w naszym projekcie służy do tworzenia struktury dokumentów, takich jak formularze, nagłówki, listy i linki
- każda strona aplikacji (np. `index.html`, `my_notes.html`) jest zbudowana przy użyciu semantycznych elementów HTML, co zapewnia lepszą dostępność, poprawność SEO oraz bardziej przejrzysty kod

### 2. CSS

- do stylizacji aplikacji użyłyśmy CSS, który odpowiada za wygląd strony, w tym kolory, czcionki, rozmieszczenie elementów i ogólny układ
- pliki CSS są załadowane z folderu `/static` i stosowane na różnych stronach aplikacji, np. `styles.css`, `stylesRecord.css` czy `stylesEvents.css`
- w plikach `styles.css`, `stylesRecord.css` i innych zaimplementowałyśmy style dla przycisków, okien dialogowych (np. modalnych), formularzy oraz elementów dynamicznych, jak timer czy lista notatek
- w projekcie zastosowałyśmy technologię Flexbox i Grid do układania elementów w responsywny sposób

### JavaScript

- jest kluczowym elementem aplikacji, zapewniającym interaktywność i dynamiczne ładowanie treści
- odpowiada m.in. za:
    - obsługę interakcji użytkownika, jak kliknięcie przycisków (np. przycisk „Nagrywaj spotkanie” w `index.html`)
    - dynamiczne ładowanie danych, takich jak lista notatek (w `notes.js`), które są pobierane asynchronicznie z serwera
    - implementację funkcjonalności nagrywania wideo, które są realizowane za pomocą MediaRecorder API w pliku `record.js`
    - obsługę powiadomień o stanie aplikacji, takich jak rozpoczęcie nagrywania wideo lub zapisanie pliku
- w pliku `notes.js` zrealizowana jest funkcjonalność ładowania notatek użytkownika za pomocą funkcji fetch() i wyświetlanie ich w dynamicznie generowanej liście

### Fetch API

- jest używane do asynchronicznego pobierania danych z serwera i przesyłania ich do aplikacji bez konieczności przeładowywania strony
- odpowiada m.in. za ładowanie listy notatek z serwera (`notes.js`) oraz wysyłanie nagrań wideo na serwer (funkcja saveRecording w `record.js`)

### MediaRecorder API

- jest wykorzystywane do nagrywania obrazu i dźwięku z ekranu użytkownika, co pozwala na tworzenie nagrań wideo
- w pliku `record.js` nagrywanie ekranu i dźwięku jest realizowane przez obiekt MediaRecorder, który zapisuje dane wideo w czasie rzeczywistym --> gdy użytkownik zatrzymuje nagrywanie, plik jest zapisywany jako blob i przekazywany do funkcji saveRecording w celu zapisania na serwerze


## Struktura folderów i plików

Aplikacja jest zorganizowana w sposób umożliwiający łatwe zarządzanie plikami i ich podział na kategorie. Poniżej przedstawiamy szczegółowy opis folderów i plików:

### `/static`
Folder zawierający zasoby statyczne, takie jak obrazy, pliki CSS i JavaScript, które są wykorzystywane przez strony HTML:

- `logo.ico` – Ikona strony (favicon).
- `logoo.png` – Logo aplikacji.
- `notes.js` – Skrypt odpowiedzialny za ładowanie i wyświetlanie listy notatek użytkownika.
- `record.js` – Skrypt odpowiedzialny za obsługę funkcji nagrywania spotkań.
- `styles.css` – Główny plik stylów CSS używany w aplikacji.
- `styles2.css` – Dodatkowy plik CSS dla niektórych stron, takich jak „My Notes” i „My Recordings”.
- `stylesEvents.css` – Skrypt stylów dedykowany do strony „Events”.
- `stylesRecord.css` – Skrypt stylów dedykowany do strony „Record”.
- `tlo.png` – Tło dla aplikacji.

### `/templates`
Folder zawierający pliki HTML, które są renderowane przez backend aplikacji:

- `events.html` – Strona z listą nadchodzących wydarzeń.
- `index.html` – Strona główna aplikacji.
- `my_notes.html` – Strona z listą notatek użytkownika.
- `my_recordings.html` – Strona z listą nagrań użytkownika.
- `record.html` – Strona umożliwiająca nagrywanie spotkania.

## Strony


## JavaScript


## Style i formatowanie CSS
