# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2023 Jim Mussared
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

# This Sphinx extension hooks the importer used by autodoc to allow us to have
# modules with the same name as builtins.
#
# Autodoc just does (via importlib) the equivalent of `import <modname>`, so
# any built-in module that we try to autodoc will get the CPython version
# instead of finding the one in `docs/stubs`. So what we do is hook autodoc's
# importer to change the sys.path to include our stubs directory, and the
# subs_helper folder that contains .py versions of the typings and
# typings_helper modules.
#
# Additionally, we add the directory containing this file to sys.path so
# our copy of `annotations.py` is used instead, which injects the necessary
# rST code into the docstrings.


from pathlib import Path
import shutil
from sphinx.application import Sphinx


def setup(app: Sphinx):
    import sys
    from sphinx.util import logging
    import sphinx.pycode
    from sphinx.ext.autodoc import importer

    logger = logging.getLogger(__name__)
    logger.info("[autodoc_import] setup and copy stubs to _stubs")

    # Patch the autodoc importer.
    ext_path = Path(__file__).parent
    docs_path = ext_path.parent
    stubs_path = docs_path / "_stubs"
    helpers_path = docs_path / "stubs_helpers"
    # use the path in the correct order of priority
    autodoc_paths = [
        str(ext_path.absolute()),
        str(docs_path.absolute()),
        str(stubs_path.absolute()),
        str(helpers_path.absolute()),
    ]
    if not copy_and_rename_module(docs_path / "stubs", docs_path / "_stubs"):
        logger.error("[autodoc_import] failed to copy stubs to _stubs")
        return

    _original_importer_import_module = importer.import_module

    def _hook_importer_import_module(modname: str, *args, **kwargs):
        logger.debug("[autodoc_import] _hook_importer_import_module: %s", modname)
        try:
            saved_sys_path = sys.path
            sys.path = autodoc_paths
            try:
                logger.debug(f"[autodoc_import] importing stub {modname}")
                module = _original_importer_import_module(f"_stubs.{modname}", *args, **kwargs)
            finally:
                sys.path = saved_sys_path

            # Fix module.__name__ and module.Foo.__module__
            module.__name__ = modname
            for key in dir(module):
                x = getattr(module, key)
                if hasattr(x, "__module__") and getattr(x, "__module__") == "stubs." + modname:
                    setattr(x, "__module__", modname)

        except ImportError as e:
            # This wasn't a module that we have stubs for (or the import
            # failed because of an issue with the stub). This shouldn't
            # happen -- we provide stubs for everything, and never want
            # to (automatically) document the CPython version instead.
            logger.error(
                f"[autodoc_import] could find/load micropython stub: {modname}, attempting to load the system version"
            )
            logger.exception(e)
            module = _original_importer_import_module(modname, *args, **kwargs)
        return module

    importer.import_module = _hook_importer_import_module

    _original_pycode_import_module = sphinx.pycode.import_module  # type: ignore

    def _hook_pycode_import_module(modname):
        logger.debug("[autodoc_import] _hook_pycode_import_module: %s", modname)
        try:
            module = _original_pycode_import_module("stubs." + modname)
            module.__name__ = modname
            return module
        except:
            return _original_pycode_import_module(modname)

    sphinx.pycode.import_module = _hook_pycode_import_module  # type: ignore

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def copy_and_rename_module(src: Path, dst: Path):
    """Copy a module from src to dst, renaming all .pyi files to .py"""
    if not src.is_dir():
        return False
    if dst.exists():
        # clear out the destination directory
        shutil.rmtree(dst)
    try:
        dst.mkdir(parents=True, exist_ok=True)
        # add  .gitignore file
        with open(dst.joinpath(".gitignore"), "w") as f:
            f.write("*")

        shutil.copytree(
            src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "__pycache__")
        )

        # rename all .pyi files to .py so that they are picked up by autodoc
        for f in dst.rglob("*.pyi"):
            shutil.move(f, f.with_suffix(".py"))
        return True
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")
        return False
