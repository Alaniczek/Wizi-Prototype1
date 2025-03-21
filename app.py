#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import json

# Katalog główny projektu
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class AppSetup:
    """Klasa odpowiedzialna za konfigurację aplikacji i instalację zależności"""
    
    @staticmethod
    def ensure_venv():
        """Upewnia się, że środowisko wirtualne istnieje i jest aktywowane"""
        venv_dir = os.path.join(PROJECT_ROOT, "venv")
        
        # Sprawdź czy środowisko wirtualne istnieje
        if not os.path.exists(venv_dir):
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
        
        # Ścieżka do pip w środowisku wirtualnym
        if sys.platform == 'win32':
            pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
        else:
            pip_path = os.path.join(venv_dir, 'bin', 'pip')
        
        return venv_dir, pip_path
    
    @staticmethod
    def install_dependencies(pip_path):
        """Instaluje wymagane zależności"""
        packages = ['openai', 'requests']
        
        for package in packages:
            try:
                print(f"Sprawdzanie pakietu {package}...")
                # Sprawdź czy pakiet jest zainstalowany
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
    def load_config():
        """Ładuje konfigurację lub tworzy domyślną, jeśli nie istnieje"""
        config_dir = os.path.join(PROJECT_ROOT, "config")
        config_path = os.path.join(config_dir, "config.json")
        
        # Upewnij się, że katalog config istnieje
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        # Jeśli plik konfiguracyjny nie istnieje, stwórz domyślny
        if not os.path.exists(config_path):
            # Sprawdź czy istnieje plik api.txt
            api_path = os.path.join(PROJECT_ROOT, "api.txt")
            api_key = ""
            
            if os.path.exists(api_path):
                with open(api_path, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        api_key = lines[0].strip()
            
            default_config = {
                "api_key": api_key,
                "model": "gpt-4o-mini",
                "store": True
            }
            
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            print(f"Utworzono domyślny plik konfiguracyjny: {config_path}")
        
        # Załaduj konfigurację
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Błąd podczas ładowania konfiguracji: {str(e)}")
            return None

    @staticmethod
    def setup():
        """Przeprowadza pełną konfigurację aplikacji"""
        venv_dir, pip_path = AppSetup.ensure_venv()
        
        if not AppSetup.install_dependencies(pip_path):
            return False
        
        config = AppSetup.load_config()
        if not config:
            return False
        
        return config, venv_dir

class GptAppGUI:
    def __init__(self, root, config):
        self.root = root
        self.root.title("GPT-4 Aplikacja Komendowa")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        self.config = config
        
        # Tworzenie interfejsu
        self.create_widgets()
    
    def create_widgets(self):
        # Ramka główna
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Etykieta wprowadzająca
        instruction_label = tk.Label(
            main_frame, 
            text="Wprowadź polecenie (np. 'otwórz przeglądarkę', 'uruchom terminal'):"
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Pole tekstowe do wprowadzania zapytania
        self.input_text = tk.Entry(main_frame, width=50)
        self.input_text.pack(fill=tk.X, pady=(0, 10))
        self.input_text.bind("<Return>", self.on_send)
        
        # Przycisk do wysyłania zapytania
        send_button = tk.Button(
            main_frame, 
            text="Wyślij", 
            command=self.on_send
        )
        send_button.pack(anchor=tk.W, pady=(0, 10))
        
        # Etykieta dla odpowiedzi
        response_label = tk.Label(main_frame, text="Odpowiedź GPT-4:")
        response_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Pole tekstowe do wyświetlania odpowiedzi
        self.response_text = scrolledtext.ScrolledText(
            main_frame, 
            width=80, 
            height=10, 
            wrap=tk.WORD
        )
        self.response_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.response_text.config(state=tk.DISABLED)
        
        # Etykieta dla poleceń terminala
        terminal_label = tk.Label(main_frame, text="Polecenie do wykonania:")
        terminal_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Pole tekstowe do wyświetlania poleceń terminala
        self.terminal_text = tk.Entry(main_frame, width=50)
        self.terminal_text.pack(fill=tk.X, pady=(0, 5))
        
        # Przyciski akcji
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        execute_button = tk.Button(
            action_frame, 
            text="Wykonaj polecenie", 
            command=self.execute_command
        )
        execute_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(
            action_frame, 
            text="Wyczyść", 
            command=self.clear_fields
        )
        clear_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Gotowy")
    
    def on_send(self, event=None):
        """Obsługuje wysłanie zapytania do GPT-4"""
        query = self.input_text.get().strip()
        if not query:
            messagebox.showinfo("Informacja", "Wprowadź polecenie do przetworzenia")
            return
        
        self.status_var.set("Wysyłanie zapytania do GPT-4...")
        
        # Uruchamiamy zapytanie w osobnym wątku, aby nie blokować interfejsu
        threading.Thread(target=self.process_query, args=(query,), daemon=True).start()
    
    def process_query(self, query):
        """Przetwarza zapytanie w osobnym wątku"""
        try:
            # Dynamiczne importowanie OpenAI dla lepszej obsługi błędów
            from openai import OpenAI
            
            api_key = self.config.get("api_key", "")
            if not api_key:
                self.update_status("Błąd: Brak klucza API")
                self.root.after(0, lambda: messagebox.showerror(
                    "Błąd konfiguracji", 
                    "Brak klucza API w pliku konfiguracyjnym."
                ))
                return
            
            model = self.config.get("model", "gpt-4o-mini")
            store = self.config.get("store", True)
            
            # Inicjalizacja klienta OpenAI
            client = OpenAI(api_key=api_key)
            
            # Wysłanie zapytania do API
            completion = client.chat.completions.create(
                model=model,
                store=store,
                messages=[
                    {"role": "system", "content": "Jesteś asystentem, który pomaga tłumaczyć polecenia użytkownika na komendy terminala Linux. Odpowiadaj tylko komendą, bez żadnych dodatkowych wyjaśnień."},
                    {"role": "user", "content": query}
                ]
            )
            
            # Przetwarzanie odpowiedzi
            response = completion.choices[0].message.content
            
            # Aktualizacja interfejsu w głównym wątku
            self.root.after(0, self.update_response, response)
            self.root.after(0, self.update_terminal, response)
            self.root.after(0, self.update_status, "Gotowy - Otrzymano odpowiedź")
            
        except ImportError:
            self.root.after(0, self.update_status, "Błąd: Biblioteka OpenAI nie jest zainstalowana")
            self.root.after(0, lambda: messagebox.showerror(
                "Błąd", 
                "Biblioteka OpenAI nie jest zainstalowana. Uruchom aplikację ponownie z opcją --setup"
            ))
        except Exception as e:
            # Obsługa błędów
            error_message = f"Wystąpił błąd: {str(e)}"
            self.root.after(0, self.update_status, "Błąd podczas przetwarzania zapytania")
            self.root.after(0, lambda: messagebox.showerror("Błąd", error_message))
    
    def update_response(self, text):
        """Aktualizuje pole odpowiedzi"""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, text)
        self.response_text.config(state=tk.DISABLED)
    
    def update_terminal(self, text):
        """Aktualizuje pole polecenia terminala"""
        # Czyścimy pole i dodajemy nowe polecenie
        # Zakładamy, że pierwszy wiersz odpowiedzi to polecenie
        command = text.strip().split('\n')[0]
        self.terminal_text.delete(0, tk.END)
        self.terminal_text.insert(0, command)
    
    def update_status(self, text):
        """Aktualizuje pasek statusu"""
        self.status_var.set(text)
    
    def execute_command(self):
        """Wykonuje polecenie w terminalu"""
        command = self.terminal_text.get().strip()
        if not command:
            messagebox.showinfo("Informacja", "Wprowadź polecenie do wykonania")
            return
        
        try:
            self.status_var.set(f"Wykonywanie: {command}")
            
            # Wykonanie polecenia w tle
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Uruchomienie wątku do monitorowania wyniku
            threading.Thread(
                target=self.monitor_command, 
                args=(process, command), 
                daemon=True
            ).start()
            
        except Exception as e:
            self.status_var.set("Błąd podczas wykonywania polecenia")
            messagebox.showerror("Błąd", f"Nie udało się wykonać polecenia: {str(e)}")
    
    def monitor_command(self, process, command):
        """Monitoruje wykonanie polecenia w osobnym wątku"""
        stdout, stderr = process.communicate()
        exit_code = process.returncode
        
        # Aktualizacja interfejsu w głównym wątku
        if exit_code == 0:
            self.root.after(0, self.command_success, stdout)
        else:
            self.root.after(0, self.command_error, stderr)
    
    def command_success(self, output):
        """Obsługuje pomyślne wykonanie polecenia"""
        self.status_var.set("Polecenie wykonane pomyślnie")
        if output.strip():
            messagebox.showinfo("Wynik polecenia", output)
    
    def command_error(self, error):
        """Obsługuje błąd wykonania polecenia"""
        self.status_var.set("Błąd podczas wykonywania polecenia")
        messagebox.showerror("Błąd polecenia", error)
    
    def clear_fields(self):
        """Czyści pola tekstowe"""
        self.input_text.delete(0, tk.END)
        self.terminal_text.delete(0, tk.END)
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state=tk.DISABLED)
        self.status_var.set("Gotowy")

def main():
    """Główna funkcja aplikacji"""
    
    # Sprawdź czy podano argument --setup
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        print("Konfigurowanie aplikacji...")
        result = AppSetup.setup()
        if result:
            config, venv_dir = result
            print("Konfiguracja zakończona pomyślnie.")
            
            # Uruchom aplikację w środowisku wirtualnym
            if sys.platform == 'win32':
                python_path = os.path.join(venv_dir, 'Scripts', 'python')
            else:
                python_path = os.path.join(venv_dir, 'bin', 'python')
            
            script_path = os.path.abspath(__file__)
            subprocess.run([python_path, script_path])
            return
        else:
            print("Konfiguracja nie powiodła się.")
            return
    
    # Sprawdź czy jesteśmy w środowisku wirtualnym
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Aplikacja nie jest uruchomiona w środowisku wirtualnym.")
        print("Uruchom 'python app.py --setup' aby skonfigurować środowisko.")
        
        # Opcjonalnie można tu dodać automatyczne uruchomienie setupu
        response = input("Czy chcesz teraz skonfigurować środowisko? (tak/nie): ").lower()
        if response in ('tak', 't', 'y', 'yes'):
            result = AppSetup.setup()
            if result:
                config, venv_dir = result
                print("Konfiguracja zakończona pomyślnie.")
                
                # Uruchom aplikację w środowisku wirtualnym
                if sys.platform == 'win32':
                    python_path = os.path.join(venv_dir, 'Scripts', 'python')
                else:
                    python_path = os.path.join(venv_dir, 'bin', 'python')
                
                script_path = os.path.abspath(__file__)
                subprocess.run([python_path, script_path])
                return
            else:
                print("Konfiguracja nie powiodła się.")
                return
        else:
            return
    
    # Załaduj konfigurację
    config = AppSetup.load_config()
    if not config:
        print("Błąd podczas ładowania konfiguracji.")
        return
    
    # Uruchom aplikację
    root = tk.Tk()
    app = GptAppGUI(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()