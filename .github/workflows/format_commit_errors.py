#!/usr/bin/env python3
"""Format verifygitlog.py error output into a Markdown summary for PR comments.

Usage
-----
Called by commit_formatting.yml:

    python .github/workflows/format_commit_errors.py

The script reads raw verifygitlog output from the environment variable
RAW_OUTPUT and writes a markdown-formatted block to GITHUB_OUTPUT.

It can also be run standalone for testing:

    RAW_OUTPUT="$(tools/verifygitlog.py ...)" python .github/workflows/format_commit_errors.py
    python .github/workflows/format_commit_errors.py --test
"""

import os
import re
import subprocess
import sys


def format_errors(raw:str) -> str:
    """Parse raw verifygitlog output and return a Markdown string.

    Each failing commit gets a header line followed by a bullet list of its
    errors.  Per-commit errors are deduplicated.
    """
    # Group errors by commit SHA, preserving discovery order.
    seen: dict[str, list[str]] = {}
    sha_order: list[str] = []

    for line in raw.splitlines():
        m = re.match(r"^error: commit ([0-9a-f]+): (.+)$", line)
        if not m:
            continue
        sha, raw_msg = m.group(1), m.group(2)
        msg = raw_msg.lstrip("* ")
        if sha not in seen:
            seen[sha] = []
            sha_order.append(sha)
        if msg not in seen[sha]:
            seen[sha].append(msg)

    parts: list[str] = []
    for sha in sha_order:
        try:
            title = subprocess.check_output(
                ["git", "log", "-1", "--format=%s", sha], text=True
            ).strip()
        except Exception:
            title = ""
        parts.append(f"**commit `{sha}`** {title}")
        for err in seen[sha]:
            parts.append(f"- {err}")
        parts.append("")

    return "\n".join(parts).rstrip()


def write_github_output(formatted: str) -> None:
    """Append the formatted value to GITHUB_OUTPUT using the heredoc syntax."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        raise RuntimeError("GITHUB_OUTPUT environment variable is not set")
    with open(github_output, "a") as f:
        f.write("formatted<<__HEREDOC__\n")
        f.write(formatted + "\n")
        f.write("__HEREDOC__\n")


def run_tests() -> None:
    """Quick self-tests – run with ``--test`` flag."""
    SAMPLE = """\
verify b008dc8
error: commit b008dc8: Unwanted email address: 198982749+Copilot@users.noreply.github.com
error: commit b008dc8: * first word of subject ("add") must be capitalised.
error: commit b008dc8: Subject line is too long (86 characters, max 72)
error: commit b008dc8: Subject prefix cannot begin with "." or "/".
error: commit b008dc8: Message must be signed-off. Use "git commit -s".
verify 0718a71
error: commit 0718a71: Unwanted email address: 198982749+Copilot@users.noreply.github.com
error: commit 0718a71: * must end with "."
error: commit 0718a71: * must start with "path: "
error: commit 0718a71: Subject line is too long (94 characters, max 72)
error: commit 0718a71: Message must be signed-off. Use "git commit -s".
See https://github.com/micropython/micropython/blob/master/CODECONVENTIONS.md
"""

    result = format_errors(SAMPLE)

    # Each commit must appear exactly once.
    assert result.count("commit `b008dc8`") == 1, "b008dc8 missing or duplicated"
    assert result.count("commit `0718a71`") == 1, "0718a71 missing or duplicated"

    # Error messages must appear.
    assert "first word of subject" in result
    assert "Subject line is too long (86 characters, max 72)" in result
    assert "Subject line is too long (94 characters, max 72)" in result

    # No raw 'verify' lines should bleed through.
    assert "verify b008dc8" not in result
    assert "See https://" not in result

    # Test deduplication: duplicate errors for the same SHA are suppressed.
    DUPES = """\
error: commit aabbcc1: Message must be signed-off. Use "git commit -s".
error: commit aabbcc1: Message must be signed-off. Use "git commit -s".
"""
    result2 = format_errors(DUPES)
    assert result2.count("signed-off") == 1, "Duplicate error not deduplicated"

    # Test empty input produces empty string.
    assert format_errors("") == ""
    assert format_errors("ok\n") == ""

    print("All tests passed.")


def main() -> None:
    if "--test" in sys.argv:
        run_tests()
        return

    raw = os.environ.get("RAW_OUTPUT", "")
    formatted = format_errors(raw)
    write_github_output(formatted)


if __name__ == "__main__":
    main()
