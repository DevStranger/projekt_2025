#  Analiza bezpieczeństwa kodu za pomocą CodeQL

W naszym projekcie użyłyśmy narzędzia `CodeQL`, które pomogło nam przeanalizować kod pod kątem potencjalnych problemów związanych z bezpieczeństwem i jakością.
CodeQL przeprowadza analizę statyczną (czyli sprawdza kod bez jego uruchamiania) oraz dynamiczną (czyli analizuje, jak działa kod w czasie rzeczywistym).

W ramach naszego procesu ciągłej integracji (CI) uruchomiłyśmy trzy główne analizy:

1. **CodeQL dla JavaScript**: CodeQL analizowało kod w JS, sprawdzając go pod kątem potencjalnych błędów i zagrożeń
2. **CodeQL dla Pythona**: narzędzie sprawdzało kod w Pythonie, szukając problemów z bezpieczeństwem
3. **Skanowanie kodu w Pull Requestach**: CodeQL monitorowało każdą zmianę w kodzie, która była dodawana przez Pull Requesty, aby upewnić się, że zmiany te nie wprowadziły nowych problemów

Po każdej analizie CodeQL generowało wyniki, które były automatycznie sprawdzane przez nasz system CI. 
Jeśli narzędzie znalazło jakikolwiek problem, zespół odpowiednio dostawał powiadomienie, aby wprowadzić poprawki.

## Analiza wyników

![Zrzut ekranu 2025-02-06 073835](https://github.com/user-attachments/assets/6bcf013c-e25b-4571-9003-08e9362761e1)

✔ "All checks have passed" - wszystkie sprawdzenia (testy) zakończyły się pomyślnie. Kod przeszedł wszystkie zdefiniowane procesy weryfikacji.

✔ "3 successful checks" - trzy różne testy zostały przeprowadzone i wszystkie zakończyły się sukcesem

---

#  Analiza bezpieczeństwa kodu za pomocą [Bandit](https://bandit.readthedocs.io/en/latest/)

W naszym projekcie użyłyśmy narzędzia `Bandit` do analizy kodu Python pod kątem potencjalnych problemów związanych z bezpieczeństwem. Bandit wykonuje analizę statyczną, czyli sprawdza kod bez jego uruchamiania, identyfikując luki i niebezpieczne wzorce w kodzie.

## Przeprowadzone testy

- **Total lines of code** (całkowita liczba linii kodu Python, która została przeanalizowana): 1310
- **Total lines skipped** (#nosec): 0 (żadna nie została pominięta)
  
![Zrzut ekranu 2025-02-06 081824](https://github.com/user-attachments/assets/3bdfc035-b1c9-44d8-9abf-db90fcdf2e15)

#### B101 – Assert used

- wykrywa użycie instrukcji `assert` w kodzie

#### B102 – Eval used

- sprawdza, czy w kodzie używana jest funkcja `eval()`
- funkcja `eval()` wykonuje przekazany do niej ciąg znaków jako kod Pythona, co w przypadku niezweryfikowanych danych wejściowych może prowadzić do wykonania złośliwego kodu

#### B103 – Exec used

- wykrywa użycie funkcji `exec()`
- `exec()` umożliwia dynamiczne wykonanie kodu, co niesie ze sobą ryzyko uruchomienia nieautoryzowanego lub złośliwego kodu

#### B110 – Potentially unsafe constructs

- wyszukuje potencjalnie niebezpieczne konstrukcje w kodzie, na przykład wywołania systemowe z nieodpowiednimi parametrami
- lub nieprecyzyjne użycie bloków `try/except`, które mogą maskować rzeczywiste problemy

#### B201 – Insecure URL usage

- sprawdza, czy w kodzie nie są używane niezabezpieczone adresy URL
- mogą one prowadzić do ataków typu man-in-the-middle i narażać transmisję danych na przechwycenie

#### B301 – Hardcoded credentials

- wykrywa twardo zakodowane dane wrażliwe, takie jak hasła, klucze API czy inne poufne informacje, które powinny być przechowywane w bezpieczny sposób

## Analiza wyników

![Zrzut ekranu 2025-02-06 080935](https://github.com/user-attachments/assets/0fa2c213-901d-477c-b8b1-dfefc63fa6d3)
![Zrzut ekranu 2025-02-06 080945](https://github.com/user-attachments/assets/3d0cabba-fd14-4503-9fb0-1246065f9cbb)
![Zrzut ekranu 202![Zrzut ekranu 2025-02-06 081004](https://github.com/user-attachments/assets/666b0844-9806-4909-bdd6-43ba6d731294)
5-02-06 080957](https://github.com/user-attachments/assets/32a6e73d-bc0c-4b71-a491-ce506ae7a79a)
![Zrzut ekranu 2025-02-06 081015](https://github.com/user-attachments/assets/ad8af19c-992d-4005-83e2-ebd5ffda3b72)
![Zrzut ekranu 2025-02-06 081020](https://github.com/user-attachments/assets/2002913f-001c-47c4-a41d-7393ef75733c)
![Zrzut ekranu 2025-02-06 081109](https://github.com/user-attachments/assets/db92f728-43e7-410e-b117-33777e20c722)
![Zrzut ekranu 2025-02-06 081118](https://github.com/user-attachments/assets/2c63c228-a745-4c09-bc66-a64fdc56a58e)
![Zrzut ekranu 2025-02-06 081125](https://github.com/user-attachments/assets/9d35dc48-a4ac-4795-8162-d57b4a1175a3)
![Zrzut ekranu 2025-02-06 081129](https://github.com/user-attachments/assets/e03973bc-20b3-4b48-9e7a-5e7bd4412703)
![Zrzut ekranu 2025-02-06 081135](https://github.com/user-attachments/assets/14cfb492-4963-41b8-90d3-40f93622e7ea)

### Problemy wg. 'dotkliwości' (severity)

- **Low**: 17
- **Medium**: 12
- **High**: 0 (brak poważnych zagrożeń)

### Problemy wg. 'pewnością' (confidence)

- **Low**: 12 (niekoniecznie rzeczywiste zagrożenie)
- **Medium**: 9
- **High**: 8 (realne problemy)

### Główne problemy

#### Hardcodowane dane wrażliwe (B105: hardcoded_password_string)

- kilka fragmentów kodu zawiera twardo wpisane dane, takie jak klucze, hasła, tajne wartości czy adresy URL (np. `app.secret_key`, `GOOGLE_CLIENT_SECRET`, `CLIENT_SECRET`, `ZOOM_CLIENT_SECRET`, itd.)
- dane wrażliwe są bezpośrednio osadzone w kodzie źródłowym, co naraża je na przypadkowe ujawnienie

#### Brak timeoutów przy wywołaniach HTTP (B113: request_without_timeout)

- kilka wywołań funkcji `requests.get()` i `requests.post()` nie określa parametru `timeout`
- brak ustawienia limitu czasu na połączenia HTTP powoduje, że w przypadku problemów sieciowych lub opóźnień serwera aplikacja może nieoczekiwanie zawiesić się, czekając na odpowiedź

#### Problemy związane z użyciem modułu subprocess (B404, B607, B603)

- import modułu `subprocess` oraz wywołania funkcji `subprocess.run()` z niepełnymi ścieżkami do wykonywalnych programów (partial executable path)
- użycie `subprocess.run()` bez odpowiedniego sprawdzania danych wejściowych, co może prowadzić do wykonania nieautoryzowanego kodu
- brak odpowiedniej walidacji oraz pełnej ścieżki do wykonywanych programów zwiększa ryzyko uruchomienia złośliwego kodu lub niezamierzonych operacji systemowych

---

| ![logoo](https://github.com/user-attachments/assets/4b34cc5f-8992-45bb-b354-4a69a66a5189) | **Zespół NoteWriter Girls Inc.** | **👑 Ola 🐝 Maja 🐝 Asia 🐝 Julka** |
|:--:|:--:|:--:|
