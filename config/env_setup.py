import os
import json
import subprocess

def install_dependencies():
    """
    Instaluje wymagane zależności dla aplikacji.
    W przypadku Kali Linux, używa odpowiednich metod instalacji.
    """
    try:
        # Sprawdź, czy OpenAI jest zainstalowane
        import openai
        print("Biblioteka OpenAI jest już zainstalowana.")
    except ImportError:
        print("Instalacja biblioteki OpenAI...")
        # W przypadku Kali Linux, spróbuj utworzyć środowisko wirtualne
        try:
            subprocess.run(["python3", "-m", "venv", "venv"], check=True)
            subprocess.run(["./venv/bin/pip", "install", "openai"], check=True)
            print("Biblioteka OpenAI została zainstalowana w środowisku wirtualnym.")
            print("Użyj './venv/bin/python app.py' aby uruchomić aplikację.")
        except subprocess.CalledProcessError:
            print("Nie udało się zainstalować biblioteki OpenAI automatycznie.")
            print("Spróbuj ręcznie utworzyć środowisko wirtualne:")
            print("1. python3 -m venv venv")
            print("2. source venv/bin/activate")
            print("3. pip install openai")

def load_config():
    """
    Wczytuje konfigurację z pliku config.json.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku konfiguracyjnego pod ścieżką {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Błąd: Nieprawidłowy format pliku JSON w {config_path}")
        return None

def get_api_key():
    """
    Pobiera klucz API z pliku konfiguracyjnego lub ze zmiennych środowiskowych.
    """
    # Najpierw sprawdź zmienne środowiskowe
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # Jeśli nie znaleziono w zmiennych środowiskowych, sprawdź plik konfiguracyjny
    config = load_config()
    if config and "api_key" in config:
        return config["api_key"]
    
    print("Błąd: Nie znaleziono klucza API. Ustaw zmienną środowiskową OPENAI_API_KEY lub dodaj klucz do pliku config.json.")
    return None

if __name__ == "__main__":
    install_dependencies()
    api_key = get_api_key()
    if api_key:
        print("Konfiguracja środowiska zakończona pomyślnie.")
        print(f"Znaleziono klucz API: {api_key[:5]}...{api_key[-5:]}")
    else:
        print("Konfiguracja środowiska zakończona z błędami.")