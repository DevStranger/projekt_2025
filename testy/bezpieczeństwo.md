#  Analiza bezpieczeństwa kodu za pomocą CodeQL

W naszym projekcie użyłyśmy narzędzia `CodeQL`, które pomogło nam przeanalizować kod pod kątem potencjalnych problemów związanych z bezpieczeństwem i jakością.
CodeQL przeprowadza analizę statyczną (czyli sprawdza kod bez jego uruchamiania) oraz dynamiczną (czyli analizuje, jak działa kod w czasie rzeczywistym).

W ramach naszego procesu ciągłej integracji (CI) uruchomiłyśmy trzy główne analizy:

1. **CodeQL dla JavaScript**: CodeQL analizowało kod w JS, sprawdzając go pod kątem potencjalnych błędów i zagrożeń
2. **CodeQL dla Pythona**: narzędzie sprawdzało kod w Pythonie, szukając problemów z bezpieczeństwem
3. **Skanowanie kodu w Pull Requestach**: CodeQL monitorowało każdą zmianę w kodzie, która była dodawana przez Pull Requesty, aby upewnić się, że zmiany te nie wprowadziły nowych problemów

Po każdej analizie CodeQL generowało wyniki, które były automatycznie sprawdzane przez nasz system CI. 
Jeśli narzędzie znalazło jakikolwiek problem, zespół odpowiednio dostawał powiadomienie, aby wprowadzić poprawki.

## Rezultaty

![Zrzut ekranu 2025-02-06 073835](https://github.com/user-attachments/assets/6bcf013c-e25b-4571-9003-08e9362761e1)

✔ "All checks have passed" - wszystkie sprawdzenia (testy) zakończyły się pomyślnie. Kod przeszedł wszystkie zdefiniowane procesy weryfikacji.

✔ "3 successful checks" - trzy różne testy zostały przeprowadzone i wszystkie zakończyły się sukcesem
