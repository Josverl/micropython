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

"""Async command handlers for mpremote.

This module provides async versions of command handlers that work with
AsyncTransport implementations. These handlers enable non-blocking
concurrent operations while maintaining backward compatibility through
sync wrappers.
"""

import asyncio
import sys

from .transport import stdout_write_bytes, TransportExecError


async def do_exec_async(state, args):
    """Async version of exec command.
    
    Args:
        state: State object with transport connection
        args: Command arguments
    """
    await state.ensure_raw_repl_async()
    state.did_action()
    
    # Read command
    if args.command == "-":
        pyfile = sys.stdin.buffer.read()
    else:
        with open(args.command, "rb") as f:
            pyfile = f.read()
    
    # Execute the command
    if hasattr(state.transport, 'exec_raw_no_follow_async'):
        await state.transport.exec_raw_no_follow_async(pyfile)
        
        # Follow output if requested
        if args.follow:
            ret, ret_err = await state.transport.follow_async(
                timeout=None,
                data_consumer=stdout_write_bytes
            )
            if ret_err:
                stdout_write_bytes(ret_err)
                raise TransportExecError(1, ret_err)
    else:
        # Fall back to sync version
        state.transport.exec_raw_no_follow(pyfile)
        if args.follow:
            ret, ret_err = state.transport.follow(
                timeout=None,
                data_consumer=stdout_write_bytes
            )
            if ret_err:
                stdout_write_bytes(ret_err)
                raise TransportExecError(1, ret_err)


async def do_eval_async(state, args):
    """Async version of eval command.
    
    Args:
        state: State object with transport connection
        args: Command arguments
    """
    await state.ensure_raw_repl_async()
    state.did_action()
    
    # Evaluate expression
    if hasattr(state.transport, 'eval_async'):
        result = await state.transport.eval_async(args.expression)
    else:
        result = state.transport.eval(args.expression)
    
    print(result)


async def do_run_async(state, args):
    """Async version of run command.
    
    Args:
        state: State object with transport connection
        args: Command arguments
    """
    await state.ensure_raw_repl_async()
    state.did_action()
    
    # Read script file
    with open(args.script, "rb") as f:
        pyfile = f.read()
    
    # Execute the script
    if hasattr(state.transport, 'exec_raw_async'):
        ret, ret_err = await state.transport.exec_raw_async(
            pyfile,
            data_consumer=stdout_write_bytes
        )
    else:
        ret, ret_err = state.transport.exec_raw(
            pyfile,
            data_consumer=stdout_write_bytes
        )
    
    if ret_err:
        stdout_write_bytes(ret_err)
        raise TransportExecError(1, ret_err)


async def do_filesystem_cp_async(state, src, dest, check_hash=False):
    """Async version of filesystem copy.
    
    Args:
        state: State object with transport connection
        src: Source path (prefixed with ':' for remote)
        dest: Destination path (prefixed with ':' for remote)
        check_hash: Whether to check hash before copying
    """
    from .commands import show_progress_bar, _remote_path_basename, CommandError
    import hashlib
    
    await state.ensure_raw_repl_async()
    
    # Download the contents of source
    if src.startswith(":"):
        if hasattr(state.transport, 'fs_readfile_async'):
            data = await state.transport.fs_readfile_async(
                src[1:],
                progress_callback=show_progress_bar
            )
        else:
            data = state.transport.fs_readfile(
                src[1:],
                progress_callback=show_progress_bar
            )
        filename = _remote_path_basename(src[1:])
    else:
        with open(src, "rb") as f:
            data = f.read()
        import os
        filename = os.path.basename(src)
    
    # Write to destination
    if dest.startswith(":"):
        # Check if we should skip based on hash
        if check_hash:
            try:
                if hasattr(state.transport, 'fs_hashfile'):
                    remote_hash = state.transport.fs_hashfile(dest[1:], "sha256")
                    source_hash = hashlib.sha256(data).digest()
                    if remote_hash == source_hash:
                        print("Up to date:", dest[1:])
                        return
            except OSError:
                pass
        
        # Write to remote
        if hasattr(state.transport, 'fs_writefile_async'):
            await state.transport.fs_writefile_async(
                dest[1:],
                data,
                progress_callback=show_progress_bar
            )
        else:
            state.transport.fs_writefile(
                dest[1:],
                data,
                progress_callback=show_progress_bar
            )
    else:
        # Write to local file
        with open(dest, "wb") as f:
            f.write(data)


# Sync wrappers for backward compatibility
def do_exec_sync_wrapper(state, args):
    """Sync wrapper for async exec command."""
    asyncio.run(do_exec_async(state, args))


def do_eval_sync_wrapper(state, args):
    """Sync wrapper for async eval command."""
    asyncio.run(do_eval_async(state, args))


def do_run_sync_wrapper(state, args):
    """Sync wrapper for async run command."""
    asyncio.run(do_run_async(state, args))
