# API endpoints

## `/`

### Opis
Renderuje stronę główną

### Metoda

`GET`

## `/record`

### Opis
Renderuje podstronę do nagrywania

### Metoda

`GET`

## `/record/record_window`

### Opis
Rozpoczyna nagrywanie wybranego okna aplikacji w osobnym wątku

### Metoda
`POST`

### Nagłówki
- `Content-Type: application/json`

### Body (JSON)
| Pole           | Typ     | Wymagane | Opis                                     |
|----------------|---------|----------|------------------------------------------|
| `window_title` | string  | Tak      | Tytuł okna, które ma być nagrywane.      |

#### Przykład zapytania
```json
{
  "window_title": "Mój Dokument - Microsoft Word"
}
```

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Rozpoczęto nagrywanie okna: Mój Dokument - Microsoft Word"
}
```

**_Błąd (400 Bad Request)_**

Jeśli nie podano `window_title`:

```json
{
  "message": "Nie podano tytułu okna."
}
```

## `/record/stop_recording`

### Opis
Zatrzymuje aktualnie trwające nagrywanie

### Metoda
`POST`

### Nagłówki
- brak wymaganych nagłówków

#### Przykład zapytania
- brak danych w treści zapytania

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Nagrywanie zakończone pomyślnie."
}
```

**_Błąd (500 Internal Server Error)_**

W przypadku nieoczekiwanego błędu:

```json
{
  "message": "Błąd podczas zatrzymywania nagrywania: <szczegóły>"
}
```

## `/record/save`

### Opis
Zapisuje nagranie przesłane jako plik i konwertuje je na format `mp4` - dodatkowo wyzwala generowanie transkrypcji w formacie `.docx`

### Metoda

`POST`

### Nagłówki

- `Content-Type: multipart/form-data`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                                                                        |
|----------------|---------|----------|-----------------------------------------------------------------------------|
| `file`         | file    | Tak      | Nagranie video do zapisania (format: `.webm`)                               |
| `title`        | string  | Nie      | Opcjonalna nazwa pliku - jeśli nie podano, używana jest bieżąca data i czas |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Strona HTML z komunikatem: "Nagranie zapisane!".
```

**_Błąd (400 Bad Request)_**

Jeśli brak pliku:

```json
{
  "error": "Nie przekazano żadnego pliku!"
}
```

**_Błąd (500 Internal Server Error)_**

W przypadku błędu konwersji:

```json
{
  "error": "Konwersja do MP4 nie powiodła się."
}
```

## `/my_recordings`

### Opis

Zwraca listę zapisanych nagrań `mp4`

### Metoda

`GET`

### Nagłówki

- brak wymaganych nagłówków

#### Przykład zapytania

- brak danych w treści zapytania

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Strona HTML z listą nagrań wideo.
```

## `/events`

### Opis

Pobiera wydarzenia z Google Calendar

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista wydarzeń
```

**_500 Internal Server Error_**

-  jeśli wystąpi błąd podczas pobierania wydarzeń

## `/list_windows`

### Opis

Zwraca listę nazw wszystkich otwartych okien

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista tytułów okien
```

## `/generate_notes`

### Opis

Generuje transkrypcję tekstową z istniejącego pliku `.wav`

### Metoda

`POST`

### Nagłówki

- `Content-Type: application/x-www-form-urlencoded`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                                                      |
|----------------|---------|----------|-----------------------------------------------------------|
| `title`        | string  | Tak      | Nazwa pliku `.wav` (bez rozszerzenia) do przetworzenia    |

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Transkrypcja wygenerowana pomyślnie."
}
```

**_Błąd (400 Bad Request)_**

Jeśli brak nazwy pliku:

```json
{
  "error": "Brak nazwy pliku! Podaj tytuł pliku WAV."
}
```

**_Błąd (404 Not Found)_**

Jeśli plik `.wav` nie istnieje:

```json
{
  "error": "Plik moje_nagranie.wav nie istnieje w katalogu recordings!"
}
```

## `/my_notes`

### Opis

Wyświetla listę wygenerowanych notatek `.docx`

### Metoda

`GEt`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista notatek w formie HTML
```
=======
# API endpoints

**Wersja:** 2.2

**Data utworzenia:** 2025-01-25 T09:12:31Z

**Data ostatniej aktualizacji:** 2025-02-05 T19:49:28Z

## `/`

### Opis
- renderuje stronę główną

### Metoda

`GET`

## `/record`

### Opis
- renderuje podstronę do nagrywania

### Metoda

`GET`

## `/record/record_window`

### Opis
- rozpoczyna nagrywanie wybranego okna w osobnym wątku

### Metoda
`POST`

### Nagłówki
- `Content-Type: application/json`

### Body (JSON)
| Pole           | Typ     | Wymagane | Opis                                     |
|----------------|---------|----------|------------------------------------------|
| `window_title` | string  | Tak      | Tytuł okna, które ma być nagrywane.      |

#### Przykład zapytania
```json
{
  "window_title": "Mój Dokument - Microsoft Word"
}
```

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Rozpoczęto nagrywanie okna: Mój Dokument - Microsoft Word"
}
```

**_Błąd (400 Bad Request)_**

Jeśli nie podano `window_title`:

```json
{
  "message": "Nie podano tytułu okna."
}
```

## `/record/stop_recording`

### Opis
- zatrzymuje aktualnie trwające nagrywanie

### Metoda
`POST`

### Nagłówki
- brak wymaganych nagłówków

#### Przykład zapytania
- brak danych w treści zapytania

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Nagrywanie zakończone pomyślnie."
}
```

**_Błąd (500 Internal Server Error)_**

W przypadku nieoczekiwanego błędu:

```json
{
  "message": "Błąd podczas zatrzymywania nagrywania: <szczegóły>"
}
```

## `/record/save`

### Opis
- zapisuje nagranie przesłane jako plik i konwertuje je na format `mp4` - dodatkowo wyzwala generowanie transkrypcji w formacie `.docx`

### Metoda

`POST`

### Nagłówki

- `Content-Type: multipart/form-data`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                                                                        |
|----------------|---------|----------|-----------------------------------------------------------------------------|
| `file`         | file    | Tak      | Nagranie video do zapisania (format: `.webm`)                               |
| `title`        | string  | Nie      | Opcjonalna nazwa pliku - jeśli nie podano, używana jest bieżąca data i czas |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Strona HTML z komunikatem: "Nagranie zapisane!".
```

**_Błąd (400 Bad Request)_**

Jeśli brak pliku:

```json
{
  "error": "Nie przekazano żadnego pliku!"
}
```

**_Błąd (500 Internal Server Error)_**

W przypadku błędu konwersji:

```json
{
  "error": "Konwersja do MP4 nie powiodła się."
}
```

## `/my_recordings`

### Opis

- zwraca listę zapisanych nagrań `mp4`

### Metoda

`GET`

### Nagłówki

- brak wymaganych nagłówków

#### Przykład zapytania

- brak danych w treści zapytania

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Strona HTML z listą nagrań wideo.
```

## `/events`

### Opis

- pobiera wydarzenia z Google Calendar

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista wydarzeń
```

**_500 Internal Server Error_**

-  jeśli wystąpi błąd podczas pobierania wydarzeń

## `/list_windows`

### Opis

- zwraca listę nazw wszystkich otwartych okien

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista tytułów okien
```

## `/generate_notes`

### Opis

- generuje transkrypcję tekstową z istniejącego pliku `.wav`

### Metoda

`POST`

### Nagłówki

- `Content-Type: application/x-www-form-urlencoded`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                                                      |
|----------------|---------|----------|-----------------------------------------------------------|
| `title`        | string  | Tak      | Nazwa pliku `.wav` (bez rozszerzenia) do przetworzenia    |

#### Odpowiedzi

**_Sukces (200 OK)_**

```json
{
  "message": "Transkrypcja wygenerowana pomyślnie."
}
```

**_Błąd (400 Bad Request)_**

Jeśli brak nazwy pliku:

```json
{
  "error": "Brak nazwy pliku! Podaj tytuł pliku WAV."
}
```

**_Błąd (404 Not Found)_**

Jeśli plik `.wav` nie istnieje:

```json
{
  "error": "Plik moje_nagranie.wav nie istnieje w katalogu recordings!"
}
```

## `/my_notes`

### Opis

- wyświetla listę wygenerowanych notatek `.docx`

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista notatek w formie HTML
```

## `/zoom/login`

### Opis

- przekierowuje użytkownika do logowania w Zoom, aby uzyskać autoryzację

### Metoda

`GET`

## `/zoom-meetings`

### Opis

- pobiera listę spotkań użytkownika Zoom po uzyskaniu tokena autoryzacyjnego

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista spotkań w formacie JSON
```

## `/zoom-meeting-participants`

### Opis

- pobiera uczestników danego spotkania Zoom

### Metoda

`GET`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                           |
|----------------|---------|----------|--------------------------------|
| `meetingId`    | string  | Tak      | Identyfikator spotkania Zoom   |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista uczestników
```

## `/teams/login`

### Opis

- przekierowuje użytkownika do logowania w Microsoft Teams

### Metoda

`GET`

## `/teams-events`

### Opis

- pobiera listę wydarzeń z kalendarza Microsoft Teams po autoryzacji

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista wydarzeń w formacie JSON
```

## `/teams-event-details`

### Opis

- pobiera szczegółowe informacje o wybranym wydarzeniu w Teams

### Metoda

`GET`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                           |
|----------------|---------|----------|--------------------------------|
| `eventId`      | string  | Tak      | Identyfikator wydarzenia Teams |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Szczegółowe informacje o wydarzeniu w formacie JSON
```

## `/google-calendar/login`

### Opis

- generuje link do logowania w Google, aby uzyskać autoryzację do kalendarza

### Metoda

`GET`

## `/google-calendar/events`

### Opis

- pobiera listę wydarzeń z Google Calendar przy użyciu autoryzowanych danych

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista wydarzeń w formacie JSON
```

## `/google-calendar/event-details`

### Opis

- pobiera szczegółowe informacje o wybranym wydarzeniu z Google Calendar

### Metoda

`GET`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                           |
|----------------|---------|----------|--------------------------------|
| `eventId`      | string  | Tak      | Identyfikator wydarzenia       |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Szczegóły wydarzenia w formacie JSON
```

## `/ms-calendar/login`

### Opis

- generuje link do logowania w MS Calendar

### Metoda

`GET`

## `/ms-calendar/events`

### Opis

- pobiera listę wydarzeń z MS Calendar przy użyciu danych autoryzacyjnych

### Metoda

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista wydarzeń w formacie JSON
```

## `/ms-calendar/event-details`

### Opis

-pobiera szczegółowe informacje o wybranym wydarzeniu z MS Calendar, w tym listę uczestników

### Metoda

`GET`

### Body (JSON)

| Pole           | Typ     | Wymagane | Opis                           |
|----------------|---------|----------|--------------------------------|
| `eventId`      | string  | Tak      | Identyfikator wydarzenia       |

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Szczegółowe informacje o wydarzeniu w formacie JSON
```
---

| ![logoo](https://github.com/user-attachments/assets/4b34cc5f-8992-45bb-b354-4a69a66a5189) | **Zespół NoteWriter Girls Inc.** | **👑 Ola 🐝 Maja 🐝 Asia 🐝 Julka** |
|:--:|:--:|:--:|
