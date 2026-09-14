import os
import sys

import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="requires a POSIX terminal")
def test_enter_enables_newline_translation():
    import pty
    import termios

    from mpremote.console import ConsolePosix

    master_fd, slave_fd = pty.openpty()
    original_stdin = sys.stdin
    slave = os.fdopen(os.dup(slave_fd), "r")
    try:
        sys.stdin = slave
        console = ConsolePosix()
        console.enter()
        try:
            output_flags = termios.tcgetattr(slave_fd)[1]
            assert output_flags & termios.OPOST
            assert output_flags & termios.ONLCR
        finally:
            console.exit()
    finally:
        sys.stdin = original_stdin
        slave.close()
        os.close(master_fd)
        os.close(slave_fd)

