#!/usr/bin/env python3
"""
Utility functions and constants for MicroPython REPL testing.

Provides helper functions for:
- Sending special keys (arrows, backspace, etc.) to REPL
- Interpreting terminal output with ANSI escape sequences
- Common REPL interaction patterns
"""

from typing import TYPE_CHECKING, TypeAlias
import time

if TYPE_CHECKING:
    import pexpect
    REPL_T : TypeAlias = pexpect.pty_spawn.spawn
else:
    REPL_T = object  # type: ignore



# Timing constants for REPL interaction
REPL_STARTUP_DELAY = 0.05  # Time to let REPL settle after startup
REPL_COMMAND_DELAY = 0.01  # Time to wait after sending command
REPL_SHORT_DELAY   = 0.000_1  # Short delay for quick operations

# REPL prompt constants
PROMPT_P1 = ">>>"
PROMPT_P2 = "..."

# Special key escape sequences
KEY_BACKSPACE = "\x7f"  # \x7f is DEL/backspace
KEY_UP = "\x1b[A"  # Up arrow - ANSI escape sequence
KEY_DOWN = "\x1b[B"  # Down arrow - ANSI escape sequence
KEY_RIGHT = "\x1b[C"  # Right arrow - ANSI escape sequence
KEY_LEFT = "\x1b[D"  # Left arrow - ANSI escape sequence
KEY_HOME = "\x1b[H"  # Home key - ANSI escape sequence
KEY_END = "\x1b[F"  # End key - ANSI escape sequence
KEY_DELETE = "\x1b[3~"  # Delete key - ANSI escape sequence
KEY_ENTER = "\r"  # Enter key - carriage return

# Mapping of special key markers to their escape sequences
KEY_MARKERS = {
    "<BS>": KEY_BACKSPACE,
    "<UP>": KEY_UP,
    "<DOWN>": KEY_DOWN,
    "<LEFT>": KEY_LEFT,
    "<RIGHT>": KEY_RIGHT,
    "<HOME>": KEY_HOME,
    "<END>": KEY_END,
    "<DEL>": KEY_DELETE,
    "<ENTER>": KEY_ENTER,
}


def interpret_terminal_output(text:str) -> str:
    """
    Interpret terminal output by processing ANSI escape sequences and cursor movements.

    This simulates what actually appears on screen by processing:
    - Backspace (\x08): move cursor left
    - Clear to end of line (\x1b[K): clear from cursor to end
    - Other ANSI sequences are stripped

    Returns the visual representation of what would be displayed.

    Args:
        text: Raw terminal output with escape sequences

    Returns:
        String representing what would be visually displayed
    """
    # Build the line character by character, tracking cursor position
    line = []
    cursor_pos = 0
    i = 0

    while i < len(text):
        if text[i] == "\x08":  # Backspace - move cursor left
            if cursor_pos > 0:
                cursor_pos -= 1
            i += 1
        elif text[i] == "\x1b":  # ANSI escape sequence
            # Look for escape sequence patterns
            if i + 1 < len(text) and text[i + 1] == "[":
                # Find the end of the escape sequence
                j = i + 2
                while j < len(text) and text[j] not in "ABCDEFGHJKSTfmnsulh":
                    j += 1
                if j < len(text):
                    seq = text[i : j + 1]
                    if seq == "\x1b[K":  # Clear to end of line
                        line = line[:cursor_pos]
                    # Other sequences ignored (cursor movement handled separately)
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1
        elif text[i] in "\r\n":  # Skip newlines in line buffer
            i += 1
        else:  # Regular character
            # Insert/overwrite at cursor position
            if cursor_pos < len(line):
                line[cursor_pos] = text[i]
            else:
                line.append(text[i])
            cursor_pos += 1
            i += 1

    return "".join(line)


def send_with_special_keys(repl: REPL_T, text:str):
    """
    Send text to REPL with special key support.

    Handles special key markers in the input text and converts them to actual keystrokes.

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

    Example:
        send_with_special_keys(repl, "eval(2 + 321<BS><BS>)")
        This sends: "eval(2 + 321", then two backspaces, resulting in "eval(2 + 3"

        send_with_special_keys(repl, "prin<LEFT><LEFT><LEFT><LEFT>t")
        This sends: "prin", then 4 left arrows, then "t", resulting in "tprin"
        (cursor moves back to start, then 't' is inserted)

    Args:
        repl: The pexpect REPL child process
        text: Text with optional special key markers
    """
    # Process text, batching regular characters for efficiency
    i = 0
    buffer = []  # Buffer for regular characters
    
    while i < len(text):
        # Check if we're at a special key marker (e.g., <BS>, <LEFT>)
        if text[i] == "<":
            # Find the closing bracket
            end = text.find(">", i)
            if end != -1:
                marker = text[i : end + 1]
                if marker in KEY_MARKERS:
                    # Flush any buffered regular characters first
                    if buffer:
                        repl.send("".join(buffer))
                        buffer = []

                    # Send the key sequence
                    repl.send(KEY_MARKERS[marker])
                    time.sleep(REPL_SHORT_DELAY)
                    i = end + 1
                    continue

        # Regular character, add to buffer
        buffer.append(text[i])
        i += 1
    
    # Flush any remaining buffered characters
    if buffer:
        repl.send("".join(buffer))


def send_and_expect(repl, command, expected, timeout=3):
    """
    Helper to send command and verify expected output.

    Args:
        repl: The pexpect REPL child process
        command: Command string to send
        expected: Expected output string
        timeout: Timeout in seconds (default 3)

    Returns:
        The output before the expected match

    Raises:
        pytest.fail if expected output not found or no prompt returned
    """
    import re
    import pytest

    repl.sendline(command)
    time.sleep(REPL_COMMAND_DELAY)

    # Use re.escape for expected to handle special regex characters
    escaped_expected = re.escape(expected)

    pexpect = pytest.importorskip("pexpect")
    index = repl.expect([escaped_expected, pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    if index != 0:
        pytest.fail(f"Expected '{expected}'. Got: {repl.before!r}")

    output = repl.before + expected

    # Wait for next prompt
    index = repl.expect([PROMPT_P1, pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    if index != 0:
        pytest.fail(f"No prompt after command. Got: {repl.before!r}")

    return output

