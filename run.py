from clipboardjacker import ClipboardJacker, Config

# Create config directly in code
config = Config(
    patterns=[
        {
            "regex": r"example\.com",
            "replace_with": "replacement.com",
            "description": "Replace example.com links",
            "priority": 1,
            "enabled": True
        }
    ],
    rate_limit=5,
    log_level="INFO",
    silent=False
)

# Initialize and run
jacker = ClipboardJacker(config)
jacker.monitor_clipboard()