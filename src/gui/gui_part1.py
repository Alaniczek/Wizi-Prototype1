#!/usr/bin/env python3
"""
GUI module for the GPT-4 Command Application - Part 1
Contains the main UI components and initialization
"""
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import json


class GptAppGUI:
    """Main GUI class for the GPT-4 Command Application"""
    
    # UI constants
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    PAD_X = 15
    PAD_Y = 15
    MAIN_FONT = ("Helvetica", 11)
    MONO_FONT = ("Consolas", 11)
    STATUS_FONT = ("Helvetica", 10)
    HEADER_FONT = ("Helvetica", 12, "bold")
    
    # Colors
    BG_COLOR = "#2c2c2c"
    FG_COLOR = "#ffffff"
    INPUT_BG = "#3c3c3c"
    INPUT_FG = "#ffffff"
    BUTTON_BG = "#404040"
    BUTTON_FG = "#ffffff"
    BUTTON_ACTIVE_BG = "#505050"
    ACCENT_COLOR = "#4a9eff"
    
    def __init__(self, root, config):
        """Initialize the application GUI"""
        self.root = root
        self.config = config
        self.selected_system = tk.StringVar(value=config.get("default_system", "Linux"))
        
        # Load chat prompts
        self.prompts = self._load_chat_prompts()
        
        # Configure the main window
        self._configure_root()
        
        # Create and arrange UI components
        self.create_widgets()
    
    def _load_chat_prompts(self):
        """Load chat prompts from JSON file"""
        try:
            prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "config", "ChatPrompt.json")
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading chat prompts: {e}")
            return None
    
    def _configure_root(self):
        """Configure the main application window"""
        self.root.title(self.prompts.get("window_titles", {}).get("main", "GPT-4 Aplikacja Komendowa"))
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.configure(bg=self.BG_COLOR)
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
    
    def create_widgets(self):
        """Create and arrange all UI components"""
        # Create main container frame with grid
        self.main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=self.PAD_X, pady=self.PAD_Y)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create sections
        self._create_header_section()
        self._create_input_section()
        self._create_system_selection()
        self._create_response_section()
        self._create_terminal_section()
        self._create_action_buttons()
        self._create_status_bar()
    
    def _create_header_section(self):
        """Create header with application title"""
        header_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, self.PAD_Y))
        
        title_label = tk.Label(
            header_frame,
            text="GPT-4 Command Assistant",
            font=self.HEADER_FONT,
            bg=self.BG_COLOR,
            fg=self.ACCENT_COLOR
        )
        title_label.pack()
    
    def _create_input_section(self):
        """Create the input field and related components"""
        input_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, self.PAD_Y))
        input_frame.grid_columnconfigure(0, weight=1)
        
        instruction_label = tk.Label(
            input_frame, 
            text=self.prompts.get("ui_labels", {}).get("input_instruction", 
                "Wprowadź polecenie (np. 'otwórz przeglądarkę', 'uruchom terminal'):"),
            font=self.MAIN_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        instruction_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        input_container = tk.Frame(input_frame, bg=self.INPUT_BG, bd=1, relief=tk.FLAT)
        input_container.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        input_container.grid_columnconfigure(0, weight=1)
        
        self.input_text = tk.Entry(
            input_container,
            font=self.MAIN_FONT,
            bg=self.INPUT_BG,
            fg=self.INPUT_FG,
            insertbackground=self.FG_COLOR,
            relief=tk.FLAT,
            bd=8
        )
        self.input_text.grid(row=0, column=0, sticky="ew")
        self.input_text.bind("<Return>", self.on_send)
        
        send_button = tk.Button(
            input_container, 
            text="Wyślij →",
            command=self.on_send,
            font=self.MAIN_FONT,
            bg=self.ACCENT_COLOR,
            fg=self.FG_COLOR,
            activebackground=self.BUTTON_ACTIVE_BG,
            activeforeground=self.FG_COLOR,
            relief=tk.FLAT,
            cursor="hand2",
            width=10,
            bd=8
        )
        send_button.grid(row=0, column=1)
    
    def _create_system_selection(self):
        """Create system selection radio buttons"""
        system_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        system_frame.grid(row=2, column=0, sticky="ew", pady=(0, self.PAD_Y))
        
        system_label = tk.Label(
            system_frame, 
            text=self.prompts.get("ui_labels", {}).get("system_selection", "System operacyjny:"),
            font=self.MAIN_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        system_label.pack(side=tk.LEFT, padx=(0, 15))
        
        systems = ["Linux", "Windows", "MacOS"]
        for system in systems:
            rb = tk.Radiobutton(
                system_frame, 
                text=system,
                variable=self.selected_system,
                value=system,
                font=self.MAIN_FONT,
                bg=self.BG_COLOR,
                fg=self.FG_COLOR,
                selectcolor=self.INPUT_BG,
                activebackground=self.BG_COLOR,
                activeforeground=self.ACCENT_COLOR,
                cursor="hand2"
            )
            rb.pack(side=tk.LEFT, padx=(0, 15))
    
    def _create_response_section(self):
        """Create the response text area"""
        response_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        response_frame.grid(row=3, column=0, sticky="nsew", pady=(0, self.PAD_Y))
        response_frame.grid_columnconfigure(0, weight=1)
        response_frame.grid_rowconfigure(1, weight=1)
        
        response_label = tk.Label(
            response_frame, 
            text=self.prompts.get("ui_labels", {}).get("gpt_response", "Odpowiedź GPT-4:"),
            font=self.MAIN_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        response_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.response_text = scrolledtext.ScrolledText(
            response_frame, 
            height=12,
            wrap=tk.WORD,
            font=self.MONO_FONT,
            bg=self.INPUT_BG,
            fg=self.INPUT_FG,
            insertbackground=self.FG_COLOR,
            bd=1,
            relief=tk.FLAT
        )
        self.response_text.grid(row=1, column=0, sticky="nsew")
        self.response_text.config(state=tk.DISABLED)
    
    def _create_terminal_section(self):
        """Create the terminal command field"""
        terminal_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        terminal_frame.grid(row=4, column=0, sticky="ew", pady=(0, self.PAD_Y))
        terminal_frame.grid_columnconfigure(0, weight=1)
        
        terminal_label = tk.Label(
            terminal_frame, 
            text=self.prompts.get("ui_labels", {}).get("command_to_execute", "Polecenie do wykonania:"),
            font=self.MAIN_FONT,
            bg=self.BG_COLOR,
            fg=self.FG_COLOR
        )
        terminal_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.terminal_text = scrolledtext.ScrolledText(
            terminal_frame,
            height=3,
            wrap=tk.WORD,
            font=self.MONO_FONT,
            bg=self.INPUT_BG,
            fg=self.INPUT_FG,
            insertbackground=self.FG_COLOR,
            bd=1,
            relief=tk.FLAT
        )
        self.terminal_text.grid(row=1, column=0, sticky="ew")
    
    def _create_action_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        button_frame.grid(row=5, column=0, sticky="ew", pady=(0, self.PAD_Y))
        
        execute_button = tk.Button(
            button_frame, 
            text=self.prompts.get("ui_labels", {}).get("execute_button", "▶ Wykonaj polecenie"),
            command=self.execute_command,
            font=self.MAIN_FONT,
            bg=self.ACCENT_COLOR,
            fg=self.FG_COLOR,
            activebackground=self.BUTTON_ACTIVE_BG,
            activeforeground=self.FG_COLOR,
            relief=tk.FLAT,
            cursor="hand2",
            width=20,
            bd=1
        )
        execute_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(
            button_frame, 
            text=self.prompts.get("ui_labels", {}).get("clear_button", "🗑 Wyczyść"),
            command=self.clear_fields,
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
        clear_button.pack(side=tk.LEFT)
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.FLAT, 
            anchor=tk.W,
            font=self.STATUS_FONT,
            bg=self.INPUT_BG,
            fg=self.FG_COLOR,
            pady=5,
            padx=10
        )
        status_bar.grid(row=1, column=0, sticky="ew")
        self.status_var.set(self.prompts.get("ui_labels", {}).get("status_ready", "Gotowy"))
    
    def on_send(self, event=None):
        """Handle sending a query to GPT-4"""
        query = self.input_text.get().strip()
        if not query:
            messagebox.showinfo("Informacja", 
                              self.prompts.get("error_messages", {}).get("empty_command", 
                                                                       "Wprowadź polecenie do przetworzenia"))
            return
        
        self.status_var.set(self.prompts.get("ui_labels", {}).get("status_sending", 
                                                                 "Wysyłanie zapytania do GPT-4..."))
        
        # Run query in a separate thread to avoid blocking the UI
        threading.Thread(target=self.process_query, args=(query,), daemon=True).start()