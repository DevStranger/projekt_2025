# API endpoints

## `/record/record_window`

### Opis
Rozpoczyna nagrywanie wybranego okna aplikacji w osobnym wątku

### Metoda
`**POST**`

### Nagłówki
- `Content-Type: application/json`

### Body (JSON)
| Pole           | Typ     | Wymagane | Opis                                      |
|-----------------|---------|----------|------------------------------------------|
| `window_title` | string  | Tak       | Tytuł okna, które ma być nagrywane.      |

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
