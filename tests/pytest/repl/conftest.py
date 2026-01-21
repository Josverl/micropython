# tests/pytest/repl/conftest.py
import pytest
import time

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


@pytest.fixture(scope="module")
def repl(micropython_path):
    """
    Fixture that provides a MicroPython REPL session.

    Handles startup, cleanup, and graceful exit.
    Yields the pexpect child process ready at the >>> prompt.
    """
    child = pexpect.spawn(micropython_path, encoding="utf-8", timeout=10)

    try:
        # Wait for initial prompt
        index = child.expect([PROMPT_P1, pexpect.TIMEOUT, pexpect.EOF], timeout=5)
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
                child.expect([PROMPT_P1, pexpect.TIMEOUT], timeout=2)
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
