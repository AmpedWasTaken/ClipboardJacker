#!/usr/bin/env python3

import json
import re
import time
import logging
import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import pyperclip
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class PatternStats:
    matches: int = 0
    last_match: Optional[datetime.datetime] = None
    total_chars_replaced: int = 0

@dataclass
class Pattern:
    regex: re.Pattern
    replace_with: str
    description: str
    priority: int
    enabled: bool
    stats: PatternStats = field(default_factory=PatternStats)

    @classmethod
    def from_dict(cls, pattern_dict: Dict) -> 'Pattern':
        try:
            regex = re.compile(pattern_dict["regex"])
            return cls(
                regex=regex,
                replace_with=pattern_dict["replace_with"],
                description=pattern_dict.get("description", "No description"),
                priority=pattern_dict.get("priority", 0),
                enabled=pattern_dict.get("enabled", True)
            )
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {str(e)}")

class ClipReplacer:
    def __init__(self, config_path: str = None, rate_limit: int = 5):
        """Initialize the ClipReplacer with patterns from config file."""
        self.patterns: List[Pattern] = []
        self.last_text: Optional[str] = None
        self.last_replacement_time: Optional[datetime.datetime] = None
        self.rate_limit = rate_limit  # Minimum seconds between replacements
        self.clipboard_history: List[Tuple[str, datetime.datetime]] = []
        self.max_history_size = 10
        
        if config_path:
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load patterns from the config file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            self.patterns = [
                Pattern.from_dict(p)
                for p in config["patterns"]
            ]
            # Sort patterns by priority (higher priority first)
            self.patterns.sort(key=lambda x: x.priority, reverse=True)
            logger.info(f"Loaded {len(self.patterns)} patterns from {config_path}")
            
            # Validate all patterns
            self.validate_patterns()
            
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {config_path}")
            raise
        except KeyError:
            logger.error(f"Invalid config format in: {config_path}")
            raise

    def add_pattern(self, pattern: Pattern) -> None:
        """Add a pattern to the replacer."""
        self.patterns.append(pattern)
        self.patterns.sort(key=lambda x: x.priority, reverse=True)
        self.validate_patterns()

    def validate_patterns(self) -> None:
        """Validate all patterns and log any issues."""
        for pattern in self.patterns:
            try:
                # Test pattern with empty string
                pattern.regex.sub(pattern.replace_with, "")
                logger.debug(f"Pattern validated: {pattern.description}")
            except Exception as e:
                logger.error(f"Invalid pattern '{pattern.description}': {str(e)}")
                pattern.enabled = False

    def can_replace(self) -> bool:
        """Check if we can perform a replacement based on rate limiting."""
        if self.last_replacement_time is None:
            return True
            
        time_since_last = (datetime.datetime.now() - self.last_replacement_time).total_seconds()
        return time_since_last >= self.rate_limit

    def backup_clipboard(self, text: str) -> None:
        """Store clipboard content in history."""
        self.clipboard_history.append((text, datetime.datetime.now()))
        if len(self.clipboard_history) > self.max_history_size:
            self.clipboard_history.pop(0)

    def process_text(self, text: str) -> str:
        """Process text through all patterns and return modified text."""
        if not text:
            return text

        if not self.can_replace():
            logger.debug("Rate limit reached, skipping replacement")
            return text

        original_text = text
        for pattern in self.patterns:
            if not pattern.enabled:
                continue
                
            new_text = pattern.regex.sub(pattern.replace_with, text)
            if new_text != text:
                # Update pattern statistics
                pattern.stats.matches += 1
                pattern.stats.last_match = datetime.datetime.now()
                pattern.stats.total_chars_replaced += len(text) - len(new_text)
                
                text = new_text
                if logger.getEffectiveLevel() <= logging.INFO:
                    logger.info(f"[!] Match found with pattern: {pattern.description}")
                    logger.info(f"    Old: {original_text}")
                    logger.info(f"    New: {text}")
                    logger.info(f"    Pattern: {pattern.regex.pattern}")
                    logger.info(f"    Priority: {pattern.priority}")
                    logger.info(f"    Total matches: {pattern.stats.matches}")
                
                # Backup original content
                self.backup_clipboard(original_text)
                self.last_replacement_time = datetime.datetime.now()
                break  # Stop after first match (highest priority)

        return text

    def print_statistics(self) -> None:
        """Print statistics about pattern matches."""
        logger.info("\nPattern Statistics:")
        logger.info("=================")
        for pattern in self.patterns:
            logger.info(f"\nPattern: {pattern.description}")
            logger.info(f"Status: {'Enabled' if pattern.enabled else 'Disabled'}")
            logger.info(f"Priority: {pattern.priority}")
            logger.info(f"Total matches: {pattern.stats.matches}")
            if pattern.stats.last_match:
                logger.info(f"Last match: {pattern.stats.last_match}")
            logger.info(f"Total chars replaced: {pattern.stats.total_chars_replaced}")

    def monitor_clipboard(self) -> None:
        """Monitor clipboard for changes and apply replacements."""
        if logger.getEffectiveLevel() <= logging.INFO:
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
                if logger.getEffectiveLevel() <= logging.INFO:
                    logger.info("\nStopping clipboard monitor...")
                break
            except Exception as e:
                logger.error(f"Error processing clipboard: {str(e)}")
                time.sleep(1)  # Pause on error to prevent spam 