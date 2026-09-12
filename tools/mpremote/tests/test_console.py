import os
import sys
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@unittest.skipIf(sys.platform == "win32", "requires a POSIX terminal")
class ConsolePosixTest(unittest.TestCase):
    def test_enter_enables_newline_translation(self):
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
                self.assertTrue(output_flags & termios.OPOST)
                self.assertTrue(output_flags & termios.ONLCR)
            finally:
                console.exit()
        finally:
            sys.stdin = original_stdin
            slave.close()
            os.close(master_fd)
            os.close(slave_fd)


if __name__ == "__main__":
    unittest.main()
