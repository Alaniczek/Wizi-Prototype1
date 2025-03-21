#!/bin/bash

# Skrypt uruchomieniowy dla aplikacji Wizi

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "Python 3 nie jest zainstalowany. Proszę zainstalować Python 3."
    exit 1
fi

# Ścieżka do głównego katalogu aplikacji
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$APP_DIR"

# Instalacja zależności (jeśli nie są zainstalowane)
if [ ! -f ".dependencies_installed" ]; then
    echo "Instalacja wymaganych pakietów..."
    pip install -r requirements.txt
    touch .dependencies_installed
fi

# Uruchom aplikację
python3 app.py "$@"