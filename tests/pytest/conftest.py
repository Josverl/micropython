"""
Pytest configuration for MicroPython REPL tests.

Simplified version adapted from tools/mpremote/tests/conftest.py
for testing MicroPython unix port REPL behavior.
"""

import os
from pathlib import Path

import pytest


def pytest_report_header(config):
    """Add test information to the pytest header."""
    return ["MicroPython REPL Tests"]


@pytest.fixture(scope="session")
def micropython_path():
    """
    Fixture that provides the path to the MicroPython unix executable.

    Defaults to ports/unix/build-standard/micropython relative to repo root.
    Can be overridden with MICROPYTHON_PATH environment variable.
    """
    env_path = os.environ.get("MICROPYTHON_PATH", "")
    if env_path and os.path.exists(env_path):
        return env_path

    # Default path relative to MicroPython repository root
    # tests/pytest -> tests -> micropython root
    tests_pytest_dir = Path(__file__).parent
    tests_dir = tests_pytest_dir.parent
    micropython_root = tests_dir.parent
    default_path = micropython_root / "ports" / "unix" / "build-standard" / "micropython"

    if not default_path.exists():
        pytest.skip(f"MicroPython not found at {default_path}. Build it or set MICROPYTHON_PATH.")

    return str(default_path)


def pytest_configure(config):
    """Register custom markers and configure test collection."""
    config.addinivalue_line("markers", "repl: mark test as requiring REPL interaction")
    config.addinivalue_line("markers", "unicode: mark test as testing unicode behavior")

    # Configure pytest to collect pytest_*.py files instead of test_*.py
    config.addinivalue_line("python_files", "pytest_*.py")
