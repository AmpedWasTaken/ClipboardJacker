#!/usr/bin/env python3

import argparse
import logging
from .clipboardjacker import ClipboardJacker, Config

def run_clipboard_jacker():
    parser = argparse.ArgumentParser(description="Monitor and replace clipboard text based on regex patterns.")
    parser.add_argument('--config', default='config.json', help='Path to config file (default: config.json)')
    parser.add_argument('--rate-limit', type=int, default=5, help='Minimum seconds between replacements (default: 5)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Set the logging level (default: INFO)')
    parser.add_argument('--silent', action='store_true', help='Run in silent mode (no output except errors)')
    parser.add_argument('--version', action='store_true', help='Show version and exit')
    args = parser.parse_args()

    if args.version:
        print(f"ClipboardJacker version {ClipboardJacker.get_version()}")
        return 0

    # Create config from CLI args
    config = Config(
        rate_limit=args.rate_limit,
        log_level=args.log_level,
        silent=args.silent
    )
    
    try:
        jacker = ClipboardJacker(args.config if args.config != 'config.json' else config)
        if not args.silent:
            logging.info(f"ClipboardJacker v{ClipboardJacker.get_version()} is now monitoring your clipboard...")
            logging.info("Press Ctrl+C to stop")
        jacker.monitor_clipboard()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(run_clipboard_jacker()) 