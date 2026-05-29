#!/usr/bin/env python3
"""Run a set of unittest-based test files under one or more MicroPython
variants and emit a per-testcase markdown comparison report.

Usage (run from anywhere):
    tools/make_report.py --variant name=/path/to/micropython [--variant ...] \
                         [--keep-path name] [--keep-path ...] \
                         [--out report.md] [paths ...]

`paths` may be individual `.py` files or directories (recursed for `.py`),
resolved relative to the repository's `tests/` directory.
Defaults to `typing typing/pep`.

Each variant gets a column. Cell values use short tags:
    ok  xfail  xpass  skip  FAIL  ERROR
    skip covers both runtime `skipTest()` calls and testcases whose whole
    file SKIP'd (or crashed) on this variant; the file's tests are still
    listed if another variant ran them.

`--keep-path` can be specified for individual variants by name. If specified
for a variant, MICROPYPATH will not be overridden when running tests for
that variant, preserving the existing environment's module search path.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
TESTS_DIR = os.path.join(REPO_ROOT, "tests")

# unittest line:  "test_name (qualified.Class) ... <result>"
_LINE_RE = re.compile(
    r"^(?P<name>\S+) \((?P<cls>[^)]+)\) \.\.\.\s*(?P<result>.+?)\s*$"
)

_RESULT_TAG = {
    "ok": "ok",
    "FAIL": "FAIL",
    "ERROR": "ERROR",
    "expected failure": "xfail",
    "unexpected success": "xpass",
}


def parse_unittest_output(text):
    """Return list of (cls, name, tag) parsed from unittest stdout."""
    results = []
    for line in text.splitlines():
        m = _LINE_RE.match(line)
        if not m:
            continue
        raw = m.group("result")
        if raw.startswith("skipped"):
            tag = "skip"
        else:
            tag = _RESULT_TAG.get(raw, raw)
        results.append((m.group("cls"), m.group("name"), tag))
    return results


def read_header_comments(file_path, max_lines=5):
    """Return up to max_lines of leading `#` comment lines from file_path,
    with the leading '#' and one optional space stripped. Stops at the first
    non-comment, non-blank line. Blank lines within the leading block are
    skipped."""
    lines = []
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                s = raw.rstrip("\n")
                stripped = s.lstrip()
                if not stripped:
                    if lines:
                        break
                    continue
                if not stripped.startswith("#"):
                    break
                text = stripped[1:]
                if text.startswith(" "):
                    text = text[1:]
                lines.append(text)
                if len(lines) >= max_lines:
                    break
    except OSError:
        return []
    return lines


def collect_test_files(paths):
    files = []
    for p in paths:
        full = p if os.path.isabs(p) else os.path.join(TESTS_DIR, p)
        if os.path.isfile(full) and full.endswith(".py"):
            files.append(os.path.relpath(full, TESTS_DIR))
        elif os.path.isdir(full):
            for entry in sorted(os.listdir(full)):
                sub = os.path.join(full, entry)
                if os.path.isfile(sub) and entry.endswith(".py"):
                    files.append(os.path.relpath(sub, TESTS_DIR))
        else:
            print("warning: skipping %s (not found)" % p, file=sys.stderr)
    return files


def run_variant(binary, test_file, keep_path=False):
    """Run one test file under one variant. Return (stdout, returncode)."""
    env = os.environ.copy()
    if not keep_path:
        env["MICROPYPATH"] = os.pathsep.join(
            (
                ".frozen",
                os.path.join(REPO_ROOT, "extmod"),
                os.path.join(REPO_ROOT, "lib", "micropython-lib", "python-stdlib", "unittest"),
            )
        )
    try:
        proc = subprocess.run(
            [binary, test_file],
            cwd=TESTS_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        return proc.stdout.decode("utf-8", "replace"), proc.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except FileNotFoundError:
        return "BINARY NOT FOUND: %s" % binary, -1


def get_binary_size(binary):
    """Return dict with text/data/bss/total sizes (bytes) for `binary`,
    or None if `size` is unavailable or the binary doesn't exist."""
    if not os.path.isfile(binary):
        return None
    try:
        proc = subprocess.run(
            ["size", binary],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    lines = proc.stdout.decode("utf-8", "replace").splitlines()
    if len(lines) < 2:
        return None
    # Expected: "   text\tdata\tbss\tdec\thex\tfilename"
    parts = lines[1].split()
    if len(parts) < 4:
        return None
    try:
        text, data, bss, total = (int(parts[i]) for i in range(4))
    except ValueError:
        return None
    return {"text": text, "data": data, "bss": bss, "total": total}


def _fmt_kb(n):
    if n is None:
        return "-"
    return "{:,}".format(n).replace(",", "_")


def render_markdown(variant_names, files, table, file_summary, sizes, headers):
    out = []
    out.append("# Test report\n")
    out.append("## Summary\n")
    out.append(
        "Legend: **ok**=passed, **xfail**=expected failure, **xpass**=unexpected "
        "success, **skip**=test skipped (includes whole-file SKIP on this "
        "variant), **FAIL**=test failed, **ERROR**=test errored (also used when the test module crashed). "
        "Firmware sizes are reported in bytes from `size <binary>`.\n"
    )
    out.append(
        "| Variant | OK | xfail | xpass | skip | FAIL | ERROR | total | text | data | bss | size | Δsize |"
    )
    out.append("|:---|" + "---:|" * 12)
    baseline_size = None
    if variant_names:
        first_size = (sizes.get(variant_names[0]) or {}).get("total")
        baseline_size = first_size
    for v in variant_names:
        c = file_summary[v]
        s = sizes.get(v) or {}
        total_size = s.get("total")
        if total_size is None or baseline_size is None:
            delta = "-"
        elif v == variant_names[0]:
            delta = "ref"
        else:
            d = total_size - baseline_size
            delta = ("{:+,}".format(d)).replace(",", "_")
        out.append(
            "| %s | %d | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s | %s |"
            % (
                v,
                c["ok"],
                c["xfail"],
                c["xpass"],
                c["skip"],
                c["FAIL"],
                c["ERROR"],
                c["total"],
                _fmt_kb(s.get("text")),
                _fmt_kb(s.get("data")),
                _fmt_kb(s.get("bss")),
                _fmt_kb(s.get("total")),
                delta,
            )
        )
    out.append("")
    for f in files:
        rows = [(k, v) for k, v in table.items() if k[0] == f]
        if not rows:
            continue
        out.append("## " + f)
        hdr_lines = headers.get(f) or []
        if hdr_lines:
            for hl in hdr_lines:
                out.append("    " + hl)
            out.append("")
        header = "| Class | Test | " + " | ".join(variant_names) + " |"
        sep = "|" + "---|" * (2 + len(variant_names))
        out.append(header)
        out.append(sep)
        for (_f, cls, name), per in rows:
            cells = [per.get(v, "skip") for v in variant_names]
            out.append("| %s | %s | %s |" % (cls, name, " | ".join(cells)))
        out.append("")
    return "\n".join(out)


def bold_failures(text):
    return re.sub(r"\b(FAIL|ERROR|xpass)\b", r"**\1**", text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--variant",
        action="append",
        required=True,
        help="name=path to a micropython binary (may be repeated)",
    )
    ap.add_argument(
        "--keep-path",
        action="append",
        default=[],
        help="variant name for which to keep MICROPYPATH (do not override it)",
    )
    ap.add_argument("--out", default="-", help="markdown output file (default: stdout)")
    ap.add_argument(
        "paths",
        nargs="*",
        default=["typing", "typing/pep"],
        help="test files or directories (relative to tests/)",
    )
    args = ap.parse_args()

    variants = OrderedDict()
    for spec in args.variant:
        if "=" not in spec:
            ap.error("--variant must be name=path")
        name, _, path = spec.partition("=")
        variants[name] = path

    # Build a set of variant names for which to keep the path
    keep_path_variants = set(args.keep_path)

    files = collect_test_files(args.paths)
    table = OrderedDict()  # (file, cls, name) -> {variant: tag}
    file_status = {}  # (file, variant) -> "ran" | "skip" | "crash"
    file_summary = {
        v: dict.fromkeys(
            ("ok", "xfail", "xpass", "skip", "FAIL", "ERROR", "total"), 0
        )
        for v in variants
    }
    sizes = {v: get_binary_size(p) for v, p in variants.items()}

    for f in files:
        for vname, vbin in variants.items():
            keep_path = vname in keep_path_variants
            text, rc = run_variant(vbin, f, keep_path=keep_path)
            first_lines = text.splitlines()[:3] if text else []
            if "SKIP" in first_lines:
                file_status[(f, vname)] = "skip"
                continue
            if rc != 0:
                file_status[(f, vname)] = "crash"
            else:
                file_status[(f, vname)] = "ran"
            cases = parse_unittest_output(text)
            for cls, name, tag in cases:
                if cls.startswith("__main__."):
                    cls = cls.replace("__main__.", "")
                key = (f, cls, name)
                if key not in table:
                    table[key] = {}
                # Count using the original tag before bolding
                if tag in file_summary[vname]:
                    file_summary[vname][tag] += 1
                file_summary[vname]["total"] += 1
                # Apply bold formatting for display
                tag = bold_failures(tag)
                table[key][vname] = tag

    # Second pass: testcases that some variants ran but others did not are
    # counted as `skip` (whole-file SKIP) or `ERROR` (variant crashed) so
    # per-variant totals match the global row count.
    for key, per in table.items():
        f = key[0]
        for vname in variants:
            if vname in per:
                continue
            status = file_status.get((f, vname), "skip")
            tag = "ERROR" if status == "crash" else "skip"
            per[vname] = tag
            file_summary[vname][tag] += 1
            file_summary[vname]["total"] += 1

    headers = {f: read_header_comments(os.path.join(TESTS_DIR, f)) for f in files}
    md = render_markdown(list(variants), files, table, file_summary, sizes, headers)
    if args.out == "-":
        print(md)
    else:
        with open(args.out, "w") as fh:
            fh.write(md)
        print("Wrote %s (%d rows)" % (args.out, len(table)), file=sys.stderr)


if __name__ == "__main__":
    main()
