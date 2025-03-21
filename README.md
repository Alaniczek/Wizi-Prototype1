# GPT Terminal Command Assistant

A Python application that helps translate natural language commands into terminal commands for different operating systems (Linux, Windows, MacOS).

## Features

- Natural language to terminal command translation
- Support for multiple operating systems (Linux, Windows, MacOS)
- User-friendly GUI interface
- Command history and output display
- Automatic virtual environment setup
- Configuration management
- Error handling and logging

## Requirements

- Python 3.8 or higher
- Operating system: Linux, Windows, or MacOS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Wizi.git
cd Wizi
```

2. Run the setup script:
```bash
# On Linux/MacOS
./run.sh

# On Windows
python app.py --setup
```

The setup script will:
- Create a virtual environment
- Install required dependencies
- Configure the application

## Configuration

1. Create a `config.json` in the `config` directory with your OpenAI API key:
```json
{
    "api_key": "your-api-key-here",
    "model": "gpt-4o-mini",
    "default_system": "Linux"
}
```

2. Optional: Customize other settings in the configuration files under the `config` directory.

## Usage

1. Start the application:
```bash
# On Linux/MacOS
./run.sh

# On Windows
python app.py
```

2. Enter your command in natural language in the input field
3. Click "Submit" or press Enter
4. The translated terminal command will appear in the output field

## Development

The project uses several development tools:
- pytest for testing
- black for code formatting
- pylint for code analysis
- mypy for type checking

To set up the development environment:
```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request