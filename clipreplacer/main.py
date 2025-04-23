#!/usr/bin/env python3

import argparse
import logging
from .clipreplacer import ClipReplacer

def main():
    parser = argparse.ArgumentParser(description="Monitor and replace clipboard text based on regex patterns.")
    parser.add_argument('--config', default='config.json', help='Path to config file (default: config.json)')
    parser.add_argument('--rate-limit', type=int, default=5, help='Minimum seconds between replacements (default: 5)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                      help='Set the logging level (default: INFO)')
    parser.add_argument('--silent', action='store_true', help='Run in silent mode (no output except errors)')
    args = parser.parse_args()

    # Set logging level
    if args.silent:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(args.log_level)

    try:
        replacer = ClipReplacer(args.config, args.rate_limit)
        if not args.silent:
            logging.info("ClipReplacer is now monitoring your clipboard...")
            logging.info("Press Ctrl+C to stop")
        replacer.monitor_clipboard()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main()) 