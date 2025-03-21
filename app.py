#!/usr/bin/env python3
"""
GPT-4 Command Application - Main Entry Point
"""
import os
import sys
import tkinter as tk
import subprocess
import importlib.util

# Constants
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")


def load_module(module_path, module_name):
    """Dynamically loads a module from a path"""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def is_running_in_venv():
    """Checks if the application is running in a virtual environment"""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


def get_python_path(venv_dir):
    """Returns the path to the Python executable in the virtual environment"""
    if sys.platform == 'win32':
        return os.path.join(venv_dir, 'Scripts', 'python')
    return os.path.join(venv_dir, 'bin', 'python')


def setup_environment(app_setup):
    """Sets up the virtual environment and dependencies"""
    print("Konfigurowanie aplikacji...")
    result = app_setup.AppSetup.setup()
    
    if not result:
        print("Konfiguracja nie powiodła się.")
        return False
        
    config, venv_dir = result
    print("Konfiguracja zakończona pomyślnie.")
    
    # Launch application in the virtual environment
    python_path = get_python_path(venv_dir)
    script_path = os.path.abspath(__file__)
    subprocess.run([python_path, script_path])
    return True


def load_gui_components():
    """Loads and combines GUI components"""
    gui_part1_path = os.path.join(SRC_DIR, "gui", "gui_part1.py")
    gui_part2_path = os.path.join(SRC_DIR, "gui", "gui_part2.py")
    
    # Import GUI modules
    gui_part1 = load_module(gui_part1_path, "gui_part1")
    gui_part2 = load_module(gui_part2_path, "gui_part2")
    
    # Combine methods from gui_part2 into the GptAppGUI class
    for name, method in gui_part2.__dict__.items():
        if callable(method) and not name.startswith('__'):
            setattr(gui_part1.GptAppGUI, name, method)
    
    return gui_part1.GptAppGUI


def main():
    """Main application function"""
    # Load app setup module
    app_setup_path = os.path.join(SRC_DIR, "config", "app_setup.py")
    app_setup = load_module(app_setup_path, "app_setup")
    
    # Check for setup argument
    if len(sys.argv) > 1 and sys.argv[1] == '--setup':
        return setup_environment(app_setup)
    
    # Check if running in virtual environment
    if not is_running_in_venv():
        return setup_environment(app_setup)
        
    
    # Load configuration
    config = app_setup.AppSetup.load_config()
    if not config:
        print("Błąd podczas ładowania konfiguracji.")
        return False
    
    # Initialize and run GUI
    GptAppGUI = load_gui_components()
    root = tk.Tk()
    app = GptAppGUI(root, config)
    root.mainloop()
    return True


if __name__ == "__main__":
    main()