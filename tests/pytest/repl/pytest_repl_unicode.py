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

from repl_utils import (
    REPL_COMMAND_DELAY,
    PROMPT_P1,
    REPL_T,
    interpret_terminal_output,
    send_with_special_keys,
    send_and_expect,
)

pexpect = pytest.importorskip("pexpect", reason="pexpect required for REPL tests")


@pytest.mark.repl
@pytest.mark.parametrize(
    "input_text,expected",
    [
        pytest.param("2 + 33<BS>", "5", id="backspace"),
        pytest.param("print(2 + 321<BS><BS>)", "5", id="multiple-backspace"),
        pytest.param("printt<BS>('test')", "test", id="command-typo"),
        pytest.param("print()<LEFT>123", "123", id="arrow-navigation"),
        pytest.param("abc<HOME>print('<END>')", "abc", id="home-end"),
        # Unicode editing tests
        pytest.param("print('München')", "München", id="unicode-typing"),
    ],
)
def test_repl_special_keys(repl: REPL_T, input_text: str, expected: str):
    """
    Test REPL special key handling with marker notation.

    Supported markers:
        <BS>    - Backspace
        <LEFT>  - Left arrow
        <RIGHT> - Right arrow
        <UP>    - Up arrow
        <DOWN>  - Down arrow
        <HOME>  - Home key
        <END>   - End key
        <DEL>   - Delete key
        <ENTER> - Enter key

    Examples:
        "2 + 33<BS>" → sends "2 + 33" then backspace → "2 + 3"
        "abc<LEFT><LEFT>x" → sends "abc", moves left twice, sends "x" → "axbc"
    """

    # Send text with special key support
    send_with_special_keys(repl, input_text)

    # Send newline to execute
    repl.sendline("")
    time.sleep(REPL_COMMAND_DELAY)

    # First, consume the command echo by waiting for the end of line
    # The REPL echoes the command, then sends \r\n, then the output appears
    index = repl.expect(["\r\n", pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    if index != 0:
        pytest.fail(f"No newline after command. Got: {repl.before!r}")

    # Now expect the result in the OUTPUT (not the command echo)
    # At this point, child.before is empty and we're positioned after the command line
    index = repl.expect([expected, "SyntaxError", pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    if index == 1:
        pytest.fail(f"Got SyntaxError. Command was not correctly edited. Buffer: {repl.before!r}")
    elif index != 0:
        pytest.fail(f"Expected '{expected}' in output. Got: {repl.before!r}")

    # Verify we can get back to a prompt (command completed successfully)
    index = repl.expect([PROMPT_P1, pexpect.TIMEOUT, pexpect.EOF], timeout=3)
    if index != 0:
        pytest.fail(f"No prompt after command. Got: {repl.before!r}")


@pytest.mark.repl
@pytest.mark.parametrize(
    "input_text,expected_visual",
    [
        pytest.param(
            "print('Mü<BS>uenchen')",
            "print('Muenchen')",
            id="unicode-backspace-visual",
            marks=pytest.mark.xfail(
                reason="BUG: Backspace on multi-byte UTF-8 sends \\x08\\x08\\x1b[K which visually deletes 'Mü' leaving only 'uenchen'"
            ),
        ),
        pytest.param(
            "print('Mü')",
            "print('Mü')",
            id="unicode-display-visual",
        ),
    ],
)
def test_repl_visual_output(repl: REPL_T, input_text: str, expected_visual: str):
    """
    Test what's actually DISPLAYED on the terminal (visual representation).

    This tests the visual line editing behavior, not just the logical buffer.
    It processes ANSI escape sequences to determine what appears on screen.

    IMPORTANT: This test documents a known bug where backspace after a multi-byte
    UTF-8 character (like 'ü' = 2 bytes) sends \\x08\\x08\\x1b[K (two backspaces +
    clear to end), which visually erases MORE than just the Unicode character.

    Example: Typing "Mü<BS>" should leave "M" but actually leaves "" (empty).
    """
    import io

    # Create a log to capture all output
    log_stream = io.StringIO()
    repl.logfile_read = log_stream

    # Send text with special key support
    send_with_special_keys(repl, input_text)

    # Give time for terminal to update
    time.sleep(REPL_COMMAND_DELAY)

    # Cancel the current line with Ctrl-C to avoid executing partial command
    repl.sendcontrol("c")
    time.sleep(REPL_COMMAND_DELAY)

    # Wait for prompt
    repl.expect([PROMPT_P1, pexpect.TIMEOUT], timeout=2)

    # Get all captured output
    raw_output = log_stream.getvalue()
    repl.logfile_read = None

    # Extract the command line that was typed
    # Look for the text between the prompt and the \r\r\n that follows the Ctrl-C
    # The format is typically: " print('Mü\x08\x08\x1b[Kuenchen')\r\r\n>>> "
    lines = raw_output.split("\r\r\n")
    command_echo = None
    for line in lines:
        # Skip the startup banner and empty lines
        if "print(" in line or expected_visual in line:
            # This is the command line - extract it
            command_echo = line.strip()
            break

    if command_echo:
        # Interpret what was visually displayed
        visual_line = interpret_terminal_output(command_echo)

        # Check if the visual representation matches expected
        if expected_visual.strip() != visual_line.strip():
            pytest.fail(
                f"Visual mismatch!\n"
                f"Expected visual: {expected_visual!r}\n"
                f"Interpreted visual: {visual_line!r}\n"
                f"Raw command echo: {command_echo!r}\n"
                f"Full raw output: {raw_output!r}"
            )
    else:
        pytest.fail(f"Could not find command in output: {raw_output!r}")


@pytest.mark.repl
@pytest.mark.unicode
@pytest.mark.parametrize(
    "command, expected",
    [
        pytest.param('print("café")', "café", id="french"),
        pytest.param('print("你好")', "你好", id="chinese"),
        pytest.param('print("Привет")', "Привет", id="russian"),
        pytest.param('print("😀")', "😀", id="emoji"),
    ],
)
def test_repl_various_unicode(repl: REPL_T, command: str, expected: str):
    """
    Test REPL with various Unicode characters from different scripts.
    """
    output = send_and_expect(repl, command, expected)
    assert expected in output
