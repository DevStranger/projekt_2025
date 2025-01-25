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

