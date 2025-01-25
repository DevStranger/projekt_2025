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

![Zrzut ekranu 2025-01-25 134102](https://github.com/user-attachments/assets/29114733-617d-4e3f-8add-0e0b0067d11a)

W ramach testu do aplikacji wysłano **8048** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **16 ms** oraz **99%** zostało wykonanych w czasie maksymalnie **24 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **8,04 ms**.

Obsłużono średnio **132,7** żądań na sekundę.

![aaaaaa](https://github.com/user-attachments/assets/216a5141-087d-4a03-9ea6-904a24f02635)

#### Users=500 Ramp=15



### 2. Dla strony wyświetlającej nagrania

#### Users=50 Ramp=1



#### Users=200 Ramp=5



#### Users=500 Ramp=15



### 3. Dla strony wyświetlającej notatki

#### Users=50 Ramp=1



#### Users=200 Ramp=5



#### Users=500 Ramp=15



### 4. Dla strony do nagrywania spotkań

#### Users=50 Ramp=1



#### Users=200 Ramp=5



#### Users=500 Ramp=15




