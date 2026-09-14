import io
import os
import sys

import pytest


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mpremote.console import ConsolePosix
from mpremote.transport_serial import SerialIntercept


@pytest.mark.skipif(sys.platform == "win32", reason="requires select-based console")
def test_waitchar_polls_transport_without_file_descriptor(mocker):
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
    select = mocker.patch("mpremote.console.select.select", return_value=([], [], []))

    console.waitchar(transport)

    assert transport.polls == 2
    select.assert_called_once_with([console.infd], [], [], 0.01)


@pytest.mark.skipif(sys.platform == "win32", reason="requires select-based console")
def test_waitchar_uses_transport_file_descriptor(mocker):
    transport = mocker.Mock()
    transport.fileno.return_value = 20
    console = ConsolePosix.__new__(ConsolePosix)
    console.infd = 10
    select = mocker.patch("mpremote.console.select.select")

    console.waitchar(transport)

    select.assert_called_once_with([console.infd, 20], [], [])


def test_in_waiting_delegates_to_legacy_method(mocker):
    serial = SerialIntercept.__new__(SerialIntercept)
    serial.inWaiting = mocker.Mock(return_value=3)

    assert serial.in_waiting == 3
