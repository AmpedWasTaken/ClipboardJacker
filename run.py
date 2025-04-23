from clipreplacer import ClipReplacer
import logging

# Set logging to ERROR level for silent mode
logging.getLogger().setLevel(logging.ERROR)

replacer = ClipReplacer("config.json")
replacer.monitor_clipboard()