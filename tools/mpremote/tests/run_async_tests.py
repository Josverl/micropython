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

"""Test runner for async transport implementation.

Runs all async-related tests in a cross-platform way.
"""

import os
import sys
import subprocess
from pathlib import Path


# ANSI color codes (work on most platforms including Windows 10+)
GREEN = '\033[0;32m'
RED = '\033[0;31m'
RESET = '\033[0m'

# Fallback for systems without color support
try:
    # Test if color output works
    if not sys.stdout.isatty() or os.name == 'nt' and not os.environ.get('TERM'):
        GREEN = RED = RESET = ''
except:
    GREEN = RED = RESET = ''


def run_test(test_name: str, test_file: Path) -> bool:
    """Run a single test file.
    
    Args:
        test_name: Human-readable name of the test
        test_file: Path to the test file
        
    Returns:
        bool: True if test passed, False otherwise
    """
    print("-" * 72)
    print(f"Running: {test_name}")
    print("-" * 72)
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=test_file.parent.parent,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"{GREEN}✓ {test_name} PASSED{RESET}")
            print()
            return True
        else:
            print(f"{RED}✗ {test_name} FAILED{RESET}")
            print()
            return False
    except Exception as e:
        print(f"{RED}✗ {test_name} FAILED with exception: {e}{RESET}")
        print()
        return False


def main():
    """Main test runner."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    
    print("=" * 72)
    print("RUNNING ALL ASYNC TRANSPORT TESTS")
    print("=" * 72)
    print()
    
    # Define tests to run
    tests = [
        ("Basic Async Transport Tests", script_dir / "test_async_transport.py"),
        ("Comprehensive Async Tests", script_dir / "test_async_comprehensive.py"),
        ("Integration Tests", script_dir / "test_integration.py"),
    ]
    
    # Run all tests
    results = []
    for test_name, test_file in tests:
        if not test_file.exists():
            print(f"{RED}✗ Test file not found: {test_file}{RESET}")
            results.append(False)
            continue
        results.append(run_test(test_name, test_file))
    
    # Summary
    print("=" * 72)
    print("TEST SUMMARY")
    print("=" * 72)
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if passed_tests == total_tests:
        print(f"{GREEN}✓ ALL TESTS PASSED{RESET}")
        print("=" * 72)
        return 0
    else:
        print(f"{RED}✗ SOME TESTS FAILED{RESET}")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(main())
