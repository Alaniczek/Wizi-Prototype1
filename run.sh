#!/bin/bash

# Skrypt uruchomieniowy dla aplikacji GPT-4

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "Python 3 nie jest zainstalowany. Proszę zainstalować Python 3."
    exit 1
fi

# Ścieżka do głównego katalogu aplikacji
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$APP_DIR"

# Sprawdź czy środowisko wirtualne istnieje, jeśli nie, uruchom setup
if [ ! -d "venv" ]; then
    echo "Środowisko wirtualne nie istnieje. Uruchamiam konfigurację..."
    python3 app.py --setup
else
    # Aktywuj środowisko wirtualne i uruchom aplikację
    source venv/bin/activate
    python app.py
fi