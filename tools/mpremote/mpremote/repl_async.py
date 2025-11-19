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

"""Async REPL implementation for mpremote.

This module provides an async REPL loop that enables concurrent handling
of keyboard input and device output without blocking.
"""

import asyncio
import sys

from .console_async import AsyncConsole
from .transport import TransportError


async def do_repl_main_loop_async(
    state, console, *, escape_non_printable=False, code_to_inject=None, file_to_inject=None
):
    """Async REPL loop with concurrent keyboard and device I/O.
    
    This function runs two concurrent coroutines:
    1. Reading keyboard input and sending to device
    2. Reading device output and displaying to console
    
    Args:
        state: State object with transport connection
        console: Async console for I/O
        escape_non_printable: Whether to escape non-printable characters
        code_to_inject: Code to inject on Ctrl-J
        file_to_inject: File to inject on Ctrl-K
        
    Returns:
        bool: True if device disconnected, False if user exited
    """
    
    async def handle_keyboard_input():
        """Coroutine: read keyboard input and send to device."""
        while True:
            try:
                c = await console.readchar_async()
                
                if c in (b"\x1d", b"\x18"):  # ctrl-] or ctrl-x, quit
                    return "exit"
                elif c == b"\x04":  # ctrl-D
                    # Special handling needed for ctrl-D if filesystem is mounted
                    if hasattr(state.transport, 'write_ctrl_d'):
                        state.transport.write_ctrl_d(console.write)
                    else:
                        if hasattr(state.transport, 'write_async'):
                            await state.transport.write_async(c)
                        else:
                            state.transport.serial.write(c)
                elif c == b"\x0a" and code_to_inject is not None:  # ctrl-j, inject code
                    if hasattr(state.transport, 'write_async'):
                        await state.transport.write_async(code_to_inject)
                    else:
                        state.transport.serial.write(code_to_inject)
                elif c == b"\x0b" and file_to_inject is not None:  # ctrl-k, inject script
                    console.write(bytes(f"Injecting {file_to_inject}\r\n", "utf8"))
                    
                    # Enter raw REPL and execute file
                    if hasattr(state.transport, 'enter_raw_repl_async'):
                        await state.transport.enter_raw_repl_async(soft_reset=False)
                    else:
                        state.transport.enter_raw_repl(soft_reset=False)
                    
                    with open(file_to_inject, "rb") as f:
                        pyfile = f.read()
                    
                    try:
                        if hasattr(state.transport, 'exec_raw_no_follow_async'):
                            await state.transport.exec_raw_no_follow_async(pyfile)
                        else:
                            state.transport.exec_raw_no_follow(pyfile)
                    except TransportError as er:
                        console.write(b"Error:\r\n")
                        console.write(str(er).encode())
                    
                    if hasattr(state.transport, 'exit_raw_repl_async'):
                        await state.transport.exit_raw_repl_async()
                    else:
                        state.transport.exit_raw_repl()
                else:
                    # Send character to device
                    if hasattr(state.transport, 'write_async'):
                        await state.transport.write_async(c)
                    else:
                        state.transport.serial.write(c)
            except OSError as er:
                if _is_disconnect_exception(er):
                    return "disconnect"
                raise
            except Exception as e:
                print(f"\r\nKeyboard error: {e}")
                return "error"
    
    async def handle_device_output():
        """Coroutine: read device output and write to console."""
        while True:
            try:
                # Read data from device
                if hasattr(state.transport, 'read_async'):
                    # Async transport
                    # Check if there's data available (non-blocking)
                    try:
                        async with asyncio.timeout(0.1):
                            dev_data_in = await state.transport.read_async(256)
                            if dev_data_in:
                                if escape_non_printable:
                                    # Pass data through to the console, with escaping
                                    console_data_out = bytearray()
                                    for c in dev_data_in:
                                        if c in (8, 9, 10, 13, 27) or 32 <= c <= 126:
                                            console_data_out.append(c)
                                        else:
                                            console_data_out.extend(b"[%02x]" % c)
                                else:
                                    console_data_out = dev_data_in
                                console.write(console_data_out)
                    except asyncio.TimeoutError:
                        # No data available, just continue
                        await asyncio.sleep(0.01)
                else:
                    # Sync transport - use polling
                    n = state.transport.serial.inWaiting()
                    if n > 0:
                        dev_data_in = state.transport.serial.read(n)
                        if dev_data_in is not None:
                            if escape_non_printable:
                                console_data_out = bytearray()
                                for c in dev_data_in:
                                    if c in (8, 9, 10, 13, 27) or 32 <= c <= 126:
                                        console_data_out.append(c)
                                    else:
                                        console_data_out.extend(b"[%02x]" % c)
                            else:
                                console_data_out = dev_data_in
                            console.write(console_data_out)
                    else:
                        await asyncio.sleep(0.01)  # Yield control
            except OSError as er:
                if _is_disconnect_exception(er):
                    return "disconnect"
                raise
            except Exception as e:
                print(f"\r\nDevice error: {e}")
                return "error"
    
    # Run both coroutines concurrently
    try:
        tasks = [
            asyncio.create_task(handle_keyboard_input(), name="keyboard"),
            asyncio.create_task(handle_device_output(), name="device")
        ]
        
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Get the result from completed task
        result = None
        for task in done:
            try:
                result = task.result()
            except Exception as e:
                print(f"\r\nTask error: {e}")
                result = "error"
        
        # Cancel remaining tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Return True if disconnected, False otherwise
        return result == "disconnect"
    
    except KeyboardInterrupt:
        console.exit()
        return False


async def do_repl_async(state, args):
    """Async REPL command handler.
    
    Args:
        state: State object with transport connection
        args: Command arguments
        
    Returns:
        bool: True if device disconnected, False if user exited
    """
    # Ensure we're in friendly REPL mode
    await state.ensure_friendly_repl_async()
    state.did_action()
    
    escape_non_printable = args.escape_non_printable
    capture_file = args.capture
    code_to_inject = args.inject_code
    file_to_inject = args.inject_file
    
    print(f"Connected to MicroPython at {state.transport.device_name}")
    print("Use Ctrl-] or Ctrl-x to exit this shell")
    if escape_non_printable:
        print("Escaping non-printable bytes/characters by printing their hex code")
    if capture_file is not None:
        print(f'Capturing session to file "{capture_file}"')
        capture_file = open(capture_file, "wb")
    if code_to_inject is not None:
        code_to_inject = bytes(code_to_inject.replace("\\n", "\r\n"), "utf8")
        print("Use Ctrl-J to inject", code_to_inject)
    if file_to_inject is not None:
        print(f'Use Ctrl-K to inject file "{file_to_inject}"')
    
    console = AsyncConsole()
    console.enter()
    
    # Wrap console.write to also write to capture file
    original_write = console.write
    if capture_file is not None:
        def console_write_with_capture(b):
            original_write(b)
            capture_file.write(b)
            capture_file.flush()
        console.write = console_write_with_capture
    
    try:
        return await do_repl_main_loop_async(
            state,
            console,
            escape_non_printable=escape_non_printable,
            code_to_inject=code_to_inject,
            file_to_inject=file_to_inject,
        )
    finally:
        console.exit()
        if capture_file is not None:
            capture_file.close()


def _is_disconnect_exception(exception):
    """Check if an exception indicates device disconnect.
    
    Args:
        exception: Exception to check
        
    Returns:
        bool: True if the exception indicates device disconnected
    """
    if isinstance(exception, OSError):
        if hasattr(exception, "args") and len(exception.args) > 0:
            # IO error, device disappeared
            if exception.args[0] == 5:
                return True
        # Check for common disconnect messages in the exception string
        exception_str = str(exception)
        disconnect_indicators = ["Write timeout", "Device disconnected", "ClearCommError failed"]
        return any(indicator in exception_str for indicator in disconnect_indicators)
    return False


# Sync wrapper for backward compatibility
def do_repl_async_wrapper(state, args):
    """Synchronous wrapper for async REPL.
    
    Args:
        state: State object with transport connection
        args: Command arguments
        
    Returns:
        bool: True if device disconnected, False if user exited
    """
    return asyncio.run(do_repl_async(state, args))
