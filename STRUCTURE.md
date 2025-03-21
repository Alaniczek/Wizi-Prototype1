# Wizi - Struktura Projektu

## 🗂️ Układ katalogów

```
.
├── app.py                 # Główny punkt wejścia aplikacji
├── run.sh                # Skrypt ułatwiający uruchomienie
├── requirements.txt      # Zależności projektu
├── config/              # Pliki konfiguracyjne
│   ├── ChatPrompt.json   # Szablony wiadomości systemowych
│   ├── config.json      # Główna konfiguracja (API, model)
│   └── env_setup.py     # Konfiguracja środowiska
├── src/                 # Kod źródłowy
│   ├── config/          # Zarządzanie konfiguracją
│   │   └── app_setup.py # Inicjalizacja aplikacji
│   ├── gui/             # Interfejs użytkownika
│   │   ├── gui_part1.py # Układ i widżety GUI
│   │   └── gui_part2.py # Obsługa zdarzeń GUI
│   └── utils/           # Narzędzia pomocnicze
│       └── utils.py     # Funkcje pomocnicze
└── logs/               # Logi aplikacji
```

## 🔨 Komponenty

### 1. Główne komponenty

#### `app.py`
- Punkt wejścia aplikacji
- Zarządzanie środowiskiem wirtualnym
- Inicjalizacja GUI i konfiguracji

#### `run.sh`
- Skrypt pomocniczy do uruchamiania
- Aktywacja środowiska wirtualnego
- Automatyczna konfiguracja

### 2. Konfiguracja (`config/`)

#### `ChatPrompt.json`
```json
{
    "system_messages": {
        "base": "Format wiadomości bazowej",
        "Linux": "Format dla Linux",
        "Windows": "Format dla Windows",
        "MacOS": "Format dla MacOS"
    }
}
```

#### `config.json`
```json
{
    "api_key": "klucz-api",
    "model": "model-gpt",
    "default_system": "system-operacyjny"
}
```

### 3. Kod źródłowy (`src/`)

#### GUI (`gui/`)
- `gui_part1.py`: Layout i komponenty
- `gui_part2.py`: Logika i obsługa zdarzeń

#### Konfiguracja (`config/`)
- `app_setup.py`: Inicjalizacja aplikacji

#### Narzędzia (`utils/`)
- `utils.py`: Funkcje pomocnicze

## 🔄 Przepływ danych

1. Input użytkownika → GUI
2. GUI → Przetwarzanie komend
3. Przetwarzanie → Zapytanie API
4. Odpowiedź API → Konwersja komendy
5. Konwersja → Wyświetlenie wyniku

## 🚀 Proces uruchomienia

1. Sprawdzenie środowiska
2. Konfiguracja (jeśli potrzebna)
3. Wczytanie konfiguracji
4. Inicjalizacja GUI

## ⚠️ Obsługa błędów

- Błędy konfiguracji środowiska
- Błędy komunikacji z API
- Błędy przetwarzania komend
- Błędy GUI

## 🧪 Rozwój

### Narzędzia
- pytest do testów
- black do formatowania
- pylint do analizy
- mypy do sprawdzania typów

### Dodawanie nowych funkcji
1. Utwórz nową gałąź
2. Dodaj testy
3. Zaimplementuj funkcję
4. Zaktualizuj dokumentację
5. Utwórz Pull Request