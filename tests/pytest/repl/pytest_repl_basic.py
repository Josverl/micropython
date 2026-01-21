#!/usr/bin/env python3
"""
Test for MicroPython interaction.

Tests basic REPL functionality and Unicode handling (issue #7585).

Usage:
    pytest test_repl_basic.py -v
    MICROPYTHON_PATH=/path/to/micropython pytest test_repl_basic.py -v
"""

import time

import pytest

from repl_utils import (
    REPL_STARTUP_DELAY,
    REPL_COMMAND_DELAY,
    REPL_SHORT_DELAY,
    PROMPT_P1,
    PROMPT_P2,
    send_and_expect,
    REPL_T,
)

pexpect = pytest.importorskip("pexpect", reason="pexpect required for REPL tests")


@pytest.mark.repl
@pytest.mark.parametrize(
    "command,expected",
    [
        pytest.param('print("tab:\\t")', "tab:\t", id="tab"),
        pytest.param('print("newline:\\n")', "newline:", id="newline"),
        pytest.param('print("quote:\\"test\\"")', 'quote:"test"', id="quote"),
        pytest.param('print("backslash:\\\\")', "backslash:\\", id="backslash"),
    ],
)
def test_repl_escape_sequences(repl: REPL_T, command: str, expected: str):
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
def test_repl_ctrl_c_interrupt(repl: REPL_T):
    """
    Test REPL Ctrl-C interrupt handling.

    Sends Ctrl-C to interrupt any running code and verify REPL returns to prompt.
    """
    # Send Ctrl-C
    repl.sendcontrol("c")
    time.sleep(REPL_COMMAND_DELAY)

    # Should see prompt (or KeyboardInterrupt then prompt)
    index = repl.expect([PROMPT_P1, pexpect.TIMEOUT, pexpect.EOF], timeout=2)
    assert index == 0, "Expected prompt after Ctrl-C"

    # REPL should still be functional
    send_and_expect(repl, "1 + 1", "2")
