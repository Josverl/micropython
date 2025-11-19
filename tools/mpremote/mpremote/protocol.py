#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""MicroPython raw REPL protocol handler.

This module contains protocol-agnostic logic for handling MicroPython's
raw REPL mode, extracted from the transport layer to support multiple
transport implementations (serial, WebSocket, BLE, etc.).
"""


class RawREPLProtocol:
    """Handles MicroPython raw REPL protocol.
    
    This class encapsulates the control codes and logic for communicating
    with MicroPython devices using the raw REPL protocol, which provides
    a more programmatic interface than the friendly REPL.
    """
    
    # Control codes for raw REPL
    CTRL_A = b'\x01'  # Enter raw REPL
    CTRL_B = b'\x02'  # Exit raw REPL
    CTRL_C = b'\x03'  # Interrupt/KeyboardInterrupt
    CTRL_D = b'\x04'  # Soft reset / End of input
    CTRL_E = b'\x05'  # Start raw paste mode
    
    # Raw REPL sequences
    RAW_REPL_ENTER = b'\r\x03\x03'  # CR + Ctrl-C twice to interrupt
    RAW_REPL_EXIT = b'\r\x02'       # CR + Ctrl-B to exit
    RAW_PASTE_START = b'\x05A\x01'  # Ctrl-E A \x01 for raw paste mode
    
    # Expected responses
    RAW_REPL_PROMPT = b'raw REPL; CTRL-B to exit\r\n>'
    RAW_REPL_OK = b'OK'
    SOFT_REBOOT_MSG = b'soft reboot\r\n'
    
    @staticmethod
    def is_raw_paste_supported(response: bytes) -> bool:
        """Check if device supports raw paste mode.
        
        Args:
            response: Response from entering raw REPL
            
        Returns:
            bool: True if raw paste is supported
        """
        # Raw paste mode is supported if the device doesn't respond with an error
        # This is typically indicated by the device accepting Ctrl-E command
        return b'OK' in response or b'raw REPL' in response
    
    @staticmethod
    def encode_command_standard(command: str) -> bytes:
        """Encode command for standard raw REPL mode.
        
        Args:
            command: Python code to execute
            
        Returns:
            bytes: Encoded command ready for transmission
        """
        return command.encode('utf-8')
    
    @staticmethod
    def encode_command_raw_paste(command: str) -> tuple:
        """Encode command for raw paste mode.
        
        Raw paste mode uses a length-prefixed protocol with flow control.
        
        Args:
            command: Python code to execute
            
        Returns:
            tuple: (header, command_bytes) where header includes length
        """
        command_bytes = command.encode('utf-8')
        # Header: Ctrl-E A \x01 followed by 4-byte little-endian length
        header = RawREPLProtocol.RAW_PASTE_START
        length = len(command_bytes).to_bytes(4, 'little')
        return header + length, command_bytes
    
    @staticmethod
    def decode_response(data: bytes) -> tuple:
        """Decode response from raw REPL execution.
        
        The response format is:
        - stdout data followed by \x04
        - stderr data followed by \x04
        
        Args:
            data: Raw response data
            
        Returns:
            tuple: (stdout, stderr) as bytes
        """
        # Find the two \x04 markers that separate stdout and stderr
        parts = data.split(b'\x04')
        
        if len(parts) >= 2:
            stdout = parts[0]
            stderr = parts[1] if len(parts) > 1 else b''
        else:
            stdout = data
            stderr = b''
        
        return stdout, stderr
    
    @staticmethod
    def check_error(stderr: bytes):
        """Check if stderr contains an error and extract it.
        
        Args:
            stderr: Error output from command execution
            
        Returns:
            str or None: Error message if present, None otherwise
        """
        if stderr:
            # Remove trailing whitespace and decode
            error_msg = stderr.strip().decode('utf-8', errors='replace')
            if error_msg:
                return error_msg
        return None
