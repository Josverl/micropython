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
# importer to instead do `import stubs.modname` with sys.path set to `docs`.
# Then we fix-up the `__name__ attribute on the module, and the `__module__`
# attribute on any included functions, types, etc so that autodoc thinks that
# they were imported the usual way.
#
# Additionally, we add the directory containing this file to sys.path so
# our copy of `annotations.py` is used instead, which injects the necessary
# rST code into the docstrings.

def setup(app):
    import os, sys
    from sphinx.util import logging

    logger = logging.getLogger(__name__)

    # Patch the autodoc importer.
    from sphinx.ext.autodoc import importer
    _original_importer_import_module = importer.import_module

    def _hook_importer_import_module(modname, *args, **kwargs):
        logger.debug("[autodoc_import] _hook_importer_import_module: %s", modname)
        try:
            saved_path = sys.path
            # This is directory containing this file (which contains annotations.py).
            ext_path = os.path.dirname(__file__)
            # This is the top-level docs directory (which contains stubs/<modname>).
            docs_path = os.path.dirname(ext_path)
            sys.path = [os.path.abspath(ext_path), os.path.abspath(docs_path)]
            try:
                module = _original_importer_import_module("stubs." + modname, *args, **kwargs)
            finally:
                sys.path = saved_path

            # Fix module.__name__ and module.Foo.__module__
            module.__name__ = modname
            for key in dir(module):
                x = getattr(module, key)
                if hasattr(x, '__module__') and getattr(x, "__module__") == "stubs." + modname:
                    setattr(x, '__module__', modname)

        except ImportError:
            # This wasn't a module that we have stubs for (or the import
            # failed because of an issue with the stub). This shouldn't
            # happen -- we provide stubs for everything, and never want
            # to (automatically) document the CPython version instead.
            logger.error('[autodoc_import] could find/load micropython stubs for %s, using system version', modname)
            module = _original_importer_import_module(modname, *args, **kwargs)
        return module

    importer.import_module = _hook_importer_import_module

    # Patch the importer used by ModuleAnalyzer.
    import sphinx.pycode
    _original_pycode_import_module = sphinx.pycode.import_module

    def _hook_pycode_import_module(modname):
        logger.debug("[autodoc_import] _hook_pycode_import_module: %s", modname)
        try:
            module = _original_pycode_import_module("stubs." + modname)
            module.__name__ = modname
            return module
        except:
            return _original_pycode_import_module(modname)

    sphinx.pycode.import_module = _hook_pycode_import_module

    return {'version': "1.0", "parallel_read_safe": True, 'parallel_write_safe': True,}
