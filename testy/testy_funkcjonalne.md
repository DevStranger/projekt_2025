# Testy wymagań funkcjonalnych

- jednostkowe
- integracyjne
- akceptacyjne

## Jednostkowe

**Cel:** sprawdzenie poprawności działania trzech tras (routes) w naszej aplikacji webowej
    - `/` strona główna
    - `/google-calendar` wyświetlanie kalendarza Google
    - `ms-calendar` kalendarz Microsoft

Testy te weryfikują, czy aplikacja:

- zwraca poprawny kod statusu HTTP 200 dla strony głównej
- zwraca odpowiedź zawierającą błąd (w formacie JSON) dla dwóch pozostałych tras, tj. `/google-calendar` i `/ms-calendar`

**Narzędzie:** framework `unittest` w języku Python

[`\testy\test_routes.py`](https://github.com/DevStranger/projekt_2025/blob/cebadf649cadffb94e4f25582b5b6d69349d9bbf/testy/test_routes.py)

Testy te zakończyły się powodzeniem ✔

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

[`\testy\testcafe\tests.js`](https://github.com/DevStranger/NoteWriter/blob/main/testy/testcafe/tests.js)

### Przebieg testów 

![Zrzut ekranu 2025-01-25 163754](https://github.com/user-attachments/assets/6924ec1d-0aeb-4407-8c84-aa8752cc0aae)
![Zrzut ekranu 2025-01-25 162753](https://github.com/user-attachments/assets/bebd74ca-7bc3-45e1-b23f-8c965b412e72)

### Wyniki testów ✔

![Zrzut ekranu 2025-01-25 164639](https://github.com/user-attachments/assets/33eb9518-f378-42c6-a2db-072a34dfeb23)

Po stworzeniu nagrań z użyciem aplikacji:

![Zrzut ekranu 2025-01-25 164930](https://github.com/user-attachments/assets/db0a8b38-5836-4524-a925-ac1f2055fad0)

### Testy integracji z kalendarzem i aplikacją do telekonferencji

---

#### Google Calendar - panel do logowania ✔

[`\testy\testcafe\google_test.js`](https://github.com/DevStranger/NoteWriter/blob/main/testy/testcafe/google_test.js)

![Zrzut ekranu 2025-02-05 215428](https://github.com/user-attachments/assets/b4c84282-87d2-481e-ac12-9909461e05e4)
![Zrzut ekranu 2025-02-05 220808](https://github.com/user-attachments/assets/c174affd-10e9-43d2-8ef4-d0ebca86fb90)
![Zrzut ekranu 2025-02-05 222203](https://github.com/user-attachments/assets/4583056e-8bd4-42a6-bf7b-a12379e5e03e)
![Zrzut ekranu 2025-02-05 222145](https://github.com/user-attachments/assets/20a94f24-ff71-42c3-8153-77ccdb48208a)
![Zrzut ekranu 2025-02-05 221344](https://github.com/user-attachments/assets/0656e1c4-45b2-435c-899b-75dd7902c509)

---

#### Teams ✔

[`\testy\testcafe\teams_test.js`](https://github.com/DevStranger/NoteWriter/blob/main/testy/testcafe/teams_test.js)

![Zrzut ekranu 2025-02-05 223229](https://github.com/user-attachments/assets/3c590c61-8951-4c0a-9488-30aa62f79268)
![Zrzut ekranu 2025-02-05 223614](https://github.com/user-attachments/assets/4d78196d-fb11-4318-b878-09429c10ad60)
![Zrzut ekranu 2025-02-05 223758](https://github.com/user-attachments/assets/5b0a96ba-f92f-4c18-a2b4-c88101f5b158)

---

#### Zoom ✔

[`\testy\testcafe\zoom_test.js`](https://github.com/DevStranger/NoteWriter/blob/main/testy/testcafe/zoom_test.js)

![Zrzut ekranu 2025-02-05 225128](https://github.com/user-attachments/assets/651e8905-cea9-4c9d-af4f-10f662d0df5f)
![Zrzut ekranu 2025-02-05 225211](https://github.com/user-attachments/assets/858f363b-e6ba-4de5-981a-a881dd7556a5)
![Zrzut ekranu 2025-02-05 225311](https://github.com/user-attachments/assets/297f1943-81ee-449d-bd42-befac04ee171)

---

### Test funkcjonalności wysyłania notatek do wybranych użytkowników 

[`\testy\testcafe\send_notes.js`](https://github.com/DevStranger/NoteWriter/blob/main/testy/testcafe/send_notes.js)

---

#### Wybór danej notatki na podstawie wyszukiwań ✔

![Zrzut ekranu 2025-02-05 225825](https://github.com/user-attachments/assets/6e37ea45-f7d7-44cb-a508-7b90fad0ae73)

---

#### Dodawanie nowego adresu e-mail i wysyłanie notatek ✔

![Zrzut ekranu 2025-02-05 233731](https://github.com/user-attachments/assets/a855805f-67e0-4c78-8d31-51889e0800f1)
![Zrzut ekranu 2025-02-05 233319](https://github.com/user-attachments/assets/76bb0f19-d514-4fae-9802-14a1e39574f3)
![Zrzut ekranu 2025-02-05 234026](https://github.com/user-attachments/assets/7f33867d-439b-4eb8-91a1-4975f0467fe8)

---

| ![logoo](https://github.com/user-attachments/assets/4b34cc5f-8992-45bb-b354-4a69a66a5189) | **Zespół NoteWriter Girls Inc.** | **👑 Ola 🐝 Maja 🐝 Asia 🐝 Julka** |
|:--:|:--:|:--:|


