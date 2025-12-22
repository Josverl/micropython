"""
MicroPython MICROPY_* Macro Documentation Generator

This package scans the MicroPython codebase for MICROPY_* macros,
collects definitions and usages, optionally enriches descriptions
using Azure OpenAI, and generates markdown documentation.
"""

from .ai_enricher import AIEnricher
from .renderer import MarkdownRenderer
from .scanner import MacroScanner
from .utils import choose_best_description, macro_category, module_hint, sanitize_for_markdown

__all__ = [
    "MacroScanner",
    "AIEnricher",
    "MarkdownRenderer",
    "module_hint",
    "macro_category",
    "choose_best_description",
    "sanitize_for_markdown",
]

__version__ = "1.0.0"
