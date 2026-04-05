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

PULLS_API_URL = "https://api.github.com/repos/micropython/micropython/pulls/{number}"


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


def fetch_pull(number: int) -> dict:
    return fetch_json(PULLS_API_URL.format(number=number))


def is_draft_pr(pr: dict) -> bool:
    number = pr.get("number")
    if not number:
        return False
    data = fetch_pull(number)
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


def extract_variant_names(filenames: list[str]) -> list[str]:
    variant_names = set()
    for name in filenames:
        match = re.match(
            r"^ports/[^/]+/boards/[^/]+/mpconfigvariant(?:_([^/.]+))?\.(?:cmake|mk)$",
            name,
        )
        if match:
            variant_names.add(match.group(1) or "default")
    return sorted(variant_names)


def summarize_cli_targets(prs: list[dict]) -> str:
    board_names = set()
    variant_names = set()

    for pr in prs:
        if pr.get("_local"):
            filenames = pr.get("_filenames", [])
        else:
            patch_text = fetch_text(pr["pull_request"]["patch_url"])
            filenames = extract_filenames_from_patch(patch_text)

        for board_dir in extract_board_dirs(filenames):
            board_names.add(Path(board_dir).name)
        for variant_name in extract_variant_names(filenames):
            variant_names.add(variant_name)

    board_text = ",".join(sorted(board_names)) if board_names else "none-detected"
    variant_text = ",".join(sorted(variant_names)) if variant_names else "none"
    return f"Boards: {board_text}\nVariants: {variant_text}"


def detect_primary_board_name(pr: dict) -> str:
    if pr.get("_local"):
        filenames = pr.get("_filenames", [])
    else:
        patch_text = fetch_text(pr["pull_request"]["patch_url"])
        filenames = extract_filenames_from_patch(patch_text)

    board_dirs = extract_board_dirs(filenames)
    if not board_dirs:
        return "current_board_pr"
    return Path(board_dirs[0]).name


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


def has_pr_testing_evidence(body: str, filenames: list[str]) -> bool:
    has_test_files = any(re.match(r"^tests/ports/[^/]+/", name) for name in filenames)
    return has_testing_section(body) or has_test_files


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


def build_current_checkout_pr(base_ref: str) -> dict:
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    head_sha = run_git(["rev-parse", "HEAD"])
    patch_text = run_git(["diff", "--no-color", f"{base_ref}...HEAD"])
    filenames_text = run_git(["diff", "--name-only", f"{base_ref}...HEAD"])
    filenames = [line for line in filenames_text.splitlines() if line.strip()]

    matched_pr = None
    for pr in iter_open_board_prs():
        pull = fetch_pull(pr["number"])
        if pull.get("head", {}).get("sha") == head_sha:
            matched_pr = pull
            break

    if matched_pr:
        title = matched_pr.get("title") or f"local checkout: {branch}"
        body = matched_pr.get("body") or ""
        html_url = matched_pr.get("html_url", "")
        labels = matched_pr.get("labels", [])
        number = matched_pr.get("number", 0)
    else:
        title = run_git(["log", "--format=%s", "-n", "1", f"{base_ref}..HEAD"]) or f"local checkout: {branch}"
        body = ""
        html_url = ""
        labels = []
        number = 0

    return {
        "number": number,
        "title": title,
        "html_url": html_url,
        "body": body,
        "labels": labels,
        "_local": True,
        "_branch": branch,
        "_patch_text": patch_text,
        "_filenames": filenames,
        "_matched_pr": bool(matched_pr),
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
    has_testing = has_pr_testing_evidence(body, filenames)

    m1 = has_board_json
    m2 = has_mp_h and has_mp_cfg
    m3 = has_pins
    m4 = has_testing
    m5 = has_board_path
    must_score = 2 * sum((m1, m2, m3, m4, m5))

    best_practice_manifest = any(re.match(r"^ports/[^/]+/boards/[^/]+/manifest\.py$", name) for name in filenames)
    best_practice_docs = any(re.match(r"^ports/[^/]+/boards/[^/]+/(board\.md|README\.md)$", name) for name in filenames)
    best_practice_variants = any(re.match(r"^ports/[^/]+/boards/[^/]+/mpconfigvariant.*\.(cmake|mk)$", name) for name in filenames)
    best_practice_tests = any(re.match(r"^tests/ports/[^/]+/", name) for name in filenames)
    best_practice_detail = len(body) > 700
    best_practice_variant_discoverability = (not best_practice_variants) or patch_has_board_json_variants(patch_text)
    best_practice_variant_pin_rule = (not best_practice_variants) or (not patch_has_variant_specific_pins(filenames))
    best_practice_workflow_evidence = has_build_workflow_evidence(body)
    best_practice_score = sum(
        (
            best_practice_manifest,
            best_practice_docs,
            best_practice_variants,
            best_practice_tests,
            best_practice_detail,
            best_practice_variant_discoverability,
            best_practice_variant_pin_rule,
            best_practice_workflow_evidence,
        )
    )
    total_score = must_score + best_practice_score

    must_pass = all((m1, m2, m3, m4, m5))
    port = detect_port(pr, title)
    if port == "unknown":
        port = detect_port_from_filenames(filenames)

    pr_ref = format_pr_ref(pr)
    summary_row = (
        f"| {pr_ref} | {port} | {title} | "
        f"{'Y' if m1 else 'N'} | {'Y' if m2 else 'N'} | {'Y' if m3 else 'N'} | "
        f"{'Y' if m4 else 'N'} | {'Y' if m5 else 'N'} | {'Yes' if must_pass else 'No'} | {best_practice_score} | {total_score} |"
    )

    missing = []
    if not m1:
        missing.append("board.json")
    if not m2:
        missing.append("mpconfigboard.h/mpconfigboard.cmake|mk")
    if not m3:
        missing.append("pins.csv")
    if not m4:
        missing.append("testing evidence in PR body or tests/ports files in PR")
    if not m5:
        missing.append("board-path file changes")
    if best_practice_variants and not best_practice_variant_discoverability:
        missing.append("board.json variants metadata for variant builds")
    if best_practice_variants and not best_practice_variant_pin_rule:
        missing.append("variant pin-layout rule (pins should not vary by variant)")

    strengths = []
    if best_practice_manifest:
        strengths.append("manifest.py included")
    if best_practice_docs:
        strengths.append("board docs included")
    if best_practice_variants:
        strengths.append("variant configs included")
    if best_practice_tests:
        strengths.append("tests added under tests/ports")
    if best_practice_detail:
        strengths.append("detailed PR description")
    if best_practice_variant_discoverability and best_practice_variants:
        strengths.append("variants appear discoverable in board.json")
    if best_practice_variant_pin_rule and best_practice_variants:
        strengths.append("variant pin-layout rule respected")
    if best_practice_workflow_evidence:
        strengths.append("best-practice build workflow evidence present")

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
    if pr.get("_local") and not pr.get("_matched_pr"):
        note += " No matching open board PR was detected for this checkout, so PR-body testing evidence could not be confirmed."
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
        default="current",
        help="Scoring mode: 'current' for local checkout branch (default), 'open' for all open non-draft board PRs.",
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
        prs = [build_current_checkout_pr(args.base_ref)]
        default_output = f"{detect_primary_board_name(prs[0])}_report.md"
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
        "- Best-practice score: 8 checks, each 1 point, total 8",
        "- Total: /18",
        "",
        "**MUST criteria (M1–M5):**",
        "",
        "| | Criterion | Description |",
        "|---|---|---|",
        "| M1 | `board.json` | Board metadata file present with name, id, vendor, and machine fields |",
        "| M2 | Config files | Both `mpconfigboard.h` and `mpconfigboard.cmake` (or `.mk`) present |",
        "| M3 | `pins.csv` | Pin mapping file present (where applicable to the port) |",
        "| M4 | Testing evidence | PR includes testing details in the PR body or adds tests under tests/ports |",
        "| M5 | Correct directory | Board files placed under the correct `ports/<port>/boards/<BOARD_NAME>/` path |",
        "",
        "**Additional Best-Practice Criteria (W1-W3):**",
        "",
        "| | Criterion | Description |",
        "|---|---|---|",
        "| W1 | Variant discoverability | If variant config files exist, board.json includes a variants map |",
        "| W2 | Variant pin rule | Variant builds keep one pins.csv layout (pin changes imply a new board) |",
        "| W3 | Build workflow evidence | PR body includes best-practice workflow evidence (submodules, BOARD_VARIANT, or test_full) |",
        "",
        "## Summary Table",
        "",
        "| PR | Port | Board/Title | M1 | M2 | M3 | M4 | M5 | MUST Pass | Best Practice (/8) | Score (/18) |",
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
    target_summary = summarize_cli_targets(prs)
    print(
        f"Assessed {len(prs)}\n{target_summary}\nCreated: {report_path}"
    )


if __name__ == "__main__":
    main()