# Project Structure

## Directory Layout

```
.
├── app.py              # Main application entry point
├── run.sh             # Shell script for easy startup
├── config/            # Configuration files
│   ├── ChatPrompt.json       # Chat system messages and prompts
│   ├── config.json          # Main application configuration
│   ├── environment.json     # Environment and dependency settings
│   └── env_setup.py        # Environment setup utilities
├── src/               # Source code
│   ├── config/           # Configuration management
│   │   └── app_setup.py  # Application setup and initialization
│   ├── gui/             # GUI components
│   │   ├── gui_part1.py # Main GUI layout and widgets
│   │   └── gui_part2.py # GUI event handlers and processing
│   └── utils/           # Utility modules
│       ├── cache_manager.py # Caching functionality
│       └── utils.py        # General utility functions
└── logs/              # Application logs
```

## Component Description

### Main Components

1. **app.py**
   - Application entry point
   - Handles virtual environment checks
   - Initializes GUI and configuration

2. **run.sh**
   - Shell script for easy application startup
   - Handles virtual environment activation
   - Runs setup if needed

### Configuration (config/)

1. **ChatPrompt.json**
   - System messages for different OS
   - Error message templates
   - Chat response formatting

2. **config.json**
   - API configuration
   - Model settings
   - Default system settings

3. **environment.json**
   - Required packages
   - System dependencies
   - Python version requirements
   - Logging configuration

### Source Code (src/)

1. **GUI Module (gui/)**
   - `gui_part1.py`: Main window layout and widgets
   - `gui_part2.py`: Event handlers and command processing

2. **Configuration Management (config/)**
   - `app_setup.py`: Application initialization and setup

3. **Utilities (utils/)**
   - `cache_manager.py`: Caching system
   - `utils.py`: Helper functions and platform detection

## Data Flow

1. User input → GUI
2. GUI → Command Processing
3. Command Processing → API Request
4. API Response → Command Translation
5. Command Translation → Output Display

## Configuration Flow

1. Application Start
2. Environment Check
3. Virtual Environment Setup (if needed)
4. Configuration Loading
5. GUI Initialization

## Error Handling

- Environment setup errors
- API communication errors
- Command processing errors
- Configuration errors

## Development Tools

- pytest for testing
- black for code formatting
- pylint for code analysis
- mypy for type checking