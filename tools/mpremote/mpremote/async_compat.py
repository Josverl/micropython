#!/usr/bin/env python3
#
# This file is part of the MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2025 Jos Verlinde
#


"""Compatibility utilities for asyncio across Python versions."""

import asyncio
import sys
from contextlib import asynccontextmanager

# Python 3.11+ has asyncio.timeout context manager
if sys.version_info >= (3, 11):
    from asyncio import timeout as asyncio_timeout
else:
    # For Python 3.10 and earlier, use async-timeout package or create a wrapper
    try:
        from async_timeout import timeout as asyncio_timeout
    except ImportError:
        # Fallback implementation using wait_for
        @asynccontextmanager
        async def asyncio_timeout(delay):
            """Compatibility timeout context manager for Python < 3.11."""
            try:
                yield
            except asyncio.TimeoutError:
                raise


def get_timeout(delay):
    """Get a timeout context manager compatible with current Python version.

    Args:
        delay: Timeout in seconds

    Returns:
        Context manager that raises asyncio.TimeoutError on timeout
    """
    return asyncio_timeout(delay)
