#!/usr/bin/env python3
"""comment.py - implementation for the add-status-comment composite action.

Called by action.yml; relies on environment variables set there.
"""

from __future__ import annotations

import json
import os
import subprocess
from typing import Any


def error_and_exit(message: str) -> None:
    """Emit a GitHub Actions error annotation and exit with failure."""
    print(f"::error::add-status-comment: {message}")
    raise SystemExit(1)


def run_gh_json(args: list[str], stdin_payload: dict[str, Any] | None = None) -> Any:
    """Run `gh api` and parse the JSON response, raising on non-zero exit."""
    cmd = ["gh", "api", *args]
    stdin = None
    if stdin_payload is not None:
        stdin = json.dumps(stdin_payload)

    result = subprocess.run(
        cmd,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(stderr if stderr else "gh api call failed")

    output = result.stdout.strip()
    if not output:
        return None
    return json.loads(output)


def run_gh_graphql(query: str) -> bool:
    """Run a GraphQL query via `gh api` and return whether it succeeded."""
    result = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={query}"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def load_pr_number(event_path: str) -> str:
    """Extract the pull request number from the GitHub event payload."""
    try:
        with open(event_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        error_and_exit("could not determine PR number from event payload.")

    pr_number = None
    pr = payload.get("pull_request")
    if isinstance(pr, dict):
        pr_number = pr.get("number")
    if pr_number is None:
        pr_number = payload.get("number")

    if pr_number in (None, "", "null"):
        error_and_exit("could not determine PR number from event payload.")

    return str(pr_number)


def find_existing_comment(owner: str, repo: str, pr_number: str, marker: str) -> dict[str, Any] | None:
    """Find the first bot-authored PR comment that starts with the marker."""
    pages = run_gh_json(
        [
            f"/repos/{owner}/{repo}/issues/{pr_number}/comments",
            "--paginate",
        ]
    )

    comments: list[dict[str, Any]] = []
    if isinstance(pages, list):
        if pages and isinstance(pages[0], list):
            for page in pages:
                if isinstance(page, list):
                    comments.extend(c for c in page if isinstance(c, dict))
        else:
            comments = [c for c in pages if isinstance(c, dict)]

    for comment in comments:
        user = comment.get("user")
        body = comment.get("body")
        if (
            isinstance(user, dict)
            and user.get("login") == "github-actions[bot]"
            and isinstance(body, str)
            and body.startswith(marker)
        ):
            return comment

    return None


def main() -> int:
    """Execute the PR status comment workflow logic using environment inputs."""
    status_input = os.environ.get("INPUT_STATUS", "")
    status_lower = status_input.lower()
    if status_lower not in {"error", "passed"}:
        error_and_exit(f"invalid status '{status_input}'. Must be 'error' or 'passed'.")

    category = os.environ.get("INPUT_CATEGORY", "")
    if not category:
        category = os.environ.get("_WORKFLOW_NAME", "")
    if not category:
        error_and_exit(
            "could not determine category (INPUT_CATEGORY and GITHUB_WORKFLOW are both empty)."
        )

    event_name = os.environ.get("_EVENT_NAME") or os.environ.get("GITHUB_EVENT_NAME", "")
    if event_name not in {"pull_request", "pull_request_target"}:
        error_and_exit(
            "this action only works on pull_request or pull_request_target events "
            f"(got: '{event_name}')."
        )

    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    pr_number = load_pr_number(event_path)

    repo_full = os.environ.get("_REPO", "")
    if "/" not in repo_full:
        error_and_exit("could not determine repository owner/name from github.repository.")
    owner, repo = repo_full.split("/", 1)

    print(f"add-status-comment: PR=#{pr_number}  category='{category}'  status='{status_lower}'")

    marker = f"<!-- add-status-comment:{category} -->"
    comment = find_existing_comment(owner, repo, pr_number, marker)

    comment_id = ""
    comment_node_id = ""
    if comment:
        comment_id = str(comment.get("id", ""))
        comment_node_id = str(comment.get("node_id", ""))
        print(f"add-status-comment: found existing comment id={comment_id}")
    else:
        print(f"add-status-comment: no existing comment found for category '{category}'")

    if status_lower == "error":
        status_emoji = "❌"
        status_label = "Error"
    elif status_lower == "passed":
        status_emoji = "✅"
        status_label = "Passed"
    else:
        status_emoji = "ℹ️"
        status_label = "Info"

    body = f"{marker}\n### {status_emoji} {category}: {status_label}"
    description = os.environ.get("INPUT_DESCRIPTION", "")
    if description:
        body = f"{body}\n\n{description}"

    if status_lower == "error":
        if not comment_id:
            print("add-status-comment: creating new comment...")
            response = run_gh_json(
                [f"/repos/{owner}/{repo}/issues/{pr_number}/comments", "-X", "POST", "--input", "-"],
                stdin_payload={"body": body},
            )
            if isinstance(response, dict):
                comment_node_id = str(response.get("node_id", ""))
            print(f"add-status-comment: created comment, node_id={comment_node_id}")
        else:
            print(f"add-status-comment: updating comment id={comment_id}...")
            run_gh_json(
                [f"/repos/{owner}/{repo}/issues/comments/{comment_id}", "-X", "PATCH", "--input", "-"],
                stdin_payload={"body": body},
            )
            print("add-status-comment: unminimizing comment...")
            gql_unminimize = (
                "mutation {"
                f" unminimizeComment(input: {{subjectId: \"{comment_node_id}\"}}) {{"
                "   unminimizedComment { isMinimized }"
                " }"
                "}"
            )
            if not run_gh_graphql(gql_unminimize):
                print(
                    "::warning::add-status-comment: unminimizeComment GraphQL call failed "
                    "(non-fatal)."
                )

    elif status_lower == "passed":
        if comment_id:
            print(f"add-status-comment: updating comment id={comment_id} with passed status...")
            run_gh_json(
                [f"/repos/{owner}/{repo}/issues/comments/{comment_id}", "-X", "PATCH", "--input", "-"],
                stdin_payload={"body": body},
            )
            print("add-status-comment: minimizing comment...")
            gql_minimize = (
                "mutation {"
                f" minimizeComment(input: {{subjectId: \"{comment_node_id}\", classifier: RESOLVED}}) {{"
                "   minimizedComment { isMinimized }"
                " }"
                "}"
            )
            if not run_gh_graphql(gql_minimize):
                print(
                    "::warning::add-status-comment: minimizeComment GraphQL call failed "
                    "(non-fatal)."
                )
        else:
            print("add-status-comment: no existing comment and status is 'passed' - nothing to do.")

    print("add-status-comment: done.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        error_and_exit(str(exc))
