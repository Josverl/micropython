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
import os
import sys
import tempfile

import serial.tools.list_ports

from .commands import (
    CommandError,
    CommandFailure,
    _remote_path_basename,
    _remote_path_dirname,
    _remote_path_join,
    do_disconnect,
    human_size,
    show_progress_bar,
)
from .transport import (
    TransportError,
    TransportExecError,
    _convert_filesystem_error,
    stdout_write_bytes,
)
from .transport_serial_async import AsyncSerialTransport


async def _open_async_serial(device: str):
    """Instantiate and connect an AsyncSerialTransport for the given device."""
    transport = AsyncSerialTransport(device, baudrate=115200)
    await transport.connect()
    return transport


async def do_connect_async(state, args=None):
    """Async equivalent of do_connect that always provisions an async transport."""

    dev = args.device[0] if args else "auto"
    if state.transport is not None:
        # Run the sync disconnect helper in a worker thread so that async transports
        # using asyncio.run() during teardown do not see the currently running loop.
        await asyncio.to_thread(do_disconnect, state)

    try:
        if dev == "list":
            for p in sorted(serial.tools.list_ports.comports()):
                print(
                    "{} {} {:04x}:{:04x} {} {}".format(
                        p.device,
                        p.serial_number,
                        p.vid if isinstance(p.vid, int) else 0,
                        p.pid if isinstance(p.pid, int) else 0,
                        p.manufacturer,
                        p.product,
                    )
                )
            state.did_action()
            return

        if dev == "auto":
            for p in sorted(serial.tools.list_ports.comports()):
                if p.vid is not None and p.pid is not None:
                    transport = await _open_async_serial(p.device)
                    state.transport = transport
                    return
            raise TransportError("no device found")

        if dev.startswith("id:"):
            serial_number = dev[len("id:") :]
            for p in serial.tools.list_ports.comports():
                if p.serial_number == serial_number:
                    transport = await _open_async_serial(p.device)
                    state.transport = transport
                    return
            raise TransportError(f"no device with serial number {serial_number}")

        if dev.startswith("port:"):
            dev = dev[len("port:") :]

        state.transport = await _open_async_serial(dev)
    except CommandError:
        raise
    except TransportError as er:
        msg = er.args[0] if er.args else str(er)
        if isinstance(msg, str) and msg.startswith("failed to access"):
            msg += " (it may be in use by another program)"
        raise CommandError(msg) from er


def _get_follow_flag(args, default=True):
    follow = getattr(args, "follow", None)
    return follow if follow is not None else default


def _resolve_exec_buffer(args):
    """Return the bytes object that should be executed by exec.*"""

    # CLI path uses args.expr (list), but tests exercise args.command directly.
    expr = getattr(args, "expr", None)
    if isinstance(expr, (list, tuple)) and expr:
        buf = expr[0]
        return buf if isinstance(buf, (bytes, bytearray)) else bytes(buf, "utf-8")

    command = getattr(args, "command", None)
    if isinstance(command, (str, bytes, bytearray)):
        if command == "-":
            return sys.stdin.buffer.read()
        with open(command, "rb") as f:
            data = f.read()
        return data

    raise CommandError("exec: missing command or expression")


def _resolve_eval_expression(args):
    expr = getattr(args, "expr", None)
    if isinstance(expr, (list, tuple)) and expr:
        return expr[0]
    expression = getattr(args, "expression", None)
    if isinstance(expression, str):
        return expression
    raise CommandError("eval: missing expression")


def _resolve_run_script(args):
    path = getattr(args, "path", None)
    if isinstance(path, (list, tuple)) and path:
        return path[0]
    script = getattr(args, "script", None)
    if isinstance(script, str):
        return script
    raise CommandError("run: missing script path")


async def do_exec_async(state, args):
    """Async version of exec command.

    Args:
        state: State object with transport connection
        args: Command arguments (expects args.expr[0])
    """
    await state.ensure_raw_repl_async()
    state.did_action()

    pyfile = _resolve_exec_buffer(args)
    follow = _get_follow_flag(args, True)

    try:
        transport = state.transport
        await transport.exec_raw_no_follow_async(pyfile)
        if follow:
            ret, ret_err = await transport.follow_async(
                timeout=None, data_consumer=stdout_write_bytes
            )
            if ret_err:
                stdout_write_bytes(ret_err)
                raise TransportExecError(1, ret_err)
    except TransportExecError:
        raise
    except TransportError as er:
        raise CommandError(er.args[0])
    except KeyboardInterrupt:
        raise


async def do_eval_async(state, args):
    """Async version of eval command.

    Args:
        state: State object with transport connection
        args: Command arguments (expects args.expr[0])
    """
    await state.ensure_raw_repl_async()
    state.did_action()

    expression = _resolve_eval_expression(args)
    # Wrap expression in print() like sync version does
    buf = "print(" + expression + ")"

    try:
        transport = state.transport
        await transport.exec_raw_no_follow_async(buf)
        ret, ret_err = await transport.follow_async(timeout=None, data_consumer=stdout_write_bytes)
        if ret_err:
            stdout_write_bytes(ret_err)
            raise CommandFailure(1)
    except TransportError as er:
        raise CommandError(er.args[0])
    except KeyboardInterrupt:
        raise CommandFailure(1)


async def do_run_async(state, args):
    """Async version of run command.

    Args:
        state: State object with transport connection
        args: Command arguments (expects args.path[0])
    """
    await state.ensure_raw_repl_async()
    state.did_action()

    filename = _resolve_run_script(args)
    with open(filename, "rb") as f:
        pyfile = f.read()

    follow = _get_follow_flag(args, True)
    transport = state.transport

    try:
        if follow:
            ret, ret_err = await transport.exec_raw_async(pyfile, data_consumer=stdout_write_bytes)
            if ret_err:
                stdout_write_bytes(ret_err)
                raise TransportExecError(1, ret_err)
        else:
            await transport.exec_raw_no_follow_async(pyfile)
    except TransportExecError:
        raise
    except TransportError as er:
        raise CommandError(er.args[0])
    except KeyboardInterrupt:
        raise


async def do_soft_reset_async(state, _args=None):
    """Async version of soft_reset command.

    Args:
        state: State object with transport connection
        _args: Unused arguments
    """
    await state.ensure_raw_repl_async(soft_reset=True)
    state.did_action()


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


async def do_filesystem_async(state, args):
    """Async version of filesystem operations.

    Handles all filesystem commands: ls, cat, mkdir, rm, rmdir, tree, cp, touch, sha256sum

    Args:
        state: State object with transport connection
        args: Command arguments with command, path, verbose, recursive, force flags
    """
    await state.ensure_raw_repl_async()
    state.did_action()

    command = args.command[0]
    paths = args.path

    if command == "cat":
        # Don't do verbose output for `cat` unless explicitly requested.
        verbose = args.verbose is True
    else:
        verbose = args.verbose is not False

    if command == "cp":
        # Note: cp requires the user to specify local/remote explicitly via leading ':'.
        # The last argument must be the destination.
        if len(paths) <= 1:
            raise CommandError("cp: missing destination path")
        cp_dest = paths[-1]
        paths = paths[:-1]
    else:
        # All other commands implicitly use remote paths. Strip the leading ':' if included.
        paths = [path[1:] if path.startswith(":") else path for path in paths]

    # ls and tree implicitly lists the cwd.
    if command in ("ls", "tree") and not paths:
        paths = [""]

    try:
        # Handle each path sequentially.
        for path in paths:
            if verbose:
                if command == "cp":
                    print("{} {} {}".format(command, path, cp_dest))
                else:
                    print("{} :{}".format(command, path))

            if command == "cat":
                await _do_fs_printfile_async(state, path)
            elif command == "ls":
                results = await state.transport.fs_listdir_async(path)
                for result in results:
                    print(
                        "{:12} {}{}".format(
                            result.st_size, result.name, "/" if result.st_mode & 0x4000 else ""
                        )
                    )
            elif command == "mkdir":
                await _do_fs_mkdir_async(state, path)
            elif command == "rm":
                if args.recursive:
                    await do_filesystem_recursive_rm_async(state, path, args)
                else:
                    await _do_fs_rmfile_async(state, path)
            elif command == "rmdir":
                await _do_fs_rmdir_async(state, path)
            elif command == "touch":
                await _do_fs_touchfile_async(state, path)
            elif command.endswith("sum") and command[-4].isdigit():
                digest = await _do_fs_hashfile_async(state, path, command[:-3])
                print(digest.hex())
            elif command == "cp":
                # Use sync version - it handles remote-to-remote and transport has sync wrappers
                from .commands import do_filesystem_cp, do_filesystem_recursive_cp
                if args.recursive:
                    do_filesystem_recursive_cp(
                        state, path, cp_dest, len(paths) > 1, not args.force
                    )
                else:
                    do_filesystem_cp(
                        state, path, cp_dest, len(paths) > 1, not args.force
                    )
            elif command == "tree":
                # Use sync version - it's well-tested and transport has sync wrappers
                from .commands import do_filesystem_tree
                do_filesystem_tree(state, path, args)
    except OSError as er:
        raise CommandError("{}: {}: {}.".format(command, er.strerror, os.strerror(er.errno)))
    except TransportError as er:
        raise CommandError("Error with transport:\n{}".format(er.args[0]))


async def _do_fs_printfile_async(state, src, chunk_size=256):
    """Async helper to print file contents."""
    try:
        await state.transport.exec_async(
            f"with open({src!r}, 'rb') as f:\n while 1:\n  b=f.read({chunk_size})\n  if not b:break\n  print(b,end='')"
        )
    except TransportExecError as e:
        raise _convert_filesystem_error(e, src) from None


async def _do_fs_mkdir_async(state, path):
    """Async helper to create directory."""
    await state.transport.exec_async(f"import os\nos.mkdir({path!r})")


async def _do_fs_rmdir_async(state, path):
    """Async helper to remove directory."""
    await state.transport.exec_async(f"import os\nos.rmdir({path!r})")


async def _do_fs_rmfile_async(state, path):
    """Async helper to remove file."""
    await state.transport.exec_async(f"import os\nos.remove({path!r})")


async def _do_fs_touchfile_async(state, path):
    """Async helper to touch file."""
    await state.transport.exec_async(f"f=open({path!r},'a')\nf.close()")


async def _do_fs_hashfile_async(state, path, algo, chunk_size=256):
    """Async helper to compute file hash."""
    import hashlib

    # Compute hash on device
    await state.transport.exec_async(
        f"import hashlib\nh=hashlib.{algo}()\nwith open({path!r},'rb') as f:\n "
        f"while 1:\n  b=f.read({chunk_size})\n  if not b:break\n  h.update(b)"
    )
    result = await state.transport.eval_async("h.digest()")
    return result


async def do_filesystem_recursive_rm_async(state, path, args):
    """Async recursive directory removal."""
    # Check if it's a directory using async method
    try:
        stat_result = await state.transport.fs_stat_async(path)
        is_dir = stat_result[0] & 0x4000  # Check directory bit
    except OSError:
        # If stat fails, try to remove as file
        await _do_fs_rmfile_async(state, path)
        return

    if is_dir:
        # List directory contents
        entries = await state.transport.fs_listdir_async(path)

        # Recursively remove contents
        for entry in entries:
            entry_path = _remote_path_join(path, entry.name)
            if entry.st_mode & 0x4000:  # Is directory
                await do_filesystem_recursive_rm_async(state, entry_path, args)
            else:
                if args.verbose:
                    print("rm :{}".format(entry_path))
                await _do_fs_rmfile_async(state, entry_path)

        # Remove the now-empty directory
        if args.verbose:
            print("rmdir :{}".format(path))
        await _do_fs_rmdir_async(state, path)
    else:
        if args.verbose:
            print("rm :{}".format(path))
        await _do_fs_rmfile_async(state, path)


async def do_edit_async(state, args):
    """Async version of edit command.

    Args:
        state: State object with transport connection
        args: Command arguments with files list
    """
    await state.ensure_raw_repl_async()
    state.did_action()

    if not os.getenv("EDITOR"):
        raise CommandError("edit: $EDITOR not set")

    for src in args.files:
        src = src.lstrip(":")
        dest_fd, dest = tempfile.mkstemp(suffix=os.path.basename(src))
        try:
            print("edit :%s" % (src,))
            # Touch file if it doesn't exist
            await _do_fs_touchfile_async(state, src)
            # Read file
            data = await state.transport.fs_readfile_async(
                src, progress_callback=show_progress_bar
            )
            with open(dest_fd, "wb") as f:
                f.write(data)
            # Open editor (blocking)
            if os.system('%s "%s"' % (os.getenv("EDITOR"), dest)) == 0:
                with open(dest, "rb") as f:
                    await state.transport.fs_writefile_async(
                        src, f.read(), progress_callback=show_progress_bar
                    )
        finally:
            os.unlink(dest)


async def do_mount_async(state, args):
    """Async version of mount command.

    Args:
        state: State object with transport connection
        args: Command arguments with path and unsafe_links flag
    """
    await state.ensure_raw_repl_async()
    path = args.path[0]

    # Mount local uses sync methods - wrap if needed
    if hasattr(state.transport, "mount_local"):
        state.transport.mount_local(path, unsafe_links=args.unsafe_links)
    else:
        raise CommandError("mount: transport does not support local mounting")

    print(f"Local directory {path} is mounted at /remote")


async def do_umount_async(state, path):
    """Async version of umount command.

    Args:
        state: State object with transport connection
        path: Unused parameter for compatibility
    """
    await state.ensure_raw_repl_async()

    # Umount local uses sync methods - wrap if needed
    if hasattr(state.transport, "umount_local"):
        state.transport.umount_local()
    else:
        raise CommandError("umount: transport does not support local mounting")


async def do_mip_async(state, args):
    """Async version of mip (MicroPython package installer) command.

    Args:
        state: State object with transport connection
        args: Command arguments with command, packages, index, target, mpy flags
    """
    from .mip import _PACKAGE_INDEX, _install_package_async

    state.did_action()

    if args.command[0] == "install":
        await state.ensure_raw_repl_async()

        for package in args.packages:
            version = None
            if "@" in package:
                package, version = package.split("@")

            print("Install", package)

            if args.index is None:
                args.index = _PACKAGE_INDEX

            if args.target is None:
                await state.transport.exec_async("import sys")
                lib_paths = [
                    p
                    for p in await state.transport.eval_async("sys.path")
                    if not p.startswith("/rom") and p.endswith("/lib")
                ]
                if lib_paths and lib_paths[0]:
                    args.target = lib_paths[0]
                else:
                    raise CommandError(
                        "Unable to find lib dir in sys.path, use --target to override"
                    )

            if args.mpy is None:
                args.mpy = True

            try:
                await _install_package_async(
                    state.transport,
                    package,
                    args.index.rstrip("/"),
                    args.target,
                    version,
                    args.mpy,
                )
            except CommandError:
                print("Package may be partially installed")
                raise
            print("Done")
    else:
        raise CommandError(f"mip: '{args.command[0]}' is not a command")


async def do_romfs_async(state, args):
    """Async version of romfs command.

    Args:
        state: State object with transport connection
        args: Command arguments with command, path, output, partition, mpy flags
    """
    from .commands import _do_romfs_build, _do_romfs_deploy, _do_romfs_query

    if args.command[0] == "query":
        # Query doesn't need async - it just reads device info
        await state.ensure_raw_repl_async()
        state.did_action()

        # Call sync version for now (mostly just exec and eval calls)
        _do_romfs_query(state, args)
    elif args.command[0] == "build":
        # Build is local-only, doesn't need async
        _do_romfs_build(state, args)
    elif args.command[0] == "deploy":
        # Deploy writes to device - could benefit from async but uses complex protocol
        # For now, use sync version
        await state.ensure_raw_repl_async()
        state.did_action()
        _do_romfs_deploy(state, args)
    else:
        raise CommandError(
            f"romfs: '{args.command[0]}' is not a command; pass romfs --help for a list"
        )


# Sync wrappers for backward compatibility
def do_filesystem_sync_wrapper(state, args):
    """Sync wrapper for async filesystem command."""
    asyncio.run(do_filesystem_async(state, args))


def do_edit_sync_wrapper(state, args):
    """Sync wrapper for async edit command."""
    asyncio.run(do_edit_async(state, args))


def do_mount_sync_wrapper(state, args):
    """Sync wrapper for async mount command."""
    asyncio.run(do_mount_async(state, args))


def do_umount_sync_wrapper(state, args):
    """Sync wrapper for async umount command."""
    asyncio.run(do_umount_async(state, args))


def do_mip_sync_wrapper(state, args):
    """Sync wrapper for async mip command."""
    asyncio.run(do_mip_async(state, args))


def do_romfs_sync_wrapper(state, args):
    """Sync wrapper for async romfs command."""
    asyncio.run(do_romfs_async(state, args))
