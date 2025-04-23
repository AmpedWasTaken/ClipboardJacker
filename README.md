# ClipboardJacker

A configurable clipboard monitoring tool that automatically replaces text matching specified regex patterns with configured replacements.

## Features

- Real-time clipboard monitoring
- Regex-based text replacement
- Configurable via JSON file
- Cross-platform support
- Detailed logging of replacements
- Command-line configuration support

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the package:
```bash
pip install -e .
```

## Usage

1. Configure your patterns in `config.json`:
```json
{
  "patterns": [
    {
      "regex": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
      "replace_with": "redacted@example.com"
    }
  ]
}
```

2. Run the program:
```bash
clipboardjacker
```

Or specify a custom config file:
```bash
clipboardjacker --config custom_config.json
```

## Example Use Cases

- Redact email addresses
- Replace sensitive information with placeholders
- Standardize text formats
- Replace Bitcoin addresses with dummy values
- Mask IP addresses

## Disclaimer

This tool modifies your clipboard contents based on the configured patterns. Please review your configuration carefully and use at your own risk. Always verify the replaced text before using it in sensitive contexts.

## License

MIT License
