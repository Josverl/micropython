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

from .commands import (
    CommandError,
    _remote_path_basename,
    _remote_path_dirname,
    _remote_path_join,
    human_size,
    show_progress_bar,
)
from .transport import TransportError, TransportExecError, stdout_write_bytes


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
    if hasattr(state.transport, "exec_raw_no_follow_async"):
        await state.transport.exec_raw_no_follow_async(pyfile)

        # Follow output if requested
        if args.follow:
            ret, ret_err = await state.transport.follow_async(
                timeout=None, data_consumer=stdout_write_bytes
            )
            if ret_err:
                stdout_write_bytes(ret_err)
                raise TransportExecError(1, ret_err)
    else:
        # Fall back to sync version
        state.transport.exec_raw_no_follow(pyfile)
        if args.follow:
            ret, ret_err = state.transport.follow(timeout=None, data_consumer=stdout_write_bytes)
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
    if hasattr(state.transport, "eval_async"):
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
    if hasattr(state.transport, "exec_raw_async"):
        ret, ret_err = await state.transport.exec_raw_async(
            pyfile, data_consumer=stdout_write_bytes
        )
    else:
        ret, ret_err = state.transport.exec_raw(pyfile, data_consumer=stdout_write_bytes)

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
    import hashlib

    from .commands import CommandError, _remote_path_basename, show_progress_bar

    await state.ensure_raw_repl_async()

    # Download the contents of source
    if src.startswith(":"):
        if hasattr(state.transport, "fs_readfile_async"):
            data = await state.transport.fs_readfile_async(
                src[1:], progress_callback=show_progress_bar
            )
        else:
            data = state.transport.fs_readfile(src[1:], progress_callback=show_progress_bar)
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
                if hasattr(state.transport, "fs_hashfile"):
                    remote_hash = state.transport.fs_hashfile(dest[1:], "sha256")
                    source_hash = hashlib.sha256(data).digest()
                    if remote_hash == source_hash:
                        print("Up to date:", dest[1:])
                        return
            except OSError:
                pass

        # Write to remote
        if hasattr(state.transport, "fs_writefile_async"):
            await state.transport.fs_writefile_async(
                dest[1:], data, progress_callback=show_progress_bar
            )
        else:
            state.transport.fs_writefile(dest[1:], data, progress_callback=show_progress_bar)
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
                if args.recursive:
                    await do_filesystem_recursive_cp_async(
                        state, path, cp_dest, len(paths) > 1, not args.force
                    )
                else:
                    await do_filesystem_cp_async(
                        state, path, cp_dest, len(paths) > 1, not args.force
                    )
            elif command == "tree":
                await do_filesystem_tree_async(state, path, args)
    except OSError as er:
        raise CommandError("{}: {}: {}.".format(command, er.strerror, os.strerror(er.errno)))
    except TransportError as er:
        raise CommandError("Error with transport:\n{}".format(er.args[0]))


async def _do_fs_printfile_async(state, src, chunk_size=256):
    """Async helper to print file contents."""
    await state.transport.exec_async(
        f"with open({src!r}, 'rb') as f:\n while 1:\n  b=f.read({chunk_size})\n  if not b:break\n  print(b,end='')"
    )


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
    result = await state.transport.eval_async("h.digest()", parse=False)
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


async def do_filesystem_recursive_cp_async(state, src, dest, multiple, check_hash):
    """Async recursive directory copy."""
    # Ignore trailing / on both src and dest
    src = src.rstrip("/" + os.path.sep + (os.path.altsep if os.path.altsep else ""))
    dest = dest.rstrip("/" + os.path.sep + (os.path.altsep if os.path.altsep else ""))

    # Check if destination exists
    if dest.startswith(":"):
        try:
            await state.transport.fs_stat_async(dest[1:])
            dest_exists = True
        except OSError:
            dest_exists = False
    else:
        dest_exists = os.path.exists(dest)

    # Recursively find all files to copy
    dirs = []
    files = []

    async def _list_recursive_async(
        base, src_path, dest_path, src_join_fun, src_isdir_fun, src_listdir_fun
    ):
        src_path_joined = src_join_fun(base, *src_path)
        is_dir = await src_isdir_fun(src_path_joined)
        if is_dir:
            if dest_path:
                dirs.append(dest_path)
            entries = await src_listdir_fun(src_path_joined)
            for entry in entries:
                await _list_recursive_async(
                    base,
                    src_path + [entry],
                    dest_path + [entry],
                    src_join_fun,
                    src_isdir_fun,
                    src_listdir_fun,
                )
        else:
            files.append((dest_path, src_path_joined))

    if src.startswith(":"):
        src_dirname = [_remote_path_basename(src[1:])]
        dest_dirname = src_dirname if dest_exists else []

        async def remote_isdir(p):
            try:
                stat = await state.transport.fs_stat_async(p)
                return stat[0] & 0x4000
            except OSError:
                return False

        async def remote_listdir(p):
            entries = await state.transport.fs_listdir_async(p)
            return [x.name for x in entries]

        await _list_recursive_async(
            _remote_path_dirname(src[1:]),
            src_dirname,
            dest_dirname,
            src_join_fun=_remote_path_join,
            src_isdir_fun=remote_isdir,
            src_listdir_fun=remote_listdir,
        )
    else:
        src_dirname = [os.path.basename(src)]
        dest_dirname = src_dirname if dest_exists else []

        async def local_isdir(p):
            return os.path.isdir(p)

        async def local_listdir(p):
            return os.listdir(p)

        await _list_recursive_async(
            os.path.dirname(src),
            src_dirname,
            dest_dirname,
            src_join_fun=os.path.join,
            src_isdir_fun=local_isdir,
            src_listdir_fun=local_listdir,
        )

    # If no directories, just copy as single file
    if not dirs:
        return await do_filesystem_cp_async(state, src, dest, multiple, check_hash)

    async def _mkdir(a, *b):
        try:
            if a.startswith(":"):
                await _do_fs_mkdir_async(state, _remote_path_join(a[1:], *b))
            else:
                os.mkdir(os.path.join(a, *b))
        except FileExistsError:
            pass

    # Create destination if needed
    if not dest_exists:
        await _mkdir(dest)

    # Create all subdirectories
    for d in dirs:
        await _mkdir(dest, *d)

    # Copy all files
    files.sort()
    for dest_path_split, src_path_joined in files:
        if src.startswith(":"):
            src_path_joined = ":" + src_path_joined
        if dest.startswith(":"):
            dest_path_joined = ":" + _remote_path_join(dest[1:], *dest_path_split)
        else:
            dest_path_joined = os.path.join(dest, *dest_path_split)

        await do_filesystem_cp_async(state, src_path_joined, dest_path_joined, False, check_hash)


async def do_filesystem_tree_async(state, path, args):
    """Async filesystem tree display."""
    connectors = ("├── ", "└── ")

    async def _tree_recursive(path, prefix=""):
        try:
            entries = await state.transport.fs_listdir_async(path)
        except OSError as e:
            print(f"{prefix}[Error reading directory: {e}]")
            return

        entries = sorted(entries, key=lambda x: (not (x.st_mode & 0x4000), x.name))

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = connectors[1] if is_last else connectors[0]
            is_dir = entry.st_mode & 0x4000

            if args.verbose:
                size_str = "" if is_dir else f" ({human_size(entry.st_size)})"
                print(f"{prefix}{connector}{entry.name}{'/' if is_dir else ''}{size_str}")
            else:
                print(f"{prefix}{connector}{entry.name}{'/' if is_dir else ''}")

            if is_dir:
                extension = "    " if is_last else "│   "
                entry_path = _remote_path_join(path, entry.name)
                await _tree_recursive(entry_path, prefix + extension)

    if not path or path == ".":
        path = "/"

    # Check if path is a directory
    try:
        stat = await state.transport.fs_stat_async(path)
        if not (stat[0] & 0x4000):
            raise CommandError(f"tree: {path} is not a directory")
    except OSError as e:
        raise CommandError(f"tree: {path}: {e}")

    if args.verbose:
        print(path + "/")
    else:
        print(path + "/")

    await _tree_recursive(path)


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
