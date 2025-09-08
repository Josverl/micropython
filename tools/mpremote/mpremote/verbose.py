"""
Global verbosity control for mpremote using Python standard logging.

Provides centralized verbose printing functionality with three levels:
- 0: quiet (suppress all non-essential output, show only WARNING and above)
- 1: normal (show INFO and above, suppress DEBUG)  
- 2: verbose/debug (show all levels including DEBUG)
"""

import logging
import sys

# Create logger for mpremote
_logger = logging.getLogger('mpremote')

# Create handler to output to stderr
_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter('%(message)s'))
_logger.addHandler(_handler)

# Prevent propagation to root logger to avoid duplicate output
_logger.propagate = False

# Set default level to INFO (normal mode)
_logger.setLevel(logging.INFO)

# Track current verbosity level for backward compatibility
_verbosity_level = 1


def set_verbosity_level(level):
    """Set the global verbosity level.
    
    Args:
        level (int): 0=quiet, 1=normal, 2=verbose/debug
    """
    global _verbosity_level
    _verbosity_level = level
    
    if level == 0:  # quiet mode
        _logger.setLevel(logging.WARNING)
    elif level == 1:  # normal mode
        _logger.setLevel(logging.INFO)
    elif level >= 2:  # verbose/debug mode
        _logger.setLevel(logging.DEBUG)


def get_verbosity_level():
    """Get the current verbosity level."""
    return _verbosity_level


def verbose_print(message, **kwargs):
    """Print a message only if not in quiet mode, to stderr.
    
    Prints for verbosity levels 1 (normal) and 2 (verbose/debug).
    """
    # Use logging.info for normal verbose output
    _logger.info(message)


def debug_print(message, **kwargs):
    """Print a debug message only in verbose/debug mode, to stderr.
    
    Prints only for verbosity level 2 (verbose/debug).
    """
    # Use logging.debug for debug output
    _logger.debug(message)


def is_quiet():
    """Check if we're in quiet mode."""
    return _verbosity_level == 0


def is_verbose():
    """Check if we're in verbose/debug mode."""
    return _verbosity_level >= 2