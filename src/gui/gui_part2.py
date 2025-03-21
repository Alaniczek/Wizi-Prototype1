"""
GUI module for the GPT-4 Command Application - Part 2
Contains the command processing and result display functionality
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading


def process_query(self, query):
    """Process a user query in a separate thread"""
    try:
        # Dynamically import OpenAI for better error handling
        from openai import OpenAI
        
        # Get configuration values
        api_key = self.config.get("api_key", "")
        if not api_key:
            self._handle_missing_api_key()
            return
        
        model = self.config.get("model", "gpt-4o-mini")
        store = self.config.get("store", True)
        selected_system = self.selected_system.get()
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Create system message based on selected operating system
        system_message = self._create_system_message(selected_system)
        
        # Send request to API
        completion = self._send_api_request(client, model, store, system_message, query)
        
        # Process response
        response = completion.choices[0].message.content
        self._update_ui_with_response(response, selected_system)
        
    except ImportError:
        self._handle_openai_import_error()
    except Exception as e:
        self._handle_general_error(str(e))

def _send_api_request(self, client, model, store, system_message, query):
    """Send request to OpenAI API"""
    return client.chat.completions.create(
        model=model,
        store=store,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
    )

def _create_system_message(self, selected_system):
    """Create system message based on selected operating system"""
    if not self.prompts:
        # Fallback if prompts couldn't be loaded
        return self._create_fallback_system_message(selected_system)
    
    system_messages = self.prompts.get("system_messages", {})
    base_message = system_messages.get("base", "").format(system=selected_system)
    system_specific = system_messages.get(selected_system, "")
    suffix = system_messages.get("suffix", "")
    
    return f"{base_message} {system_specific} {suffix}"

def _create_fallback_system_message(self, selected_system):
    """Create fallback system message if prompts are not available"""
    base_message = f"Jesteś asystentem, który pomaga tłumaczyć polecenia użytkownika na komendy terminala systemu {selected_system}. "
    
    if selected_system == "Linux":
        base_message += "Odpowiadaj komendami dla systemu Linux, używając bash."
    elif selected_system == "Windows":
        base_message += "Odpowiadaj komendami dla systemu Windows, używając CMD lub PowerShell."
    elif selected_system == "MacOS":
        base_message += "Odpowiadaj komendami dla systemu MacOS, używając terminala bash/zsh."
    
    base_message += " Odpowiadaj tylko komendą, bez żadnych dodatkowych wyjaśnień."
    return base_message

def _update_ui_with_response(self, response, selected_system):
    """Update UI elements with API response"""
    self.root.after(0, self.update_response, response)
    self.root.after(0, self.update_terminal, response)
    status_message = self.prompts.get("ui_labels", {}).get("status_ready", "Gotowy")
    self.root.after(0, self.update_status, f"{status_message} - Otrzymano odpowiedź dla systemu {selected_system}")

def _handle_missing_api_key(self):
    """Handle missing API key error"""
    self.update_status(self.prompts.get("ui_labels", {}).get("status_error", "Błąd: Brak klucza API"))
    
    error_window = tk.Toplevel(self.root)
    error_window.title("Błąd konfiguracji")
    error_window.geometry("400x200")
    error_window.configure(bg=self.BG_COLOR)
    error_window.resizable(False, False)
    
    # Configure grid
    error_window.grid_columnconfigure(0, weight=1)
    
    # Add error icon
    error_label = tk.Label(
        error_window,
        text="⚠️",
        font=("Helvetica", 48),
        bg=self.BG_COLOR,
        fg="#ff4444"
    )
    error_label.grid(row=0, column=0, pady=(20, 10))
    
    # Add error message
    message_label = tk.Label(
        error_window,
        text=self.prompts.get("error_messages", {}).get("missing_api_key", 
            "Brak klucza API w pliku konfiguracyjnym."),
        font=self.MAIN_FONT,
        bg=self.BG_COLOR,
        fg=self.FG_COLOR,
        wraplength=350
    )
    message_label.grid(row=1, column=0, padx=20, pady=(0, 20))
    
    # Add OK button
    ok_button = tk.Button(
        error_window,
        text="OK",
        command=error_window.destroy,
        font=self.MAIN_FONT,
        bg=self.ACCENT_COLOR,
        fg=self.FG_COLOR,
        activebackground=self.BUTTON_ACTIVE_BG,
        activeforeground=self.FG_COLOR,
        relief=tk.FLAT,
        cursor="hand2",
        width=10
    )
    ok_button.grid(row=2, column=0, pady=(0, 20))

def _handle_openai_import_error(self):
    """Handle OpenAI import error"""
    self.root.after(0, self.update_status, "Błąd: Biblioteka OpenAI nie jest zainstalowana")
    self.root.after(0, lambda: messagebox.showerror(
        "Błąd", 
        self.prompts.get("error_messages", {}).get("openai_not_installed", 
            "Biblioteka OpenAI nie jest zainstalowana. Uruchom aplikację ponownie z opcją --setup")
    ))

def _handle_general_error(self, error_message):
    """Handle general errors"""
    status_error = self.prompts.get("ui_labels", {}).get("status_error", "Błąd podczas przetwarzania zapytania")
    self.root.after(0, self.update_status, status_error)
    self.root.after(0, lambda: messagebox.showerror("Błąd", f"Wystąpił błąd: {error_message}"))

def update_response(self, text):
    """Update response text area"""
    self.response_text.config(state=tk.NORMAL)
    self.response_text.delete(1.0, tk.END)
    self.response_text.insert(tk.END, text)
    self.response_text.config(state=tk.DISABLED)

def update_terminal(self, text):
    """Update terminal command field"""
    self.terminal_text.delete(1.0, tk.END)  # Changed from 0 to 1.0 for ScrolledText
    command = text.strip().split('\n')[0]
    self.terminal_text.insert(tk.END, command)

def update_status(self, text):
    """Update status bar"""
    self.status_var.set(text)

def execute_command(self):
    """Execute terminal command"""
    command = self.terminal_text.get(1.0, tk.END).strip()  # Changed from get() to get(1.0, tk.END)
    if not command:
        messagebox.showinfo(
            "Informacja", 
            self.prompts.get("error_messages", {}).get("empty_command", "Wprowadź polecenie do wykonania")
        )
        return
    
    try:
        status_executing = self.prompts.get("ui_labels", {}).get("status_executing", "Wykonywanie: {command}")
        self.status_var.set(status_executing.format(command=command))
        
        # Execute command in background
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Start thread to monitor command execution
        threading.Thread(
            target=self.monitor_command, 
            args=(process, command), 
            daemon=True
        ).start()
        
    except Exception as e:
        status_error = self.prompts.get("ui_labels", {}).get("status_error", "Błąd podczas wykonywania polecenia")
        self.status_var.set(status_error)
        messagebox.showerror("Błąd", f"Nie udało się wykonać polecenia: {str(e)}")

def monitor_command(self, process, command):
    """Monitor command execution in a separate thread"""
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    
    # Update UI in main thread
    if exit_code == 0:
        self.root.after(0, self.command_success, stdout)
    else:
        self.root.after(0, self.command_error, stderr)

def command_success(self, output):
    """Handle successful command execution"""
    status_success = self.prompts.get("ui_labels", {}).get("status_success", "Polecenie wykonane pomyślnie")
    self.status_var.set(status_success)
    
    # Display result in enlarged dialog
    if output.strip():
        self._show_result_window(
            self.prompts.get("window_titles", {}).get("result", "Wynik polecenia"),
            output
        )

def command_error(self, error):
    """Handle command execution error"""
    status_error = self.prompts.get("ui_labels", {}).get("status_error", "Błąd podczas wykonywania polecenia")
    self.status_var.set(status_error)
    self._show_error_window(
        self.prompts.get("window_titles", {}).get("error", "Błąd polecenia"),
        error
    )

def _show_result_window(self, title, content):
    """Show a customized result window"""
    result_window = self._create_output_window(title, content)
    result_window.focus_set()

def _show_error_window(self, title, content):
    """Show a customized error window"""
    error_window = self._create_output_window(title, content, error=True)
    error_window.focus_set()

def _create_output_window(self, title, content, error=False):
    """Create a customized output window"""
    output_window = tk.Toplevel(self.root)
    output_window.title(title)
    output_window.geometry("800x500")
    output_window.configure(bg=self.BG_COLOR)
    output_window.minsize(600, 400)
    
    # Configure grid
    output_window.grid_columnconfigure(0, weight=1)
    output_window.grid_rowconfigure(1, weight=1)
    
    # Add title label
    title_label = tk.Label(
        output_window,
        text=title,
        font=self.HEADER_FONT,
        bg=self.BG_COLOR,
        fg=self.ACCENT_COLOR
    )
    title_label.grid(row=0, column=0, sticky="w", padx=self.PAD_X, pady=(self.PAD_Y, self.PAD_Y//2))
    
    # Create container frame for content
    content_frame = tk.Frame(output_window, bg=self.BG_COLOR)
    content_frame.grid(row=1, column=0, sticky="nsew", padx=self.PAD_X, pady=(0, self.PAD_Y))
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)
    
    # Add text area with scrollbar
    bg_color = "#3c2c2c" if error else self.INPUT_BG
    output_text = scrolledtext.ScrolledText(
        content_frame,
        wrap=tk.WORD,
        font=self.MONO_FONT,
        bg=bg_color,
        fg=self.FG_COLOR,
        insertbackground=self.FG_COLOR,
        bd=1,
        relief=tk.FLAT
    )
    output_text.grid(row=0, column=0, sticky="nsew")
    
    # Add content
    output_text.insert(tk.END, content)
    output_text.config(state=tk.DISABLED)
    
    # Add button frame
    button_frame = tk.Frame(output_window, bg=self.BG_COLOR)
    button_frame.grid(row=2, column=0, sticky="ew", padx=self.PAD_X, pady=(0, self.PAD_Y))
    
    # Add close button
    close_button = tk.Button(
        button_frame,
        text=self.prompts.get("ui_labels", {}).get("close_button", "✖ Zamknij"),
        command=output_window.destroy,
        font=self.MAIN_FONT,
        bg=self.BUTTON_BG,
        fg=self.FG_COLOR,
        activebackground=self.BUTTON_ACTIVE_BG,
        activeforeground=self.FG_COLOR,
        relief=tk.FLAT,
        cursor="hand2",
        width=15,
        bd=1
    )
    close_button.pack(side=tk.RIGHT)
    
    # Add copy button
    copy_button = tk.Button(
        button_frame,
        text="📋 Kopiuj",
        command=lambda: self._copy_to_clipboard(output_text.get(1.0, tk.END)),
        font=self.MAIN_FONT,
        bg=self.ACCENT_COLOR,
        fg=self.FG_COLOR,
        activebackground=self.BUTTON_ACTIVE_BG,
        activeforeground=self.FG_COLOR,
        relief=tk.FLAT,
        cursor="hand2",
        width=15,
        bd=1
    )
    copy_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    return output_window

def _copy_to_clipboard(self, text):
    """Copy text to clipboard"""
    self.root.clipboard_clear()
    self.root.clipboard_append(text)
    self.root.update()

def clear_fields(self):
    """Clear all text fields"""
    self.input_text.delete(0, tk.END)
    self.terminal_text.delete(1.0, tk.END)  # Changed from 0 to 1.0 for ScrolledText
    self.response_text.config(state=tk.NORMAL)
    self.response_text.delete(1.0, tk.END)
    self.response_text.config(state=tk.DISABLED)
    status_ready = self.prompts.get("ui_labels", {}).get("status_ready", "Gotowy")
    self.status_var.set(status_ready)