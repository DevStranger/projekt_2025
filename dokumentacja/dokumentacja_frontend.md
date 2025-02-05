# Dokumentacja Frontendu

**Wersja:** 2.0

**Data utworzenia:** 25.I.2025

**Data ostatniej aktualizacji:** 05.02.2025

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

- `logo.ico` – ikona strony (favicon)
- `logoo.png` – logo aplikacji
- `notes.js` – skrypt odpowiedzialny za ładowanie i wyświetlanie listy notatek użytkownika
- `record.js` – skrypt odpowiedzialny za obsługę funkcji nagrywania spotkań
- `styles.css` – główny plik stylów CSS używany w aplikacji
- `styles2.css` – dodatkowy plik CSS dla niektórych stron, takich jak „My Notes” i „My Recordings”
- `stylesEvents.css` – skrypt stylów dedykowany do strony „Events”
- `stylesRecord.css` – skrypt stylów dedykowany do strony „Record”
- `tlo.png` – tło dla aplikacji

### `/templates`
Folder zawierający pliki HTML, które są renderowane przez backend aplikacji:

- `events.html` – strona z listą nadchodzących wydarzeń
- `my_events.html` -  dedykowana strona z integracją Zoom (pokazuje spotkania, umożliwia logowanie i pobieranie listy spotkań, dodatkowo umożliwia pobieranie uczestników i wysyłkę e-maili)
- `my_events2.html` - strona z wydarzeniami Teams, umożliwiająca logowanie do Teams, pobieranie wydarzeń oraz wyświetlanie szczegółów
- `my_google_calendar.html` - strona dedykowana wydarzeniom z Google Calendar, umożliwiająca logowanie oraz pobieranie wydarzeń z kalendarza
- `my_ms_calendar.html` - strona prezentująca wydarzenia z MS Calendar, gdzie użytkownik może zalogować się, pobrać wydarzenia oraz sprawdzić szczegóły
- `index.html` – strona główna aplikacji
- `my_notes.html` – strona z listą notatek użytkownika
- `my_recordings.html` – strona z listą nagrań użytkownika
- `record.html` – strona umożliwiająca nagrywanie spotkania

## Strony

### `index.html`
Strona główna aplikacji, zawierająca przyciski umożliwiające przejście do innych sekcji aplikacji: wydarzeń, nagrywania, notatek oraz nagrań

**Opis funkcji:**
- przyciski prowadzące do poszczególnych sekcji aplikacji
- ładowanie skryptu `notes.js`, który odpowiada za załadowanie listy notatek

---

### `events.html`
Strona wyświetlająca nadchodzące wydarzenia, które są pobierane z backendu (w zmiennej `events`)

**Opis funkcji:**
- lista wydarzeń z datą i tytułem
- jeśli brak jest wydarzeń, wyświetlana jest odpowiednia informacja

---

### `my_events.html`
Strona dedykowana integracji z Zoom

**Opis funkcji:**
- umożliwia logowanie do Zooma poprzez przycisk `„Zaloguj się przez Zoom”`
- po zalogowaniu użytkownik może załadować listę spotkań klikając przycisk `„Załaduj spotkania”`
- lista spotkań wyświetlana jest jako elementy listy z dodatkowymi przyciskami umożliwiającymi pobranie szczegółów
- dodatkowo dostępna jest funkcjonalność wysyłania e-maili do uczestników spotkania

---

### `my_events2.html`
Strona z wydarzeniami Teams

**Opis funkcji:**
- umożliwia logowanie do Microsoft Teams poprzez przycisk `„Zaloguj się w Teams”`
- po zalogowaniu, użytkownik może kliknąć przycisk `„Załaduj wydarzenia”`, aby pobrać i wyświetlić listę wydarzeń
- dla każdego wydarzenia dostępny jest przycisk `„Pokaż uczestników”`, który wyświetla szczegółowe informacje oraz umożliwia wysyłanie wiadomości

---

### `my_google_calendar.html`
Strona integrująca wydarzenia z Google Calendar

**Opis funkcji:**
- zawiera przyciski do logowania w Google: `„Zaloguj się w Google”` oraz pobierania wydarzeń: `„Załaduj wydarzenia”`
- wydarzenia wyświetlane są w formie listy, gdzie każdy element zawiera tytuł, datę rozpoczęcia oraz przycisk `„Szczegóły”`, umożliwiający pobranie dodatkowych informacji (w tym listy uczestników i opcję wysyłania e-maili)

---

### `my_ms_calendar.html`
Strona dedykowana wydarzeniom z MS Calendar

**Opis funkcji:**
- umożliwia logowanie do MS Calendar poprzez przycisk `„Zaloguj się do MS Calendar”`
- po zalogowaniu, użytkownik może kliknąć przycisk `„Załaduj wydarzenia”` aby wyświetlić listę wydarzeń
- dla każdego wydarzenia dostępna jest opcja pobrania szczegółowych informacji, w tym listy uczestników, wyświetlanych po kliknięciu przycisku `„Pokaż szczegóły”`

---

### `my_notes.html`
Strona prezentująca listę notatek użytkownika (notatki są wyświetlane jako linki do pobrania)

**Opis funkcji:**
- dynamiczne ładowanie notatek użytkownika z backendu
- notatki są wyświetlane w formie linków, umożliwiających ich pobranie
- zastosowanie pętli Jinja (`{% for note in notes %}`) do generowania listy notatek na podstawie danych przesłanych z backendu.

---

### `my_recordings.html`
Strona wyświetlająca listę nagrań użytkownika (nagrania są wyświetlane jako linki, a kliknięcie na nie powoduje otwarcie modala z odtwarzaczem wideo)

**Opis funkcji:**
- lista nagrań użytkownika, z możliwością odtwarzania nagrań bezpośrednio w przeglądarce
- modal z odtwarzaczem wideo do wyświetlania wybranego nagrania

---

### `record.html`
Strona umożliwiająca nagrywanie spotkań z wybranego okna - umożliwia użytkownikowi rozpoczęcie nagrywania, zatrzymanie nagrywania oraz zapisanie nagrania

**Opis funkcji:**
- wybór okna do nagrywania za pomocą przycisku „Wybierz okno do nagrywania” (może być też cały ekran)
- możliwość rozpoczęcia i zatrzymania nagrywania przy pomocy przycisków
- wprowadzenie tytułu nagrania przed jego zapisaniem
- wyświetlanie timera nagrywania (czas trwania nagrania)

## JavaScript

### `notes.js`
Skrypt odpowiedzialny za załadowanie i wyświetlanie listy notatek użytkownika

**Opis działania:**
1. po załadowaniu strony (`DOMContentLoaded`) skrypt wykonuje zapytanie do backendu (`/my_notes`), aby pobrać listę dostępnych notatek w formacie JSON
2. notatki są dynamicznie tworzone jako elementy listy HTML, a każdy element jest linkiem umożliwiającym pobranie pliku

---

### `record.js`
Skrypt odpowiedzialny za obsługę nagrywania spotkań

**Opis działania:**
1. umożliwia użytkownikowi wybranie okna do nagrywania za pomocą `navigator.mediaDevices.getDisplayMedia`
2. nagrywanie jest obsługiwane za pomocą `MediaRecorder`, który zapisuje wideo jako plik `.webm`
3. w trakcie nagrywania wyświetlany jest timer pokazujący upływający czas
4. po zakończeniu nagrywania, użytkownik ma możliwość zapisania nagrania poprzez wysłanie pliku na serwer (`/save`)

## Style i formatowanie CSS

### `styles.css`
Główne style aplikacji, zawierające ogólne zasady dotyczące układu, kolorów, fontów oraz responsywności

---

### `styles2.css`
Dodatkowy plik stylów, który jest używany na stronach „My Notes” i „My Recordings” i zawiera specyficzne style dla tych widoków

---

### `stylesEvents.css`
Plik stylów dla strony „Events”, odpowiadający za wygląd listy nadchodzących wydarzeń

---

### `stylesRecord.css`
Plik stylów dla strony „Record”, dostosowujący wygląd interfejsu użytkownika do funkcji nagrywania
