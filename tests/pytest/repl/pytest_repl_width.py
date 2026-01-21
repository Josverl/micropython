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
    REPL_STARTUP_DELAY,
    REPL_COMMAND_DELAY,
    REPL_SHORT_DELAY,
    PROMPT_P1,
    PROMPT_P2,
    interpret_terminal_output,
    send_with_special_keys,
    send_and_expect,
)

pexpect = pytest.importorskip("pexpect", reason="pexpect required for REPL tests")


@pytest.mark.repl
@pytest.mark.xfail(
    reason=(
        "BUG: Wide emoji 🪲 (U+1FAB2) has visual width of 2 columns but "
        "REPL internally tracks it as 1 character for cursor positioning. "
        "When navigating with HOME key, REPL moves cursor by character count "
        "instead of visual column count, causing misalignment."
    )
)
def test_repl_wide_emoji_cursor_positioning(repl):
    """
    Test that wide emoji characters maintain correct cursor positioning in REPL.

    The beetle emoji 🪲 (U+1FAB2) has East Asian Width property of 'W' (Wide),
    meaning it occupies 2 columns in a terminal display. However, MicroPython's
    REPL currently treats it as a single character (1 column) for internal cursor
    position tracking.

    Visual issue observed (see screenshot):
    1. User types: print("🪲")
    2. Emoji displays taking 2 visual columns
    3. REPL moves cursor forward by 1 character (not 2 columns)
    4. Following characters appear at wrong visual positions
    5. Result: Visual overlap - closing quote overwrites emoji's second column

    Detection strategy:
    - Type a string with wide emoji: "🪲"
    - Use HOME to go to beginning (REPL sends \x1b[5D for 5 chars: " 🪲 ")
    - But visually it's 6 columns: " + 🪲(2 cols) + "
    - The cursor ends up 1 column off from where it should be
    - Type 'X' which should appear at the start
    - If cursor is mispositioned, X appears in the wrong place

    This test will FAIL when the bug exists because the REPL's character-based
    cursor positioning doesn't match the terminal's column-based display.
    """
    import io

    # Capture terminal output
    log_stream = io.StringIO()
    repl.logfile_read = log_stream

    # Type: "🪲"
    # This is 3 characters but 4 visual columns (quote + 2-col emoji + quote)
    send_with_special_keys(repl, '"🪲"')
    time.sleep(REPL_SHORT_DELAY)

    # Use HOME to go to beginning
    # REPL will move cursor left by 3 (character count)
    # But should move left by 4 (visual column count)
    # This leaves cursor 1 column to the right of where it should be
    send_with_special_keys(repl, "<HOME>")
    time.sleep(REPL_SHORT_DELAY)

    # Now type 'START' - it should appear at the beginning
    # But due to cursor mispositioning, it will overwrite part of the line
    send_with_special_keys(repl, "START")
    time.sleep(REPL_SHORT_DELAY)

    # Cancel the line
    repl.sendcontrol("c")
    time.sleep(REPL_SHORT_DELAY)

    # Wait for prompt
    repl.expect([PROMPT_P1, pexpect.TIMEOUT], timeout=2)

    # Get the captured output
    raw_output = log_stream.getvalue()
    repl.logfile_read = None

    # With correct positioning: START"🪲" should appear as complete string
    # With bug: Each char of START causes redraw, showing S"🪲", T"🪲", A"🪲", etc.
    # The full word 'START"🪲"' as a contiguous sequence won't appear

    # Check if the line was corrupted due to cursor mispositioning
    # Looking for the pattern where START and emoji appear together properly
    # With the bug, we see individual letters mixed with redraws

    # Count how many times the emoji appears (each redraw shows it again)
    emoji_count = raw_output.count("🪲")

    # With correct cursor positioning: emoji appears once or twice
    # With bug: emoji appears 5+ times (once per character typed in 'START')
    if emoji_count > 3:
        pytest.fail(
            "Cursor positioning error detected! "
            "The emoji appears {} times in output, indicating the line is being "
            "redrawn repeatedly due to cursor misalignment. "
            "Each character typed caused a redraw instead of proper insertion. "
            "This is caused by REPL treating wide emoji (2 visual columns) as "
            "1 character for cursor positioning. "
            "Raw output: {!r}".format(emoji_count, raw_output)
        )

    # Also check that START appears as complete word
    if "START" not in raw_output:
        pytest.fail(
            "The word 'START' is corrupted or missing, indicating cursor "
            "mispositioning after wide emoji. "
            "Raw output: {!r}".format(raw_output)
        )
