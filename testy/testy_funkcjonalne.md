# Testy wymagań funkcjonalnych

- jednostkowe
- integracyjne
- akceptacyjne

## Jednostkowe


## Integracyjne

### 1. Test integracji przycisków z przekierowaniami ✔

**Cel:** sprawdzenie czy przyciski nawigacyjne poprawnie przekierowują użytkownika do odpowiednich stron i czy dane są poprawnie ładowane z backendu

**Narzędzie:** - (manualnie)

Kliknięcie przycisku „Moje notatki” przekierowuje użytkownika do strony z listą notatek. Podobnie dla „Moje nagrania”. 

### 2. Test integracji frontendu z backendem (ładowanie danych)

**Cel:** sprawdzenie czy frontend poprawnie otrzymuje dane z backendu i je wyświetla

**Narzędzie:** - (manualnie)

Na stronie "Moje notatki" frontend wysyła zapytanie do backendu o listę dostępnych notatek, a backend zwraca odpowiednią listę. Na stronie "Moje nagrania" frontend wysyła zapytanie o nagrania, a backend zwraca odpowiednie dane.

### 3. Test integracji z systemem plików

**Cel:** sprawdzenie czy pliki notatek i nagrań są poprawnie przechowywane i dostępne na serwerze
**Narzędzie:** - (manualnie)

Plik jest poprawnie zapisany na serwerze w odpowiednim katalogu i odpowiednio konwertowany. Po załadowaniu strony z notatkami użytkownik ma możliwość pobrania tych plików z serwera.

***Wszystkie powyższ testy zostały także przeprowadzone automatycznie z użyciem narzędzia TestCafe (patrz: testy akceptacyjne)***

## Akceptacyjne

**Cel:** weryfikacja poprawności działania funkcji aplikacji poprzez sprawdzenie jej zachowania w różnych scenariuszach użytkowych

**Narzędzie:** testcafe

### Przeprowadzane testy

`/testy/tests.js`

https://github.com/DevStranger/projekt_2025/blob/ac420128c920077b187d1cff3820a46d57407100/testy/tests.js

### Przebieg testów

![Zrzut ekranu 2025-01-25 163754](https://github.com/user-attachments/assets/6924ec1d-0aeb-4407-8c84-aa8752cc0aae)
![Zrzut ekranu 2025-01-25 162753](https://github.com/user-attachments/assets/bebd74ca-7bc3-45e1-b23f-8c965b412e72)

### Wyniki testów

![Zrzut ekranu 2025-01-25 164639](https://github.com/user-attachments/assets/33eb9518-f378-42c6-a2db-072a34dfeb23)

Po stworzeniu nagrań z użyciem aplikacji:

![Zrzut ekranu 2025-01-25 164930](https://github.com/user-attachments/assets/db0a8b38-5836-4524-a925-ac1f2055fad0)
