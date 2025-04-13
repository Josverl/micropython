# Micropython package installer
# Ported from micropython-lib/micropython/mip/mip.py.
# MIT license; Copyright (c) 2022 Jim Mussared

import fnmatch
from typing import List
import urllib.error
import urllib.request
import json
import os
import os.path
from pathlib import Path

from .commands import CommandError, show_progress_bar


_PACKAGE_INDEX = "https://micropython.org/pi/v2"

allowed_mip_url_prefixes = ("http://", "https://", "github:", "gitlab:")


# This implements os.makedirs(os.dirname(path))
def _ensure_path_exists(transport, path):
    split = path.split("/")

    # Handle paths starting with "/".
    if not split[0]:
        split.pop(0)
        split[0] = "/" + split[0]

    prefix = ""
    for i in range(len(split) - 1):
        prefix += split[i]
        if not transport.fs_exists(prefix):
            transport.fs_mkdir(prefix)
        prefix += "/"


def _rewrite_url(url, branch=None):
    if not branch:
        branch = "HEAD"
    if url.startswith("github:"):
        url = url[7:].split("/")
        url = (
            "https://raw.githubusercontent.com/"
            + url[0]
            + "/"
            + url[1]
            + "/"
            + branch
            + "/"
            + "/".join(url[2:])
        )
    elif url.startswith("gitlab:"):
        url = url[7:].split("/")
        url = (
            "https://gitlab.com/"
            + url[0]
            + "/"
            + url[1]
            + "/-/raw/"
            + branch
            + "/"
            + "/".join(url[2:])
        )
    return url


def _download_file(transport, url, dest):
    if url.startswith(allowed_mip_url_prefixes):
        try:
            with urllib.request.urlopen(url) as src:
                data = src.read()
        except urllib.error.HTTPError as e:
            if e.status == 404:
                raise CommandError(f"File not found: {url}")
            else:
                raise CommandError(f"Error {e.status} requesting {url}")
        except urllib.error.URLError as e:
            raise CommandError(f"{e.reason} requesting {url}")
    else:
        if "\\" in url:
            raise CommandError(f'Use "/" instead of "\\" in file URLs: {url!r}\n')
        try:
            with open(url, "rb") as f:
                data = f.read()
        except OSError as e:
            raise CommandError(f"{e.strerror} opening {url}")

    print("Installing:", dest)
    _ensure_path_exists(transport, dest)
    transport.fs_writefile(dest, data, progress_callback=show_progress_bar)


def _install_json(transport, package_json_url, index, target, version, mpy):
    base_url = ""
    if package_json_url.startswith(allowed_mip_url_prefixes):
        try:
            with urllib.request.urlopen(_rewrite_url(package_json_url, version)) as response:
                package_json = json.load(response)
        except urllib.error.HTTPError as e:
            if e.status == 404:
                raise CommandError(f"Package not found: {package_json_url}")
            else:
                raise CommandError(f"Error {e.status} requesting {package_json_url}")
        except urllib.error.URLError as e:
            raise CommandError(f"{e.reason} requesting {package_json_url}")
        base_url = package_json_url.rpartition("/")[0]
    elif package_json_url.endswith(".json"):
        try:
            with open(package_json_url, "r") as f:
                package_json = json.load(f)
        except OSError:
            raise CommandError(f"Error opening {package_json_url}")
        base_url = os.path.dirname(package_json_url)
    else:
        raise CommandError(f"Invalid url for package: {package_json_url}")
    for target_path, short_hash in package_json.get("hashes", ()):
        fs_target_path = target + "/" + target_path
        file_url = f"{index}/file/{short_hash[:2]}/{short_hash}"
        _download_file(transport, file_url, fs_target_path)
    for target_path, url in package_json.get("urls", ()):
        fs_target_path = target + "/" + target_path
        if base_url and not url.startswith(allowed_mip_url_prefixes):
            url = f"{base_url}/{url}"  # Relative URLs
        _download_file(transport, _rewrite_url(url, version), fs_target_path)
    for dep, dep_version in package_json.get("deps", ()):
        _install_package(transport, dep, index, target, dep_version, mpy)


def _install_package(transport, package, index, target, version, mpy):
    if package.startswith(allowed_mip_url_prefixes):
        if package.endswith(".py") or package.endswith(".mpy"):
            print(f"Downloading {package} to {target}")
            _download_file(
                transport, _rewrite_url(package, version), target + "/" + package.rsplit("/")[-1]
            )
            return
        else:
            if not package.endswith(".json"):
                if not package.endswith("/"):
                    package += "/"
                package += "package.json"
            print(f"Installing {package} to {target}")
    elif package.endswith(".json"):
        pass
    else:
        if not version:
            version = "latest"
        print(f"Installing {package} ({version}) from {index} to {target}")

        mpy_version = "py"
        if mpy:
            transport.exec("import sys")
            mpy_version = transport.eval("getattr(sys.implementation, '_mpy', 0) & 0xFF") or "py"

        package = f"{index}/package/{mpy_version}/{package}/{version}.json"

    _install_json(transport, package, index, target, version, mpy)


def _do_mip_search(index: str, filter: List[str]):
    """
    Search for packages in the package index.
    Args:
        index (str): The URL of the package index.
        filter (List[str]): List of patterns to filter packages.
    """
    try:
        with urllib.request.urlopen(index) as response:
            index_data = json.load(response)
    except Exception as e:
        raise CommandError(f"Error loading package index: {index}") from e

    print("Available packages:")
    for p in index_data['packages']:
        if not any(fnmatch.fnmatch(p["name"], pattern) for pattern in filter):
            continue
        print(f"{p['name']:<20} {p['version']:>8} {p['description']}")


def do_mip(state, args):
    state.did_action()

    if args.command[0] == "search":
        index = (args.index or _PACKAGE_INDEX).rstrip('/') + "/index.json"
        filter = args.packages or ["*"]
        _do_mip_search(index, filter)

    elif args.command[0] == "install":
        state.ensure_raw_repl()
        packages = []
        if args.requirement:
            if len(args.packages) != 1:
                raise CommandError("Only a single requirements file can be specified")
            packages = parse_requirements_file(Path(args.packages[0]))
        else:
            packages = args.packages

        state.ensure_raw_repl()

        for package in packages:
            version = None
            if "==" in package:
                package, version = package.split("==")
            elif "@" in package:
                # OK git github/gitlab urls, deprecated for others ?
                package, version = package.split("@")

            print("Install", package)

            if args.index is None:
                args.index = _PACKAGE_INDEX

            if args.target is None:
                state.transport.exec("import sys")
                lib_paths = [
                    p
                    for p in state.transport.eval("sys.path")
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
                _install_package(
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


def parse_requirements_file(requirements_file: Path):
    """Load a list of packages from a requirements.txt or pyproject.toml file"""
    # just in time import
    import sys

    packages = []
    if not requirements_file.exists() and requirements_file.is_file():
        raise CommandError(f"Requirements file not found: {requirements_file}")

    if requirements_file.suffix == '.toml':
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib

        # read
        try:
            with open(requirements_file, "rb") as f:
                toml_data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise CommandError("Unable to read requirements file") from e
        try:
            packages = toml_data['tool']['mpremote']['mip']
        except KeyError as e:
            raise CommandError(f"No mpremote mip requirements could be located in: {f}") from e

    else:
        # simplified requirements format , no options
        # https://pip.pypa.io/en/stable/reference/requirements-file-format/
        with open(requirements_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.startswith("-"):
                        raise CommandError("Global options are not supported")
                    if any(seq in line for seq in ("<", "<=", "!=", ">=", ">", "!=", "~=", "===")):
                        # only '=='
                        # mip does not recognize https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers
                        raise CommandError("Only == is supported")
                    if any(seq in line for seq in ("[", "]", ";")):
                        raise CommandError("no extras or environment markers are supported")
                    packages.append(line)

    return packages

    # from urllib.parse import urlparse
    # if requirements_file.startswith("http://") or requirements_file.startswith("https://"):
    #     with urllib.request.urlopen(requirements_file) as f:
    #         for line in f:
    #             line = line.decode().strip()
    #             if line and not line.startswith("#"):
    #                 packages.append(line)
    #     return packages
