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

#### Users=500 Ramp=5 Testing time=300

![Zrzut ekranu 2025-01-25 135148](https://github.com/user-attachments/assets/f71c6226-11bf-4bdc-8419-355161d08c73)

W ramach testu do aplikacji wysłano **22 504** żądania HTTP i **7024** z nich zakończyło się niepowodzeniem (**~31%**). 

**95%** żądań zostało wykonanych w czasie poniżej **51 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **17,18 ms**.

Obsłużono średnio **327,6** żądań na sekundę.

![total_requests_per_second_1737809508 924](https://github.com/user-attachments/assets/28715d5e-95f4-4ff2-987a-b0b2ff735fa3)

### 2. Dla strony wyświetlającej nagrania

#### Users=50 Ramp=1 Testing time=60

![Zrzut ekranu 2025-01-25 135726](https://github.com/user-attachments/assets/91e083c3-2cc5-4c64-afd0-7101e5c4e5cd)

W ramach testu do aplikacji wysłano **1189** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **14 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **6,7 ms**.

Obsłużono średnio **32,3** żądań na sekundę.

![total_requests_per_second_1737809858 173](https://github.com/user-attachments/assets/ef6a8117-6e8d-4e52-b04e-e7521ac8ad00)

#### Users=200 Ramp=2 Testing time=100

![Zrzut ekranu 2025-01-25 135959](https://github.com/user-attachments/assets/6813e97b-7f0e-4572-80eb-de6e74cc5318)

W ramach testu do aplikacji wysłano **6763** żądania HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **15 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **7,57 ms**.

Obsłużono średnio **124** żądania na sekundę.

![total_requests_per_second_1737810000 283](https://github.com/user-attachments/assets/d1361c35-5e11-4d75-8dc2-2b8257d0a44c)

#### Users=500 Ramp=5 Testing time=300

![Zrzut ekranu 2025-01-25 140549](https://github.com/user-attachments/assets/aa08db34-873c-450a-8c42-4032d32a1e24)

W ramach testu do aplikacji wysłano **81 501** żądań HTTP i **42 366** z nich zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **99 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **37,08 ms**.

Obsłużono średnio **329,5** żądania na sekundę.

![total_requests_per_second_1737810350 541](https://github.com/user-attachments/assets/dc163113-5f65-4253-a748-ce4773572e40)

#### Users=500 Ramp=1 Testing time=300



### 3. Dla strony wyświetlającej notatki

#### Users=50 Ramp=1 Testing time=60



#### Users=200 Ramp=2 Testing time=100



#### Users=500 Ramp=15 Testing time=300



### 4. Dla strony do nagrywania spotkań

#### Users=50 Ramp=1 Testing time=60



#### Users=200 Ramp=2 Testing time=100



#### Users=500 Ramp=5 Testing time=300



## Test szybkości odpowiedzi



## Test wrażliwości na ataki (OWASP ZAP)



## Testy zgodności (dla różnych przeglądarek)


