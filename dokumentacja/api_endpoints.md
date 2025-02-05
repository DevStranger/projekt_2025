# API endpoints

**Wersja:** 1.2

**Data utworzenia:** 25.I.2025

**Data ostatniej aktualizacji:** 05.02.2025

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

`GET`

#### Odpowiedzi

**_Sukces (200 OK)_**

```
Lista notatek w formie HTML
```

## ``
