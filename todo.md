# Planowanie Aplikacji: Otwieranie Innej Aplikacji przy użyciu API GPT-4

## 1. Przegląd
- [x] **Cel:** Stworzyć aplikację, która odczytuje dane wejściowe użytkownika, używa API GPT-4 do określenia, którą aplikację otworzyć, a następnie otwiera odpowiednią aplikację.
- [x] **Kluczowe Komponenty:**
    - [x] Proste GUI
    - [x] Integracja z API GPT-4
    - [x] Uruchamianie komend w terminalu
    - [x] Potwierdzenie wykonania zadania

## 2. Wymagania
- [x] **Oprogramowanie:**
    - [x] Python
    - [x] Biblioteki do wykonywania żądań HTTP (np. requests)
    - [x] Biblioteki do tworzenia GUI (np. Tkinter)
- [x] **API:** Dostęp do API GPT-4 oraz klucz API
- [x] **Środowisko:** Linux

## 3. Konfiguracja
### 3.1. Konfiguracja Środowiska
- [x] Zainstalować wymaganą wersję Pythona oraz potrzebne biblioteki
- [x] Bezpiecznie przechowywać klucz API GPT-4 przy użyciu zmiennych środowiskowych
- [x] Dodać plik `.gitignore` i umieścić w nim klucz API, aby nie był przechowywany w repozytorium

### 3.2. Struktura Projektu
- [x] Główny plik aplikacji (np. app.py)
- [x] Plik konfiguracyjny (np. config.json)
- [x] Moduły pomocnicze (np. input_handler.py, gui.py)
- [x] Dokumentacja i planowanie projektu (todo.md)

## 4. Tworzenie GUI
### 4.1. Projektowanie Interfejsu
- [x] Zaimplementować prosty interfejs użytkownika przy użyciu Tkinter
- [x] Dodanie pola tekstowego do wprowadzania danych przez użytkownika
- [x] Dodanie przycisku do wysyłania danych do API GPT-4

### 4.2. Obsługa Wejścia i Wyjścia
- [x] Przechwytywanie danych wejściowych z pola tekstowego
- [x] Wyświetlanie odpowiedzi z API GPT-4 w interfejsie użytkownika
- [x] Potwierdzenie wykonania zadania

## 5. Integracja z API GPT-4
### 5.1. Konstruowanie Żądania API
- [x] Zdefiniować endpoint, nagłówki i strukturę payloadu
- [x] Dołączyć dane wejściowe użytkownika do żądania

### 5.2. Obsługa Odpowiedzi API
- [x] Analizować odpowiedź, aby wyodrębnić informację o aplikacji do otwarcia
- [x] Zarządzać błędami API oraz przekroczeniem limitów czasu

## 6. Uruchamianie Komend w Terminalu
### 6.1. Mapowanie Odpowiedzi na Komendy
- [x] Utworzyć mapowanie słów kluczowych z odpowiedzi na odpowiednie komendy terminala

### 6.2. Wykonywanie Komend
- [x] Użyć wywołań systemowych (np. subprocess w Pythonie) do uruchomienia komend w terminalu
- [x] Potwierdzenie wykonania zadania

## 7. Obsługa Błędów i Logowanie
### 7.1. Zarządzanie Błędami Systemowymi i API
- [x] Zaimplementować bloki try-except dla krytycznych funkcji
- [x] Logować błędy w celu ułatwienia diagnostyki problemów

### 7.2. Informacje Zwrotne dla Użytkownika
- [x] Zapewnić użytkownikowi czytelne komunikaty dotyczące sukcesu lub niepowodzenia operacji

## 8. Testowanie i Wdrażanie
### 8.1. Testy Jednostkowe
- [ ] Napisać testy dla funkcji obsługi wejścia, integracji API oraz uruchamiania komend

### 8.2. Testy Integracyjne
- [ ] Przeprowadzić symulację przepływu (end-to-end) od wejścia użytkownika do wykonania komendy

### 8.3. Rozważenia Dotyczące Wdrożenia
- [x] Skonfigurować CI/CD (ciągła integracja/ciągłe wdrażanie), jeśli to możliwe
- [x] Zapewnić właściwą konfigurację środowiska na maszynach wdrożeniowych

## 9. Przyszłe Ulepszenia
- [ ] Rozważyć dodanie rozpoznawania głosu dla lepszego doświadczenia użytkownika
- [ ] Rozbudować system obsługi błędów oraz logowanie operacji