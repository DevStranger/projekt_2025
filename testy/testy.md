# Testy wymagań niefunkcjonalnych

- wydajność
- bezpieczeństwo
- dostępność
- skalowalność

## Test obciążenia (Load Testing)

**Cel:** sprawdzenie ile użytkowników strona jest w stanie obsłużyć jednocześnie

**Narzędzie:** Locust (narzędzie do testowania obciążenia, które pozwala na symulowanie wielu użytkowników korzystających z aplikacji webowej, a także umożliwia łatwe pisanie testów w Pythonie)

### 1. Dla strony głównej naszej aplikacji

#### Users=50 Ramp=1

![Zrzut ekranu 2025-01-25 133207](https://github.com/user-attachments/assets/45efd15d-09a0-4592-a8b9-545a1886534d)

W ramach testu do aplikacji wysłano **3970** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **11 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **6,04 ms**.

Obsłużono średnio **33,7** żądań na sekundę.

![total_requests_per_second_1737808342 482](https://github.com/user-attachments/assets/e9d49b5b-edb5-44bf-aae9-7d843fa67fa6)

#### Users=200 Ramp=5



#### Users=500 Ramp=15



### 2. Dla strony wyświetlającej nagrania



### 3. Dla strony wyświetlającej notatki



### 4. Dla strony do nagrywania spotkań
