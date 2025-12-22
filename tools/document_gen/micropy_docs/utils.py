"""Utility functions for macro processing."""

import re
from typing import Any, Dict, List, Tuple


def module_hint(relpath: str) -> str:
    """Extract a module hint from a relative path (e.g., 'ports/esp32' or 'extmod')."""
    parts = relpath.split("/")
    if not parts:
        return ""
    if parts[0] == "ports" and len(parts) > 1:
        return f"ports/{parts[1]}"
    return parts[0]


def macro_category(name: str, prefix: str = "MICROPY_") -> str:
    """Extract the category token from a macro name (e.g., 'MICROPY_PY_FOO' -> 'PY')."""
    rest = name.removeprefix(prefix)
    token = rest.split("_", 1)[0]
    return token or "MISC"


def choose_best_description(defs_for_name: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Choose the best description from a list of macro definitions.

    Returns (description, location) where location is 'file:line'.
    Prefers non-empty description, else longest comment, else longest value.
    """
    descr_candidates = [d for d in defs_for_name if d.get("description")]
    if descr_candidates:
        descr_candidates.sort(key=lambda d: len(d["description"]), reverse=True)
        return descr_candidates[0][
            "description"
        ], f"{descr_candidates[0]['file']}:{descr_candidates[0]['line']}"

    comment_candidates = [d for d in defs_for_name if d.get("comment")]
    if comment_candidates:
        comment_candidates.sort(key=lambda d: len(d["comment"]), reverse=True)
        return comment_candidates[0][
            "comment"
        ], f"{comment_candidates[0]['file']}:{comment_candidates[0]['line']}"

    value_candidates = [d for d in defs_for_name if d.get("value")]
    if value_candidates:
        value_candidates.sort(key=lambda d: len(d["value"]), reverse=True)
        return value_candidates[0][
            "value"
        ], f"{value_candidates[0]['file']}:{value_candidates[0]['line']}"

    first = defs_for_name[0]
    return "", f"{first['file']}:{first['line']}"


def sanitize_for_markdown(text: str) -> str:
    """Keep only printable characters and common whitespace, exclude replacement char."""
    if not text:
        return ""
    return "".join(c for c in text if (c.isprintable() or c in "\n\t") and c != "\ufffd")


def strip_trailing_digits(name: str) -> str:
    """Strip trailing digits from a name: LED1 -> LED, LED12 -> LED, LED -> LED."""
    return re.sub(r"\d+$", "", name)


def extract_second_level(name: str, category: str, prefix: str = "MICROPY_") -> str:
    """
    Extract a second-level grouping from macro names like MICROPY_HW_USB_* -> USB.

    Trailing sequence numbers are stripped so LED, LED1, LED2 all map to LED.
    Examples:
        MICROPY_HW_I2C0 -> I2C
        MICROPY_HW_I2C0_SCL -> I2C
        MICROPY_HW_LED -> LED
        MICROPY_HW_LED1 -> LED
    """
    full_prefix = f"{prefix}{category}_"
    if not name.startswith(full_prefix):
        return ""
    rest = name[len(full_prefix) :]
    parts = rest.split("_")
    if len(parts) >= 1 and parts[0]:
        return strip_trailing_digits(parts[0])
    return ""


def code_search_md(word: str) -> str:
    """Generate a markdown link to GitHub code search for a macro."""
    return f"[`{word}`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20{word}&type=code)"
