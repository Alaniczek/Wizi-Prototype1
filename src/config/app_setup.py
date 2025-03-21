#!/usr/bin/env python3
"""
Application setup module for handling environment and configuration
"""
import os
import sys
import subprocess
import json

# Constants
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
API_PATH = os.path.join(PROJECT_ROOT, "api.txt")
VENV_DIR = os.path.join(PROJECT_ROOT, "venv")


class AppSetup:
    """Class responsible for application configuration and dependency installation"""
    
    REQUIRED_PACKAGES = ['openai', 'requests']
    
    @staticmethod
    def ensure_venv():
        """Ensures that the virtual environment exists and is activated"""
        # Check if virtual environment exists
        if not os.path.exists(VENV_DIR):
            print("Tworzenie środowiska wirtualnego...")
            try:
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
                print("Środowisko wirtualne zostało utworzone.")
            except subprocess.CalledProcessError:
                print("Błąd: Nie udało się utworzyć środowiska wirtualnego.")
                print("Spróbuj wykonać następujące polecenia ręcznie:")
                print("sudo apt install python3-venv")
                print("python3 -m venv venv")
                sys.exit(1)
        
        # Get pip path based on platform
        pip_path = os.path.join(VENV_DIR, 'Scripts' if sys.platform == 'win32' else 'bin', 'pip')
        return VENV_DIR, pip_path
    
    @staticmethod
    def install_dependencies(pip_path):
        """Installs required dependencies"""
        for package in AppSetup.REQUIRED_PACKAGES:
            try:
                print(f"Sprawdzanie pakietu {package}...")
                # Check if package is installed
                result = subprocess.run(
                    [pip_path, "show", package], 
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"Instalowanie pakietu {package}...")
                    subprocess.run([pip_path, "install", package], check=True)
                    print(f"Pakiet {package} został zainstalowany.")
                else:
                    print(f"Pakiet {package} jest już zainstalowany.")
            except subprocess.CalledProcessError:
                print(f"Błąd: Nie udało się zainstalować pakietu {package}.")
                return False
        
        return True
    
    @staticmethod
    def read_api_key():
        """Reads API key from the api.txt file if it exists"""
        if not os.path.exists(API_PATH):
            return ""
            
        with open(API_PATH, 'r') as f:
            lines = f.readlines()
            return lines[0].strip() if lines else ""
    
    @staticmethod
    def create_default_config():
        """Creates default configuration if it doesn't exist"""
        # Make sure config directory exists
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        # Read API key if available
        api_key = AppSetup.read_api_key()
        
        # Default configuration
        default_config = {
            "api_key": api_key,
            "model": "gpt-4o-mini",
            "store": True,
            "default_system": "Linux"
        }
        
        # Write configuration to file
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        print(f"Utworzono domyślny plik konfiguracyjny: {CONFIG_PATH}")
        return default_config
    
    @staticmethod
    def load_config():
        """Loads configuration or creates default if it doesn't exist"""
        # Create default configuration if it doesn't exist
        if not os.path.exists(CONFIG_PATH):
            return AppSetup.create_default_config()
        
        # Load configuration
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Błąd podczas ładowania konfiguracji: {str(e)}")
            return None

    @staticmethod
    def setup():
        """Performs full application setup"""
        venv_dir, pip_path = AppSetup.ensure_venv()
        
        if not AppSetup.install_dependencies(pip_path):
            return False
        
        config = AppSetup.load_config()
        if not config:
            return False
        
        return config, venv_dir