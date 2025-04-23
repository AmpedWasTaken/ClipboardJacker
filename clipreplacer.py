#!/usr/bin/env python3

import json
import re
import time
import argparse
import logging
from typing import List, Dict, Optional
import pyperclip

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

class Pattern:
    def __init__(self, regex: str, replace_with: str):
        self.regex = re.compile(regex)
        self.replace_with = replace_with

class ClipReplacer:
    def __init__(self, config_path: str):
        """Initialize the ClipReplacer with patterns from config file."""
        self.patterns: List[Pattern] = []
        self.last_text: Optional[str] = None
        self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load patterns from the config file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            self.patterns = [
                Pattern(p["regex"], p["replace_with"])
                for p in config["patterns"]
            ]
            logger.info(f"Loaded {len(self.patterns)} patterns from {config_path}")
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {config_path}")
            raise
        except KeyError:
            logger.error(f"Invalid config format in: {config_path}")
            raise

    def process_text(self, text: str) -> str:
        """Process text through all patterns and return modified text."""
        if not text:
            return text

        original_text = text
        for pattern in self.patterns:
            text = pattern.regex.sub(pattern.replace_with, text)

        if text != original_text:
            logger.info("[!] Match found. Replacing...")
            logger.info(f"    Old: {original_text}")
            logger.info(f"    New: {text}")

        return text

    def monitor_clipboard(self) -> None:
        """Monitor clipboard for changes and apply replacements."""
        logger.info("ClipReplacer is now monitoring your clipboard...")
        logger.info("Press Ctrl+C to stop")

        while True:
            try:
                current_text = pyperclip.paste()
                
                # Only process if text has changed and isn't None
                if current_text is not None and current_text != self.last_text:
                    processed_text = self.process_text(current_text)
                    
                    # Only update clipboard if text was modified
                    if processed_text != current_text:
                        pyperclip.copy(processed_text)
                        self.last_text = processed_text
                    else:
                        self.last_text = current_text

                time.sleep(0.1)  # Prevent high CPU usage
                
            except KeyboardInterrupt:
                logger.info("\nStopping clipboard monitor...")
                break
            except Exception as e:
                logger.error(f"Error processing clipboard: {str(e)}")
                time.sleep(1)  # Pause on error to prevent spam

def main():
    parser = argparse.ArgumentParser(description="Monitor and replace clipboard text based on regex patterns.")
    parser.add_argument('--config', default='config.json', help='Path to config file (default: config.json)')
    args = parser.parse_args()

    try:
        replacer = ClipReplacer(args.config)
        replacer.monitor_clipboard()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main()) 