#!/usr/bin/env python3
"""
Utility functions for the GPT-4 Command Application
"""
import os
import sys
import json
import importlib.util


def import_from_path(module_name, file_path):
    """
    Dynamically import a module from a given file path
    
    Args:
        module_name (str): Name to assign to the imported module
        file_path (str): Absolute path to the module file
        
    Returns:
        module: The imported module object
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def get_platform_info():
    """
    Get detailed information about the current operating system
    
    Returns:
        dict: Dictionary with platform information including system type,
              Python version, and text encoding
    """
    platform_info = {
        'system': sys.platform,
        'python_version': sys.version,
        'encoding': sys.getdefaultencoding()
    }
    
    # Determine platform type based on sys.platform
    if sys.platform == 'win32':
        platform_info['platform_type'] = 'Windows'
    elif sys.platform == 'darwin':
        platform_info['platform_type'] = 'MacOS'
    elif sys.platform.startswith('linux'):
        platform_info['platform_type'] = 'Linux'
    else:
        platform_info['platform_type'] = 'Unknown'
        
    return platform_info


def handle_error(error_message, exit_on_error=False):
    """
    Handle application errors with consistent formatting
    
    Args:
        error_message (str): The error message to display
        exit_on_error (bool): Whether to exit the application after displaying the error
        
    Returns:
        bool: False if the application continues, otherwise exits
    """
    print(f"[ERROR] {error_message}")
    
    if exit_on_error:
        sys.exit(1)
    
    return False


def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, create it if it doesn't
    
    Args:
        directory_path (str): Path to the directory to check/create
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
        return True
    except OSError as e:
        handle_error(f"Failed to create directory {directory_path}: {str(e)}")
        return False


def load_json(file_path: str) -> dict:
    """
    Load and parse a JSON file
    
    Args:
        file_path (str): Path to the JSON file to load
        
    Returns:
        dict: Parsed JSON content, or empty dict if file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        handle_error(f"Failed to load JSON file {file_path}: {str(e)}")
        return {}