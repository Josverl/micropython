#!/usr/bin/env python3
"""
Simple test for MicroPython REPL interaction.

Tests basic REPL functionality and Unicode handling (issue #7585).

Usage:
    pytest test_repl_simple.py -v
    MICROPYTHON_PATH=/path/to/micropython pytest test_repl_simple.py -v
"""

import time

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for REPL tests")

# Timing constants for REPL interaction
REPL_STARTUP_DELAY = 0.2  # Time to let REPL settle after startup
REPL_COMMAND_DELAY = 0.3  # Time to wait after sending command
REPL_SHORT_DELAY = 0.1  # Short delay for quick operations


@pytest.fixture
def repl(micropython_path):
    """
    Fixture that provides a MicroPython REPL session.

    Handles startup, cleanup, and graceful exit.
    Yields the pexpect child process ready at the >>> prompt.
    """
    child = pexpect.spawn(micropython_path, encoding="utf-8", timeout=10)

    try:
        # Wait for initial prompt
        index = child.expect([">>>", pexpect.TIMEOUT, pexpect.EOF], timeout=5)
        if index != 0:
            pytest.fail(f"No initial prompt. Output: {child.before!r}")

        time.sleep(REPL_STARTUP_DELAY)
        yield child

    finally:
        # Graceful exit: try os._exit(0), then Ctrl-D, then terminate
        if child.isalive():
            try:
                child.sendline("import os")
                time.sleep(REPL_SHORT_DELAY)
                child.expect([">>>", pexpect.TIMEOUT], timeout=2)
                child.sendline("os._exit(0)")
                time.sleep(REPL_STARTUP_DELAY)
            except:
                pass

        if child.isalive():
            try:
                child.sendcontrol("d")
                time.sleep(REPL_STARTUP_DELAY)
            except:
                pass

        if child.isalive():
            try:
                child.terminate(force=True)
            except:
                pass

        child.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=2)
        child.close()


def send_and_expect(repl, command, expected, timeout=3):
    """
    Helper to send command and verify expected output.

    Returns the output before the expected match.
    """
    import re

    repl.sendline(command)
    time.sleep(REPL_COMMAND_DELAY)

    # Use re.escape for expected to handle special regex characters
    escaped_expected = re.escape(expected)

    index = repl.expect([escaped_expected, pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    if index != 0:
        pytest.fail(f"Expected '{expected}'. Got: {repl.before!r}")

    output = repl.before + expected

    # Wait for next prompt
    index = repl.expect([">>>", pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    if index != 0:
        pytest.fail(f"No prompt after command. Got: {repl.before!r}")

    return output


@pytest.mark.repl
@pytest.mark.parametrize(
    "command,expected",
    [
        ('print("Hello repl test")', "Hello repl test"),
        ("2 + 3", "5"),
        pytest.param(
            'print("München")',
            "München",
            marks=pytest.mark.unicode,
            id="unicode-issue-7585",
        ),
    ],
)
def test_repl_output(repl, command, expected):
    """
    Test REPL command execution and output verification.

    Parametrized test covering:
    - Basic print statements
    - Expression evaluation
    - Unicode handling (issue #7585)
    """
    output = send_and_expect(repl, command, expected)
    assert expected in output


@pytest.mark.repl
def test_repl_backspace(repl):
    """
    Test REPL backspace handling.

    Types a command with typo, uses backspace to correct it, then executes.
    """
    # Type with typo: "2 + 33"
    repl.send("2 + 33")
    time.sleep(REPL_STARTUP_DELAY)

    # Send backspace to delete one '3'
    repl.send("\x7f")  # \x7f is DEL/backspace
    time.sleep(REPL_STARTUP_DELAY)

    # Now send newline to execute "2 + 3"
    repl.sendline("")
    time.sleep(REPL_COMMAND_DELAY)

    # Expect result
    index = repl.expect(["5", pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    if index != 0:
        pytest.fail(f"Expected '5'. Got: {repl.before!r}")

    # Wait for prompt
    repl.expect([">>>", pexpect.TIMEOUT, pexpect.EOF], timeout=3)


@pytest.mark.repl
@pytest.mark.parametrize(
    "command,expected",
    [
        ('print("tab:\\t")', "tab:\t"),
        ('print("newline:\\n")', "newline:"),
        ('print("quote:\\"test\\"")', 'quote:"test"'),
        ('print("backslash:\\\\")', "backslash:\\"),
    ],
    ids=["tab", "newline", "quote", "backslash"],
)
def test_repl_escape_sequences(repl, command, expected):
    """
    Test REPL handling of escape sequences.

    Verifies proper handling of:
    - Tab characters
    - Newline characters
    - Escaped quotes
    - Backslashes
    """
    output = send_and_expect(repl, command, expected)
    assert expected in output


@pytest.mark.repl
@pytest.mark.unicode
@pytest.mark.parametrize(
    "command,expected",
    [
        ('print("café")', "café"),
        ('print("你好")', "你好"),
        ('print("Привет")', "Привет"),
        pytest.param('print("😀")', "😀", id="emoji"),
    ],
    ids=["french", "chinese", "russian", "emoji"],
)
def test_repl_various_unicode(repl, command, expected):
    """
    Test REPL with various Unicode characters from different scripts.

    Tests:
    - Latin with diacritics (café)
    - Chinese characters (你好)
    - Cyrillic (Привет)
    - Emoji (😀)
    """
    output = send_and_expect(repl, command, expected)
    assert expected in output


@pytest.mark.repl
def test_repl_ctrl_c_interrupt(repl):
    """
    Test REPL Ctrl-C interrupt handling.

    Sends Ctrl-C to interrupt any running code and verify REPL returns to prompt.
    """
    # Send Ctrl-C
    repl.sendcontrol("c")
    time.sleep(REPL_COMMAND_DELAY)

    # Should see prompt (or KeyboardInterrupt then prompt)
    index = repl.expect([">>>", pexpect.TIMEOUT, pexpect.EOF], timeout=2)
    assert index == 0, "Expected prompt after Ctrl-C"

    # REPL should still be functional
    send_and_expect(repl, "1 + 1", "2")
