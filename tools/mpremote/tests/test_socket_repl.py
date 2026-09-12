import io
import os
import sys
import unittest
from unittest import mock


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mpremote.console import ConsolePosix
from mpremote.transport_serial import SerialIntercept


@unittest.skipIf(sys.platform == "win32", "requires select-based console")
class ConsolePosixWaitcharTest(unittest.TestCase):
    def test_waitchar_polls_transport_without_file_descriptor(self):
        class BufferedTransport:
            def __init__(self):
                self.polls = 0

            def fileno(self):
                raise io.UnsupportedOperation

            @property
            def in_waiting(self):
                self.polls += 1
                return self.polls == 2

        console = ConsolePosix.__new__(ConsolePosix)
        console.infd = 10
        transport = BufferedTransport()
        with mock.patch("mpremote.console.select.select", return_value=([], [], [])) as select:
            console.waitchar(transport)

        self.assertEqual(transport.polls, 2)
        select.assert_called_once_with([console.infd], [], [], 0.01)

    def test_waitchar_uses_transport_file_descriptor(self):
        transport = mock.Mock()
        transport.fileno.return_value = 20
        console = ConsolePosix.__new__(ConsolePosix)
        console.infd = 10
        with mock.patch("mpremote.console.select.select") as select:
            console.waitchar(transport)

        select.assert_called_once_with([console.infd, 20], [], [])


class SerialInterceptTest(unittest.TestCase):
    def test_in_waiting_delegates_to_legacy_method(self):
        serial = SerialIntercept.__new__(SerialIntercept)
        serial.inWaiting = mock.Mock(return_value=3)
        self.assertEqual(serial.in_waiting, 3)


if __name__ == "__main__":
    unittest.main()