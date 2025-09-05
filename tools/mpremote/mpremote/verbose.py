"""
Global verbosity control for mpremote.

Provides centralized verbose printing functionality with three levels:
- 0: quiet (suppress all non-essential output)
- 1: normal (current default behavior)  
- 2: verbose/debug (show additional debug information)
"""

import sys

# Global verbosity level
# 0 = quiet, 1 = normal, 2 = verbose/debug
_verbosity_level = 1


def set_verbosity_level(level):
    """Set the global verbosity level.
    
    Args:
        level (int): 0=quiet, 1=normal, 2=verbose/debug
    """
    global _verbosity_level
    _verbosity_level = level


def get_verbosity_level():
    """Get the current verbosity level."""
    return _verbosity_level


def verbose_print(message, **kwargs):
    """Print a message only if not in quiet mode, to stderr.
    
    Prints for verbosity levels 1 (normal) and 2 (verbose/debug).
    """
    if _verbosity_level >= 1:
        print(message, file=sys.stderr, **kwargs)


def debug_print(message, **kwargs):
    """Print a debug message only in verbose/debug mode, to stderr.
    
    Prints only for verbosity level 2 (verbose/debug).
    """
    if _verbosity_level >= 2:
        print(message, file=sys.stderr, **kwargs)


def is_quiet():
    """Check if we're in quiet mode."""
    return _verbosity_level == 0


def is_verbose():
    """Check if we're in verbose/debug mode."""
    return _verbosity_level >= 2