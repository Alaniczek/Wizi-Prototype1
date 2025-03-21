# Wizi - GPT Terminal Command Assistant

Inteligentny asystent komend terminalowych wykorzystujący GPT-4 do tłumaczenia poleceń na komendy systemowe.

## 🌟 Funkcje

- Tłumaczenie poleceń w języku naturalnym na komendy systemowe
- Wsparcie dla systemów Linux, Windows i MacOS
- Intuicyjny interfejs graficzny
- Osobne okna dla komend i odpowiedzi AI
- Automatyczna konfiguracja środowiska

## 📋 Wymagania

- Python 3.8 lub nowszy
- Dostęp do internetu (dla API OpenAI)
- System operacyjny: Linux, Windows lub MacOS

## 🚀 Szybka instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/Alaniczek/Wizi.git
cd Wizi
```

2. Uruchom aplikację:
```bash
python3 app.py
```

Aplikacja automatycznie skonfiguruje wszystkie potrzebne zależności przy pierwszym uruchomieniu.

## ⚙️ Konfiguracja

1. Utwórz plik `config.json` w katalogu `config` z następującą zawartością:
```json
{
    "api_key": "twój-klucz-api-openai",
    "model": "gpt-4o-mini",
    "default_system": "Linux"
}
```

2. Upewnij się, że masz zainstalowane wymagane pakiety:
```bash
pip install -r requirements.txt
```

## 🎯 Jak używać

1. Uruchom aplikację komendą `python3 app.py`
2. W polu wprowadzania wpisz polecenie w języku naturalnym (np. "utwórz folder na pulpicie")
3. Kliknij "Submit" lub wciśnij Enter
4. Odpowiedź pojawi się w dwóch oknach:
   - Okno "Chat": Opis wykonanej operacji i pytanie o następne działanie
   - Okno "Komenda": Dokładna komenda systemowa do wykonania

## 🔧 Rozwiązywanie problemów

- **Problem z konfiguracją:** Uruchom `python3 app.py --setup`
- **Brak klucza API:** Upewnij się, że plik `config.json` zawiera prawidłowy klucz API
- **Błędy zależności:** Uruchom `pip install -r requirements.txt`

## 🤝 Jak przyczynić się do rozwoju

1. Zrób fork repozytorium
2. Utwórz nową gałąź dla swojej funkcji (`git checkout -b feature/AmazingFeature`)
3. Zatwierdź zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Wypchnij do gałęzi (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📝 Licencja

Ten projekt jest objęty licencją MIT - szczegóły w pliku [LICENSE](LICENSE)

## ✨ Autor

Alaniczek - [GitHub](https://github.com/Alaniczek)

## 🙏 Podziękowania

- OpenAI za API GPT-4
- Społeczność Python za świetne narzędzia
- Wszystkim kontrybutorem projektu