"""
Shared utilities for MicroPython REPL tests.

Helper functions for interacting with MicroPython REPL via pexpect.
"""

import sys


def requires_pexpect():
    """
    Decorator to skip tests if pexpect is not available.

    Usage:
        @requires_pexpect
        class TestClass:
            ...
    """
    try:
        import pytest
        import pexpect

        return lambda func: func
    except ImportError:
        import pytest

        return pytest.mark.skip(reason="pexpect is required for REPL tests")


def requires_unix():
    """
    Decorator to skip tests on Windows (PTY support required).

    Usage:
        @requires_unix
        class TestClass:
            ...
    """
    try:
        import pytest

        if sys.platform == "win32":
            return pytest.mark.skip(reason="PTY tests only work on Unix-like systems")
        return lambda func: func
    except ImportError:
        return lambda func: func
