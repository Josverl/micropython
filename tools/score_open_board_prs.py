#!/usr/bin/env python3

import json
import re
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path


CACHE_DIR = Path(".cache/score_open_board_prs")

SEARCH_URL = (
    "https://api.github.com/search/issues"
    "?q=repo:micropython/micropython+is:pr+is:open+label:board-definition"
    "&per_page=100&page={page}"
)


def fetch_text(url: str, *, timeout: int = 60, retries: int = 3) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", url)
    cache_path = CACHE_DIR / cache_name
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "micropython-score-open-board-prs",
        },
    )

    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                text = response.read().decode("utf-8")
                cache_path.write_text(text, encoding="utf-8")
                return text
        except (TimeoutError, socket.timeout, urllib.error.URLError) as exc:
            last_error = exc
            if attempt == retries - 1:
                break
            time.sleep(1 + attempt)

    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def fetch_json(url: str) -> dict:
    return json.loads(fetch_text(url))


def iter_open_board_prs() -> list[dict]:
    items = []
    for page in range(1, 3):
        data = fetch_json(SEARCH_URL.format(page=page))
        page_items = data.get("items", [])
        items.extend(page_items)
        if len(page_items) < 100:
            break

    seen = set()
    prs = []
    for item in items:
        if "pull_request" not in item:
            continue
        number = item["number"]
        if number in seen:
            continue
        seen.add(number)
        prs.append(item)

    return sorted(prs, key=lambda pr: pr["number"], reverse=True)


def extract_filenames_from_patch(patch_text: str) -> list[str]:
    filenames = []
    for match in re.finditer(r"^\+\+\+ b/(.*?)$", patch_text, flags=re.MULTILINE):
        filename = match.group(1)
        if filename and filename != "/dev/null":
            filenames.append(filename)
    return filenames


def extract_board_dirs(filenames: list[str]) -> list[str]:
    board_dirs = set()
    for name in filenames:
        match = re.match(r"^(ports/[^/]+/boards/[^/]+)/", name)
        if match:
            board_dirs.add(match.group(1))
    return sorted(board_dirs)


def summarize_key_files(filenames: list[str]) -> str:
    interesting = []
    patterns = [
        (r"board\.json$", "board.json"),
        (r"mpconfigboard\.h$", "mpconfigboard.h"),
        (r"mpconfigboard\.(cmake|mk)$", "board build config"),
        (r"pins\.csv$", "pins.csv"),
        (r"manifest\.py$", "manifest.py"),
        (r"(board\.md|README\.md)$", "board docs"),
        (r"mpconfigvariant.*\.(cmake|mk)$", "variant configs"),
        (r"^tests/ports/[^/]+/", "port tests"),
    ]
    for pattern, label in patterns:
        if any(re.search(pattern, name) for name in filenames):
            interesting.append(label)
    return ", ".join(interesting)


def extract_body_summary(body: str) -> str:
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    lines = [line.strip() for line in body.splitlines()]
    filtered = []
    for line in lines:
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("```"):
            continue
        if "Thanks for submitting a Pull Request" in line:
            continue
        filtered.append(line)

    summary_parts = []
    for line in filtered[:12]:
        if line.startswith("-") or line.startswith("*"):
            summary_parts.append(line.lstrip("-* "))
        elif not summary_parts:
            summary_parts.append(line)
        if len(" ".join(summary_parts)) > 220:
            break

    summary = " ".join(summary_parts).strip()
    summary = re.sub(r"`", "", summary)
    summary = re.sub(r"\*\*?", "", summary)
    summary = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", summary)
    summary = re.sub(r"\s+", " ", summary)
    return summary[:240].rstrip()


def detect_port(pr: dict, title: str) -> str:
    match = re.match(r"^([a-z0-9_\-]+)/", title, flags=re.IGNORECASE)
    if match:
        return match.group(1).lower()

    for label in pr.get("labels", []):
        name = label.get("name", "")
        if name.startswith("port-"):
            return name.removeprefix("port-")

    return "unknown"


def has_testing_section(body: str) -> bool:
    return bool(
        re.search(r"(^|\n)\s*#{1,3}\s*Testing\b", body, flags=re.IGNORECASE)
        or re.search(r"\bmake\s+BOARD=", body)
    )


def score_pr(pr: dict) -> tuple[str, str]:
    number = pr["number"]
    title = (pr.get("title") or "").replace("|", "\\|")
    url = pr["html_url"]
    body = pr.get("body") or ""
    patch_url = pr["pull_request"]["patch_url"]
    patch_text = fetch_text(patch_url)
    filenames = extract_filenames_from_patch(patch_text)
    board_dirs = extract_board_dirs(filenames)

    has_board_json = any(re.match(r"^ports/[^/]+/boards/[^/]+/board\.json$", name) for name in filenames)
    has_mp_h = any(re.match(r"^ports/[^/]+/boards/[^/]+/mpconfigboard\.h$", name) for name in filenames)
    has_mp_cfg = any(re.match(r"^ports/[^/]+/boards/[^/]+/mpconfigboard\.(cmake|mk)$", name) for name in filenames)
    has_pins = any(re.match(r"^ports/[^/]+/boards/[^/]+/pins\.csv$", name) for name in filenames)
    has_board_path = any(re.match(r"^ports/[^/]+/boards/[^/]+/", name) for name in filenames)
    has_testing = has_testing_section(body)

    m1 = has_board_json
    m2 = has_mp_h and has_mp_cfg
    m3 = has_pins
    m4 = has_testing
    m5 = has_board_path
    must_score = 2 * sum((m1, m2, m3, m4, m5))

    bonus_manifest = any(re.match(r"^ports/[^/]+/boards/[^/]+/manifest\.py$", name) for name in filenames)
    bonus_docs = any(re.match(r"^ports/[^/]+/boards/[^/]+/(board\.md|README\.md)$", name) for name in filenames)
    bonus_variants = any(re.match(r"^ports/[^/]+/boards/[^/]+/mpconfigvariant.*\.(cmake|mk)$", name) for name in filenames)
    bonus_tests = any(re.match(r"^tests/ports/[^/]+/", name) for name in filenames)
    bonus_detail = len(body) > 700
    bonus_score = sum((bonus_manifest, bonus_docs, bonus_variants, bonus_tests, bonus_detail))
    total_score = must_score + bonus_score

    must_pass = all((m1, m2, m3, m4, m5))
    port = detect_port(pr, title)

    summary_row = (
        f"| [#{number}]({url}) | {port} | {title} | "
        f"{'Y' if m1 else 'N'} | {'Y' if m2 else 'N'} | {'Y' if m3 else 'N'} | "
        f"{'Y' if m4 else 'N'} | {'Y' if m5 else 'N'} | {'Yes' if must_pass else 'No'} | {total_score} |"
    )

    missing = []
    if not m1:
        missing.append("board.json")
    if not m2:
        missing.append("mpconfigboard.h/mpconfigboard.cmake|mk")
    if not m3:
        missing.append("pins.csv")
    if not m4:
        missing.append("testing evidence in PR body")
    if not m5:
        missing.append("board-path file changes")

    strengths = []
    if bonus_manifest:
        strengths.append("manifest.py included")
    if bonus_docs:
        strengths.append("board docs included")
    if bonus_variants:
        strengths.append("variant configs included")
    if bonus_tests:
        strengths.append("tests added under tests/ports")
    if bonus_detail:
        strengths.append("detailed PR description")

    key_files = summarize_key_files(filenames)
    body_summary = extract_body_summary(body)
    board_scope = ", ".join(board_dirs[:3]) if board_dirs else "no board directory detected from patch"
    if len(board_dirs) > 3:
        board_scope += f", and {len(board_dirs) - 3} more"

    note = f"### [#{number}]({url}) - {title}\n\n"
    note += f"Scope: {board_scope}."
    if key_files:
        note += f" Key files detected: {key_files}."
    if body_summary:
        note += f" PR summary: {body_summary}."
    if must_pass:
        note += " This PR currently meets the minimum MUST criteria."
    else:
        note += " This PR does not yet meet the minimum MUST criteria."
    if missing:
        note += f" Key gaps: {', '.join(missing)}."
    if strengths:
        note += f" Notable strengths: {', '.join(strengths)}."

    return summary_row, note


def main() -> None:
    report_path = Path("OPEN_BOARD_PR_BEST_PRACTICES_ASSESSMENT.md")
    prs = iter_open_board_prs()

    rows = []
    notes = []
    for pr in prs:
        row, note = score_pr(pr)
        rows.append(row)
        notes.append(note)

    lines = [
        "# Open Board PR Assessment Against Best Practices",
        "",
        "Generated from currently open PRs labeled `board-definition` in `micropython/micropython`.",
        "",
        "Scoring model:",
        "- MUST score: 5 checks (M1-M5), each 2 points, total 10",
        "- Best-practice bonus: 5 checks, each 1 point, total 5",
        "- Total: /15",
        "",
        "**MUST criteria (M1–M5):**",
        "",
        "| | Criterion | Description |",
        "|---|---|---|",
        "| M1 | `board.json` | Board metadata file present with name, id, vendor, and machine fields |",
        "| M2 | Config files | Both `mpconfigboard.h` and `mpconfigboard.cmake` (or `.mk`) present |",
        "| M3 | `pins.csv` | Pin mapping file present (where applicable to the port) |",
        "| M4 | Testing evidence | PR description includes hardware test results or flash/run evidence |",
        "| M5 | Correct directory | Board files placed under the correct `ports/<port>/boards/<BOARD_NAME>/` path |",
        "",
        "## Summary Table",
        "",
        "| PR | Port | Board/Title | M1 | M2 | M3 | M4 | M5 | MUST Pass | Score (/15) |",
        "|---|---|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        "## Per-PR Notes",
        "",
    ]

    for note in notes:
        lines.append(note)
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"ASSESSED={len(prs)}")


if __name__ == "__main__":
    main()