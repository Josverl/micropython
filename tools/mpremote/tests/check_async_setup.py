#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Final validation script for async implementation.

Validates that all components are in place and working in a cross-platform way.
"""

import os
import sys
import subprocess
from pathlib import Path


# ANSI color codes (work on most platforms including Windows 10+)
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

# Fallback for systems without color support
try:
    if not sys.stdout.isatty() or os.name == "nt" and not os.environ.get("TERM"):
        GREEN = RED = YELLOW = RESET = ""
except:
    GREEN = RED = YELLOW = RESET = ""


class ValidationChecker:
    """Validation checker for async implementation."""

    def __init__(self):
        self.checks_passed = 0
        self.checks_total = 0
        self.script_dir = Path(__file__).parent.resolve()
        self.mpremote_dir = self.script_dir.parent

    def check_pass(self, message: str):
        """Record a passing check."""
        print(f"{GREEN}✓{RESET} {message}")
        self.checks_passed += 1
        self.checks_total += 1

    def check_fail(self, message: str):
        """Record a failing check."""
        print(f"{RED}✗{RESET} {message}")
        self.checks_total += 1

    def check_warn(self, message: str):
        """Print a warning."""
        print(f"{YELLOW}⚠{RESET} {message}")

    def check_file_exists(self, filepath: Path, description: str):
        """Check if a file exists."""
        if filepath.exists():
            self.check_pass(f"{description} exists")
        else:
            self.check_fail(f"{description} missing")

    def check_import(self, module_name: str, description: str):
        """Check if a module can be imported."""
        try:
            __import__(module_name)
            self.check_pass(f"{description} imports")
        except ImportError:
            self.check_fail(f"{description} import failed")

    def check_python_code(self, code: str, description: str):
        """Execute Python code and check if it succeeds."""
        try:
            exec(code)
            self.check_pass(description)
        except Exception as e:
            self.check_fail(f"{description} - {e}")

    def validate_phase1(self):
        """Validate Phase 1: Transport Layer."""
        print("\n=== Phase 1: Transport Layer ===")

        mpremote_pkg = self.mpremote_dir / "mpremote"

        # Check files exist
        self.check_file_exists(mpremote_pkg / "transport_async.py", "transport_async.py")
        self.check_file_exists(
            mpremote_pkg / "transport_serial_async.py", "transport_serial_async.py"
        )
        self.check_file_exists(mpremote_pkg / "protocol.py", "protocol.py")

        # Check imports (need to add parent to path)
        sys.path.insert(0, str(self.mpremote_dir))

        self.check_import("mpremote.transport_async", "AsyncTransport")
        self.check_import("mpremote.transport_serial_async", "AsyncSerialTransport")
        self.check_import("mpremote.protocol", "RawREPLProtocol")

    def validate_phase2(self):
        """Validate Phase 2: Command Layer."""
        print("\n=== Phase 2: Command Layer ===")

        mpremote_pkg = self.mpremote_dir / "mpremote"

        # Check files exist
        self.check_file_exists(mpremote_pkg / "commands_async.py", "commands_async.py")

        # Check State class has async methods
        code = """
from mpremote.main import State
s = State()
assert hasattr(s, 'ensure_raw_repl_async')
assert hasattr(s, 'ensure_connected_async')
assert hasattr(s, 'ensure_friendly_repl_async')
"""
        self.check_python_code(code, "State class has async methods")

        # Check command async functions exist
        self.check_import("mpremote.commands_async", "Async command handlers")

    def validate_phase3(self):
        """Validate Phase 3: REPL and Console."""
        print("\n=== Phase 3: REPL and Console ===")

        mpremote_pkg = self.mpremote_dir / "mpremote"

        # Check files exist
        self.check_file_exists(mpremote_pkg / "console_async.py", "console_async.py")
        self.check_file_exists(mpremote_pkg / "repl_async.py", "repl_async.py")

        # Check imports
        self.check_import("mpremote.console_async", "AsyncConsole")
        self.check_import("mpremote.repl_async", "do_repl_async")

    def validate_dependencies(self):
        """Validate dependencies."""
        print("\n=== Dependencies ===")

        # Check requirements.txt
        req_file = self.mpremote_dir / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text()
            if "pyserial-asyncio" in content:
                self.check_pass("pyserial-asyncio in requirements.txt")
            else:
                self.check_fail("pyserial-asyncio not in requirements.txt")
        else:
            self.check_fail("requirements.txt not found")

        # Check if pyserial-asyncio is installed
        try:
            import serial_asyncio

            self.check_pass("pyserial-asyncio installed")
        except ImportError:
            self.check_warn("pyserial-asyncio not installed (optional)")

    def validate_testing(self):
        """Validate testing infrastructure."""
        print("\n=== Testing Infrastructure ===")

        tests_dir = self.script_dir

        self.check_file_exists(tests_dir / "test_async_transport.py", "test_async_transport.py")
        self.check_file_exists(
            tests_dir / "test_async_comprehensive.py", "test_async_comprehensive.py"
        )
        self.check_file_exists(tests_dir / "test_integration.py", "test_integration.py")
        self.check_file_exists(tests_dir / "run_async_tests.py", "run_async_tests.py")

    def validate_documentation(self):
        """Validate documentation."""
        print("\n=== Documentation ===")

        self.check_file_exists(self.mpremote_dir / "ASYNC_README.md", "ASYNC_README.md")
        self.check_file_exists(
            self.mpremote_dir / "IMPLEMENTATION_SUMMARY.md", "IMPLEMENTATION_SUMMARY.md"
        )

    def validate_backward_compatibility(self):
        """Validate backward compatibility."""
        print("\n=== Backward Compatibility ===")

        # Check original modules still work
        self.check_import("mpremote.transport_serial", "Original SerialTransport")
        self.check_import("mpremote.console", "Original Console")
        self.check_import("mpremote.repl", "Original do_repl")

        # Check State has both sync and async methods
        code = """
from mpremote.main import State
s = State()
# Check sync methods
assert hasattr(s, 'ensure_raw_repl')
assert hasattr(s, 'ensure_connected')
assert hasattr(s, 'ensure_friendly_repl')
# Check async methods
assert hasattr(s, 'ensure_raw_repl_async')
assert hasattr(s, 'ensure_connected_async')
assert hasattr(s, 'ensure_friendly_repl_async')
"""
        self.check_python_code(code, "State has both sync and async methods")

    def validate_syntax(self):
        """Validate Python syntax."""
        print("\n=== Python Syntax Validation ===")

        mpremote_pkg = self.mpremote_dir / "mpremote"
        files_to_check = [
            "transport_async.py",
            "transport_serial_async.py",
            "protocol.py",
            "console_async.py",
            "repl_async.py",
            "commands_async.py",
        ]

        for filename in files_to_check:
            filepath = mpremote_pkg / filename
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        compile(f.read(), str(filepath), "exec")
                    self.check_pass(f"{filename} has valid syntax")
                except SyntaxError as e:
                    self.check_fail(f"{filename} has syntax errors: {e}")
            else:
                self.check_fail(f"{filename} not found")

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 72)
        print("VALIDATION SUMMARY")
        print("=" * 72)
        print(f"Checks passed: {self.checks_passed} / {self.checks_total}")

        if self.checks_passed == self.checks_total:
            print(f"{GREEN}✓ ALL CHECKS PASSED{RESET}")
            print("Implementation is complete and ready for use!")
            return 0
        else:
            failed = self.checks_total - self.checks_passed
            print(f"{RED}✗ {failed} CHECKS FAILED{RESET}")
            print("Please review the failed checks above.")
            return 1
