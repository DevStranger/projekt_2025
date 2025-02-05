# ![logoo](https://github.com/user-attachments/assets/ea83b9b5-852f-429a-9611-ffe853084701) Aplikacja do Sporządzania Notatek ze Spotkań 

**Data utworzenia repozytorium:** 2024-12-03

**Data ostatniej aktualizacji:** 2025-02-05

---

## Członkowie zespołu

- Aleksandra Adamiak
- Maja Chlipała
- Joanna Furtak
- Julia Mikrut

## Macierz kompetencji

| Kompetencje                      | Ola        | Maja | Asia   | Julka |
|----------------------------------|------------|------|--------|-------|
| Znajomość algorytmów             | ✅         | ✅   | ✅    | ❌   |
| Znajomość j. angielskiego        | ✅         | ✅   | ✅    | ✅   |
| Umiejętność obsługi GitLab       | ✅         | ✅   | ✅    | ✅   |
| Programowanie Python             | ✅         | ✅   | ✅    | ✅   |
| Obsługa baz danych (SQL)         | ✅         | ✅   | ✅    | ✅   |
| Programowanie C++                | ✅         | ✅   | ❌    | ✅   |
| Programowanie Java               | ❌         | ❌   | ✅    | ❌   |
| Praca w grupie                   | ✅         | ❌   | ✅    | ✅   |
| Testowanie oprogramowania        | ✅         | ✅   | ✅    | ✅   |
| Umiejętność trenowania modeli ML | ✅         | ✅   | ✅    | ✅   |
| Obsługa API komunikacyjnych      | ✅         | ✅   | ✅    | ✅   |

✅ – posiada kompetencje  
❌ – brak kompetencji

---

## **Zarządzanie Notatkami i Transkrypcją**

### **Generowanie Notatek**
- oprócz tekstu mówionego, aplikacja powinna wykryć i zapisać, kto jest mówcą

### **Zbieranie Notatek z Materiałów Prowadzącego**
- zrzut ekranu powinien być wykonywany automatycznie przy wykryciu zmiany obrazu

### **Dodatkowe Funkcje**
- **licznik słów** wypowiedzianych przez daną osobę.

### **Zarządzanie Notatką po Zakończeniu Spotkania**
- po zakończeniu spotkania raport powinien zostać wysłany uczestnikom na ich adresy e-mail

### **Podsumowanie Spotkania**
- automatycznie generowane krótkie podsumowanie głównych tematów spotkania

### **Nagrywanie Ekranu**
- tak, każdy użytkownik powinien mieć możliwość nagrywania ekranu

### **Integracja z Kalendarzem**
- tak, aplikacja powinna synchronizować się z kalendarzem użytkownika

### **Dodatkowe Opcje Notatek**
- możliwość **wyszukiwania w notatkach**

### **Rozpoznawanie Pisma Odręcznego**
- nie przewiduje się tej funkcjonalności

### **Rozpoznawanie Nastroju Mówcy**
- nie przewiduje się tej funkcjonalności

### **Spełnienie Wymagań Klienta**
- ✅ **Tak**, wszystkie wymagania klienta są możliwe do spełnienia

---

## **Format Danych Wejściowych**

| Pole            | Typ danych |
|-----------------|------------|
| Imię i nazwisko | `string`   |
| E-mail          | `string`   |

---

## **Modelowany System**

### **Aktorzy**
- **Prowadzący**, **Uczestnicy spotkania**

### **Opis**
- celem działania jest pełen wgląd w przebieg spotkania bez konieczności oglądania pełnego nagrania
- automatycznie generowana notatka pozwala zaoszczędzić czas

### **Dane**
- przekształcenie prezentacji i tekstu mówionego w notatki ze spotkania

### **Wyzwalacz**
- automatyczny start po dołączeniu do spotkania lub ręczne uruchomienie przez użytkownika

### **Odpowiedź Systemu**
- **notatki w pliku tekstowym** zawierający przetworzone informacje

### **Uwagi**
- proces zbierania informacji powinien zakończyć się wraz z opuszczeniem spotkania

---

## **Diagramy UML**
- 📌 **Diagram przypadków użycia** – opisuje interakcje użytkownika z systemem
- 📌 **Diagram przepływu danych** – przedstawia przepływ informacji w systemie
- 📌 **Diagram sekwencyjny** – modeluje sekwencję zdarzeń w czasie

---

## **Architektura Systemu**

### **Opis Działania Aplikacji**
1. **Automatyczna Transkrypcja**  
   - mowa przekształcana na tekst z podziałem na mówców
   - rejestrowana liczba słów wypowiedzianych przez każdą osobę

2. **Zrzuty Ekranu**  
   - wykonywane automatycznie przy zmianie slajdu w prezentacji
   - obrazy wklejane do notatek dla lepszego kontekstu

3. **Generowanie Dokumentów**  
   - po zakończeniu spotkania aplikacja generuje notatkę w formacie **PDF lub Word**
   - dokument zawiera pełną transkrypcję, zrzuty ekranu i statystyki rozmowy

4. **Interfejs Użytkownika**  
   - podgląd notatki po zakończeniu spotkania

5. **Udostępnianie Notatek**  
   - opcja wysłania notatki do innych uczestników spotkania
   - lista kontaktów z możliwością wyboru odbiorców

6. **Automatyzacja**  
   - proces tworzenia i dystrybucji notatek jest **w pełni zautomatyzowany**

---

## **Język implementacji**
- **Python**  
  - wszyscy członkowie zespołu posiadają umiejętność programowania w Pythonie, co ułatwia współpracę i implementację

---

## Organizacja pracy

### 👑 Aleksandra Adamiak - Project Manager, UI Visionary

**Odpowiedzialna za:**
- organizację pracy zespołu
- koordynację działań członków zespołu
- wizję interfejsu użytkownika
- dokumentowanie postępów na kanale na Slack-u
- funkcjonalność nagrywania ekranu
- integrację poszczególnych części kodu
- frontend i backend
- i inne elementy projektu ...

### 🐝 Joanna Furtak - Koordynator ds. Integracji z Kalendarzem i Dystrybucji Notatek

**Odpowiedzialna za:**
- integrację aplikacji z kalendarzem Google i microsoft
- integrację z aplikacjami do telekonferencji - Zoom i Teams
- funkcjonalność rozsyłania notatek do uczestników spotkania po jego zakończeniu
- integrację poszczególnych części kodu
- frontend i backend
- i inne elementy projektu ...

### 🐝 Julia Mikrut - Koordynator ds. Sporządzania i Przetwarzania Notatek

**Odpowiedzialna za:**
- research i dostosowanie modelu przetwarzania języka naturalnego do celu sporządzania notatek na podstawie tekstu mówionego
- funkcjonalność wstawiania zrzutów ekranu do notatek (jeśli wyświetlana jest prezentacja)
- funkcjonalność sporządzania podsumowań notatek ze spotkania
- integrację poszczególnych części kodu
- frontend i backend
- i inne elementy projektu ...

### 🐝 Maja Chlipała - Koordynator ds. Dokumentacji Technicznej, Testów i Integracji Systemu

**Odpowiedzialna za:**
- sporządzenie dokumentacji technicznej projektu
- przeprowadzenie testów wymagań funkcjonalnych i niefunkcjonalnych (+ sprawozdanie z ich przebiegu)
- integrację poszczególnych części kodu
- frontend i backend
- i inne elementy projektu ...

---

## Autorzy i kontakt
- Aleksandra Adamiak (aadamiak@student.agh.edu.pl)
- Maja Chlipała (majachlipala@student.agh.edu.pl)
- Joanna Furtak (joannafurtak@student.agh.edu.pl)
- Julia Mikrut (mikrut@student.agh.edu.pl)
