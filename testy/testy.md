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

#### Users=500 Ramp=5 Run time=300

![Zrzut ekranu 2025-01-25 135148](https://github.com/user-attachments/assets/f71c6226-11bf-4bdc-8419-355161d08c73)

W ramach testu do aplikacji wysłano **22 504** żądania HTTP i **7024** z nich zakończyło się niepowodzeniem (**~31%**). 

**95%** żądań zostało wykonanych w czasie poniżej **51 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **17,18 ms**.

Obsłużono średnio **327,6** żądań na sekundę.

![total_requests_per_second_1737809508 924](https://github.com/user-attachments/assets/28715d5e-95f4-4ff2-987a-b0b2ff735fa3)

### 2. Dla strony wyświetlającej nagrania

#### Users=50 Ramp=1 Run time=60

![Zrzut ekranu 2025-01-25 135726](https://github.com/user-attachments/assets/91e083c3-2cc5-4c64-afd0-7101e5c4e5cd)

W ramach testu do aplikacji wysłano **1189** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **14 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **6,7 ms**.

Obsłużono średnio **32,3** żądań na sekundę.

![total_requests_per_second_1737809858 173](https://github.com/user-attachments/assets/ef6a8117-6e8d-4e52-b04e-e7521ac8ad00)

#### Users=200 Ramp=2 Run time=100

![Zrzut ekranu 2025-01-25 135959](https://github.com/user-attachments/assets/6813e97b-7f0e-4572-80eb-de6e74cc5318)

W ramach testu do aplikacji wysłano **6763** żądania HTTP i **żadne** z nich nie zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **15 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **7,57 ms**.

Obsłużono średnio **124** żądania na sekundę.

![total_requests_per_second_1737810000 283](https://github.com/user-attachments/assets/d1361c35-5e11-4d75-8dc2-2b8257d0a44c)

#### Users=500 Ramp=5 Run time=300

![Zrzut ekranu 2025-01-25 140549](https://github.com/user-attachments/assets/aa08db34-873c-450a-8c42-4032d32a1e24)

W ramach testu do aplikacji wysłano **81 501** żądań HTTP i **42 366** z nich zakończyło się niepowodzeniem. 

**95%** żądań zostało wykonanych w czasie poniżej **99 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **37,08 ms**.

Obsłużono średnio **329,5** żądania na sekundę.

![total_requests_per_second_1737810350 541](https://github.com/user-attachments/assets/dc163113-5f65-4253-a748-ce4773572e40)

#### Users=500 Ramp=1 Run time=300

![Zrzut ekranu 2025-01-25 141152](https://github.com/user-attachments/assets/9e0e4690-4f1e-4091-9518-9b2cec9a8f82)

W ramach testu do aplikacji wysłano **29 767** żądań HTTP i **3557** z nich zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **23 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **10,5 ms**.

Obsłużono średnio **193,3** żądania na sekundę.

![total_requests_per_second_1737810354 548](https://github.com/user-attachments/assets/a0074984-e81f-4673-b83f-27af4aa4af75)

### 3. Dla strony wyświetlającej notatki

#### Users=50 Ramp=1 Run time=60

![Zrzut ekranu 2025-01-25 141559](https://github.com/user-attachments/assets/8fe6246b-dd2f-42d4-82b7-d018b6c8061f)

W ramach testu do aplikacji wysłano **113** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **7 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **5,1 ms**.

Obsłużono średnio **7,1** żądań na sekundę.

![total_requests_per_second_1737810960 496](https://github.com/user-attachments/assets/ae846aae-3225-4d6e-817a-2e2c4dd52913)

#### Users=200 Ramp=2 Run time=100

![Zrzut ekranu 2025-01-25 141830](https://github.com/user-attachments/assets/c4e00633-9f1b-4b11-bf3b-cb000e9455d9)

W ramach testu do aplikacji wysłano **6719** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **16 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **7,79 ms**.

Obsłużono średnio **123,3** żądań na sekundę.

![total_requests_per_second_1737811111 113](https://github.com/user-attachments/assets/012ba31c-d3ff-4c28-b5f0-55a3facfcb41)

#### Users=500 Ramp=3 Run time=300

![Zrzut ekranu 2025-01-25 142521](https://github.com/user-attachments/assets/8733855a-024e-4e57-b5e3-b92795acec4c)

W ramach testu do aplikacji wysłano **6070** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **43 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **16,94 ms**.

Obsłużono średnio **138,3** żądań na sekundę.

![total_requests_per_second_1737811451 971](https://github.com/user-attachments/assets/ed6e465f-a9ec-4925-bf52-49ce20ba0f64)

#### Users=700 Ramp=4 Run time=300

![Zrzut ekranu 2025-01-25 142809](https://github.com/user-attachments/assets/7f8975f4-2a9e-421c-a6b8-40bfcdba4383)

W ramach testu do aplikacji wysłano **27 317** żądań HTTP i **10 433** z nich zakończyło się niepowodzeniem (~**38%**).

**95%** żądań zostało wykonanych w czasie poniżej **150 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **36,18 ms**.

Obsłużono średnio **350,6** żądań na sekundę.

![Zrzut ekranu 2025-01-25 142821](https://github.com/user-attachments/assets/b1830819-3000-448f-9aca-e7b4c46eefb4)

![total_requests_per_second_1737811690 064](https://github.com/user-attachments/assets/3edc57aa-3a30-4556-81cb-1a5ec8ff4f1e)

### 4. Dla strony do nagrywania spotkań

#### Users=50 Ramp=15 Testing time=30

![Zrzut ekranu 2025-01-25 151527](https://github.com/user-attachments/assets/0c7a63d8-474a-4959-b007-58dd2ad06f8a)

W ramach testu do aplikacji wysłano **973** żądania HTTP i **żadne** z nich nie zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **19 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **7,94 ms**.

Obsłużono średnio **32,7** żądań na sekundę.

![total_requests_per_second_1737814528 248](https://github.com/user-attachments/assets/4aa0481b-7b02-47ea-9c61-3c593ff2874a)

#### Users=200 Ramp=10 Testing time=100

![Zrzut ekranu 2025-01-25 151730](https://github.com/user-attachments/assets/c327d5cb-c1ca-4688-aeb5-72ca731ac226)

W ramach testu do aplikacji wysłano **12 041** żądań HTTP i **żadne** z nich nie zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **18 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **8,78 ms**.

Obsłużono średnio **132,7** żądań na sekundę.

![total_requests_per_second_1737814651 645](https://github.com/user-attachments/assets/a3d0cfdf-2268-4484-bd6d-929bc9798c15)

#### Users=500 Ramp=3 Testing time=300

![Zrzut ekranu 2025-01-25 151223](https://github.com/user-attachments/assets/99006622-20fc-40a8-8fc7-369cf0ce3020)

W ramach testu do aplikacji wysłano **69 691** żądań HTTP i **31 469** z nich zakończyło się niepowodzeniem.

**95%** żądań zostało wykonanych w czasie poniżej **290 ms**, a średni czas odpowiedzi dla wszystkich żądań wynosił ok. **56,34 ms**.

Obsłużono średnio **327,9** żądań na sekundę.

![Zrzut ekranu 2025-01-25 151236](https://github.com/user-attachments/assets/6a9aa4c8-6289-4b88-bd67-1427d9ad471e)

```
CPU usage above 90%! This may constrain your throughput and may even give inconsistent response time measurements!
```

![total_requests_per_second_1737814344 521](https://github.com/user-attachments/assets/11399c64-57f9-40e3-bec6-761048b9f847)

## Test szybkości odpowiedzi

**Cel:** zmierzyć czas odpowiedzi aplikacji na zapytania HTTP

**Narzędzie:** curl



## Test wrażliwości na ataki (OWASP ZAP)

**Cel:** sprawdzić, czy aplikacja ma luki bezpieczeństwa

**Narzędzie:** OWASP ZAP (Zed Attack Proxy)


## Testy zgodności (dla różnych przeglądarek)

**Cel:** sprawdzić czy aplikacja jest dostępna w różnych przeglądarkach

**Narzędzie:** przeglądarka Chrome, przeglądarka Microsoft Edge

# Testy wymagań funkcjonalnych

- jednostkowe
- integracyjne
- akceptacyjne
