#!/usr/bin/env python3

import argparse
import json
import re
import socket
import subprocess
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


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


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


def is_draft_pr(pr: dict) -> bool:
    pull_meta_url = pr.get("pull_request", {}).get("url")
    if not pull_meta_url:
        return False
    data = fetch_json(pull_meta_url)
    return bool(data.get("draft", False))


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
        if is_draft_pr(item):
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


def detect_port_from_filenames(filenames: list[str]) -> str:
    for name in filenames:
        match = re.match(r"^ports/([^/]+)/boards/[^/]+/", name)
        if match:
            return match.group(1)
    return "unknown"


def has_testing_section(body: str) -> bool:
    return bool(
        re.search(r"(^|\n)\s*#{1,3}\s*Testing\b", body, flags=re.IGNORECASE)
        or re.search(r"\bmake\s+BOARD=", body)
    )


def patch_has_board_json_variants(patch_text: str) -> bool:
    return bool(re.search(r'^\+\s*"variants"\s*:', patch_text, flags=re.MULTILINE))


def patch_has_variant_specific_pins(filenames: list[str]) -> bool:
    return any(
        re.match(r"^ports/[^/]+/boards/[^/]+/pins[^/]*\.csv$", name) and not name.endswith("/pins.csv")
        for name in filenames
    )


def has_build_workflow_evidence(body: str) -> bool:
    return bool(
        re.search(r"\bmake\s+submodules\b", body)
        or re.search(r"\bmake\s+test_full\b", body)
        or re.search(r"\bBOARD_VARIANT=", body)
    )


def has_signoff_evidence(body: str, patch_text: str) -> bool:
    return bool(
        re.search(r"\bSigned-off-by:\b", body, flags=re.IGNORECASE)
        or re.search(r"\bSigned-off-by:\b", patch_text, flags=re.IGNORECASE)
    )


def build_current_checkout_pr(base_ref: str) -> dict:
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    patch_text = run_git(["diff", "--no-color", f"{base_ref}...HEAD"])
    filenames_text = run_git(["diff", "--name-only", f"{base_ref}...HEAD"])
    filenames = [line for line in filenames_text.splitlines() if line.strip()]

    # Prefer a concise summary from commits on the branch, fallback to branch name.
    title = run_git(["log", "--format=%s", "-n", "1", f"{base_ref}..HEAD"]) or f"local checkout: {branch}"
    body = run_git(["log", "--format=%B", f"{base_ref}..HEAD"])

    return {
        "number": 0,
        "title": title,
        "html_url": "",
        "body": body,
        "labels": [],
        "_local": True,
        "_branch": branch,
        "_patch_text": patch_text,
        "_filenames": filenames,
    }


def format_pr_ref(pr: dict) -> str:
    number = pr.get("number", 0)
    url = pr.get("html_url", "")
    if number and url:
        return f"[#{number}]({url})"
    return "LOCAL"


def score_pr(pr: dict) -> tuple[str, str]:
    number = pr["number"]
    title = (pr.get("title") or "").replace("|", "\\|")
    url = pr.get("html_url", "")
    body = pr.get("body") or ""
    if pr.get("_local"):
        patch_text = pr.get("_patch_text", "")
        filenames = pr.get("_filenames", [])
    else:
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

    wiki_variant_discoverability = (not bonus_variants) or patch_has_board_json_variants(patch_text)
    wiki_variant_pin_rule = (not bonus_variants) or (not patch_has_variant_specific_pins(filenames))
    wiki_workflow_evidence = has_build_workflow_evidence(body)
    wiki_signoff_evidence = has_signoff_evidence(body, patch_text)
    wiki_score = sum(
        (
            wiki_variant_discoverability,
            wiki_variant_pin_rule,
            wiki_workflow_evidence,
            wiki_signoff_evidence,
        )
    )
    total_score = must_score + bonus_score + wiki_score

    must_pass = all((m1, m2, m3, m4, m5))
    port = detect_port(pr, title)
    if port == "unknown":
        port = detect_port_from_filenames(filenames)

    pr_ref = format_pr_ref(pr)
    summary_row = (
        f"| {pr_ref} | {port} | {title} | "
        f"{'Y' if m1 else 'N'} | {'Y' if m2 else 'N'} | {'Y' if m3 else 'N'} | "
        f"{'Y' if m4 else 'N'} | {'Y' if m5 else 'N'} | {'Yes' if must_pass else 'No'} | {wiki_score} | {total_score} |"
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
    if bonus_variants and not wiki_variant_discoverability:
        missing.append("board.json variants metadata for variant builds")
    if bonus_variants and not wiki_variant_pin_rule:
        missing.append("variant pin-layout rule (pins should not vary by variant)")

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
    if wiki_variant_discoverability and bonus_variants:
        strengths.append("variants appear discoverable in board.json")
    if wiki_variant_pin_rule and bonus_variants:
        strengths.append("variant pin-layout rule respected")
    if wiki_workflow_evidence:
        strengths.append("wiki build workflow evidence present")
    if wiki_signoff_evidence:
        strengths.append("sign-off evidence detected")

    key_files = summarize_key_files(filenames)
    body_summary = extract_body_summary(body)
    board_scope = ", ".join(board_dirs[:3]) if board_dirs else "no board directory detected from patch"
    if len(board_dirs) > 3:
        board_scope += f", and {len(board_dirs) - 3} more"

    if number and url:
        note = f"### [#{number}]({url}) - {title}\n\n"
    else:
        branch = pr.get("_branch", "current branch")
        note = f"### LOCAL ({branch}) - {title}\n\n"
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
    parser = argparse.ArgumentParser(
        description=(
            "Score board-definition PRs against best-practice criteria. "
            "Modes: open (all open, non-draft labeled PRs) or current (currently checked-out branch)."
        )
    )
    parser.add_argument(
        "--mode",
        choices=("open", "current"),
        default="open",
        help="Scoring mode: 'open' for all open non-draft board PRs, 'current' for local checkout branch.",
    )
    parser.add_argument(
        "--base-ref",
        default="master",
        help="Git base ref used by --mode current (default: master).",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output markdown path. Defaults depend on mode.",
    )
    args = parser.parse_args()

    if args.mode == "current":
        default_output = "CURRENT_BOARD_PR_BEST_PRACTICES_ASSESSMENT.md"
        prs = [build_current_checkout_pr(args.base_ref)]
        generated_from = (
            "Generated from the currently checked-out branch relative to "
            f"`{args.base_ref}`."
        )
    else:
        default_output = "OPEN_BOARD_PR_BEST_PRACTICES_ASSESSMENT.md"
        prs = iter_open_board_prs()
        generated_from = (
            "Generated from currently open non-draft PRs labeled "
            "`board-definition` in `micropython/micropython`."
        )

    report_path = Path(args.output or default_output)

    rows = []
    notes = []
    for pr in prs:
        row, note = score_pr(pr)
        rows.append(row)
        notes.append(note)

    lines = [
        "# Open Board PR Assessment Against Best Practices",
        "",
        generated_from,
        "",
        "Scoring model:",
        "- MUST score: 5 checks (M1-M5), each 2 points, total 10",
        "- Best-practice bonus: 5 checks, each 1 point, total 5",
        "- Wiki-aligned bonus: 4 checks, each 1 point, total 4",
        "- Total: /19",
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
        "**Wiki-aligned bonus criteria (W1-W4):**",
        "",
        "| | Criterion | Description |",
        "|---|---|---|",
        "| W1 | Variant discoverability | If variant config files exist, board.json includes a variants map |",
        "| W2 | Variant pin rule | Variant builds keep one pins.csv layout (pin changes imply a new board) |",
        "| W3 | Build workflow evidence | PR body includes wiki-style workflow evidence (submodules, BOARD_VARIANT, or test_full) |",
        "| W4 | Sign-off evidence | Signed-off-by evidence found in PR body or patch metadata |",
        "",
        "## Summary Table",
        "",
        "| PR | Port | Board/Title | M1 | M2 | M3 | M4 | M5 | MUST Pass | Wiki (/4) | Score (/19) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        "## Per-PR Notes",
        "",
    ]

    for note in notes:
        lines.append(note)
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"MODE={args.mode} ASSESSED={len(prs)} OUTPUT={report_path}")


if __name__ == "__main__":
    main()