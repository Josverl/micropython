#!/usr/bin/env python3
"""
Fetch commits and PRs from MicroPython repository by key contributors.

Retrieves ~100 commits/PRs from specified authors and stores their diffs,
metadata, and commit messages for analysis.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from diskcache import Cache
from github import Github
from github.GithubException import GithubException


# Target contributors for analysis (resolve GitHub handles automatically)
TARGET_CONTRIBUTORS = [
    {"name": "Damien George", "email": "damien@micropython.org", "handle": "dpgeorge"},
    {"name": "Jeff Epler", "email": "jepler@unpythonic.net", "handle": "jepler"},
    {
        "name": "Andrew Leech",
        "email": "andrew.leech@planetinnovation.com.au",
        "handle": "pi-anl",
    },
    {"name": "Alessandro Gatti", "email": "a.gatti@frob.it", "handle": "agatti"},
    {"name": "Angus Gratton", "email": "angus@redyak.com.au", "handle": "projectgus"},
    {"name": "robert-hh", "email": "robert@hammelrath.com"},
    {"name": "Daniël van de Giessen", "email": "daniel@dvdgiessen.nl"},
    {"name": "Yuuki NAGAO", "email": "wf.yn386@gmail.com"},
    {"name": "Chris Webb", "email": "chris@arachsys.com"},
]

# Repository details
REPO_OWNER = "micropython"
REPO_NAME = "micropython"
REPO_PATH = f"{REPO_OWNER}/{REPO_NAME}"

# Configuration
MAX_COMMITS_PER_AUTHOR = 80  # 4x previous limit
MAX_PRS_PER_AUTHOR = 40  # 4x previous limit
LOOK_BACK_DAYS = 1460  # ~4 years
OUTPUT_DIR = Path(__file__).parent / "data"
SKIP_PRS_IF_NO_TOKEN = True
CACHE_DIR = OUTPUT_DIR / "cache"


class CommitFetcher:
    """Fetches and stores commits from MicroPython repository."""

    def __init__(self, github_token=None):
        """Initialize with optional GitHub token for higher rate limits."""
        if github_token:
            self.github = Github(github_token)
        else:
            self.github = Github()
        self.github_token = github_token
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limited = False
        self.cache = Cache(str(CACHE_DIR))
        if not self._rate_limit_ok() and not self.github_token:
            raise RuntimeError("GitHub API rate limit exceeded. Set GITHUB_TOKEN and retry.")
        self.repo = self.github.get_repo(REPO_PATH)

    def fetch_commits_by_author(self, author, max_commits=MAX_COMMITS_PER_AUTHOR):
        """Fetch commits from a specific author."""
        print(f"Fetching commits from author: {author}")
        commits = []

        try:
            since = datetime.now() - timedelta(days=LOOK_BACK_DAYS)
            query_commits = self.repo.get_commits(author=author, since=since)

            for i, commit in enumerate(query_commits):
                if i >= max_commits:
                    break
                commits.append(self._cached_commit_to_dict(commit.sha))
                print(f"  - {commit.sha[:8]}: {commit.commit.message.split(chr(10))[0]}")

        except GithubException as e:
            print(f"  Error fetching commits: {e}")

        return commits

    def fetch_commits_by_identity(self, contributor, max_commits=MAX_COMMITS_PER_AUTHOR):
        """Fetch commits using resolved handle or fallback to commit search."""
        handle = contributor.get("handle")
        if handle:
            return self.fetch_commits_by_author(handle, max_commits)

        print("  No GitHub handle resolved; falling back to commit search by email/name.")
        return self.fetch_commits_by_search(contributor, max_commits)

    def fetch_commits_by_search(self, contributor, max_commits=MAX_COMMITS_PER_AUTHOR):
        """Fetch commits by searching commits with email/name, then loading full commit data."""
        commits = []
        seen = set()
        queries = [
            f'repo:{REPO_PATH} author-email:"{contributor["email"]}"',
            f'repo:{REPO_PATH} author-name:"{contributor["name"]}"',
        ]

        for query in queries:
            try:
                search_results = self._cached_search_commits(query)
                for commit in search_results:
                    if commit.sha in seen:
                        continue
                    seen.add(commit.sha)
                    commits.append(self._cached_commit_to_dict(commit.sha))
                    if len(commits) >= max_commits:
                        return commits
            except GithubException as e:
                print(f"  Error searching commits for {contributor['name']}: {e}")

        return commits

    def fetch_pull_requests_by_author(self, author, max_prs=MAX_PRS_PER_AUTHOR):
        """Fetch PRs authored by a specific author."""
        print(f"Fetching PRs from author: {author}")
        prs = []

        if self.rate_limited:
            print("  Skipping PR fetch (rate limit previously hit).")
            return prs

        if SKIP_PRS_IF_NO_TOKEN and not self.github_token:
            print("  Skipping PR fetch (no GitHub token provided).")
            return prs

        if not self._rate_limit_ok():
            print("  Skipping PR fetch (rate limit too low).")
            self.rate_limited = True
            return prs

        try:
            query = f"repo:{REPO_PATH} author:{author} type:pr"
            search_results = self.github.search_issues(query, sort="updated", order="desc")

            for issue in search_results:
                if len(prs) >= max_prs:
                    break
                try:
                    pr_data = self._cached_pull(issue.number)
                except GithubException as e:
                    if self._is_rate_limited_error(e):
                        print("  Warning: Rate limit hit while fetching PRs; stopping PR fetch.")
                        self.rate_limited = True
                        break
                    print(f"  Warning: Could not load PR #{issue.number}: {e}")
                    continue
                prs.append(pr_data)
                print(f"  - #{pr_data['number']}: {pr_data['title']}")

        except GithubException as e:
            print(f"  Error fetching PRs: {e}")

        return prs

    def _commit_to_dict(self, commit):
        """Convert a commit to a dictionary with metadata and diff."""
        commit_data = {
            "sha": commit.sha,
            "author": commit.commit.author.name,
            "author_email": commit.commit.author.email,
            "date": commit.commit.author.date.isoformat(),
            "message": commit.commit.message,
            "files_changed": len(commit.files),
            "additions": sum(f.additions for f in commit.files),
            "deletions": sum(f.deletions for f in commit.files),
            "files": [],
        }

        # Extract file-level diff information
        for file in commit.files:
            file_data = {
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "patch": file.patch or "",
            }
            commit_data["files"].append(file_data)

        return commit_data

    def _pr_to_dict(self, pr):
        """Convert a PR to a dictionary with metadata and diff."""
        pr_data = {
            "number": pr.number,
            "title": pr.title,
            "body": pr.body or "",
            "author": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "merged": pr.merged,
            "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
            "additions": pr.additions,
            "deletions": pr.deletions,
            "changed_files": pr.changed_files,
            "files": [],
        }

        # Fetch file-level changes
        try:
            for file in pr.get_files():
                file_data = {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch or "",
                }
                pr_data["files"].append(file_data)
        except GithubException as e:
            print(f"  Warning: Could not fetch files for PR #{pr.number}: {e}")

        return pr_data

    def fetch_all(self):
        """Fetch commits and PRs from all target authors."""
        all_data = {
            "metadata": {
                "repository": REPO_PATH,
                "fetched_at": datetime.now().isoformat(),
                "look_back_days": LOOK_BACK_DAYS,
                "max_commits_per_author": MAX_COMMITS_PER_AUTHOR,
            },
            "commits": {},
            "pull_requests": {},
            "contributors": [],
        }

        resolved = self.resolve_contributors(TARGET_CONTRIBUTORS)
        all_data["contributors"] = resolved

        for contributor in resolved:
            label = contributor.get("handle") or contributor["email"]
            print(f"\n{'=' * 60}")
            print(f"Processing contributor: {contributor['name']} ({label})")
            print(f"{'=' * 60}")

            # Fetch commits
            commits = self.fetch_commits_by_identity(contributor, MAX_COMMITS_PER_AUTHOR)
            all_data["commits"][label] = commits

            # Fetch PRs (requires GitHub handle)
            if contributor.get("handle"):
                prs = self.fetch_pull_requests_by_author(
                    contributor["handle"], max_prs=MAX_PRS_PER_AUTHOR
                )
            else:
                prs = []
                print("  Skipping PR fetch (no GitHub handle resolved).")
            all_data["pull_requests"][label] = prs

        return all_data

    def save_data(self, data, filename="micropython_analysis_data.json"):
        """Save fetched data to JSON file."""
        output_path = self.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nData saved to: {output_path}")
        print(f"Total commits: {sum(len(c) for c in data['commits'].values())}")
        print(f"Total PRs: {sum(len(p) for p in data['pull_requests'].values())}")
        return output_path

    def _cached_commit_to_dict(self, sha):
        """Get commit dict from cache or GitHub API."""
        key = f"commit:{sha}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        commit = self.repo.get_commit(sha)
        data = self._commit_to_dict(commit)
        self.cache.set(key, data)
        return data

    def _cached_pull(self, number):
        """Get pull request data from cache or GitHub API."""
        key = f"pull:{number}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        pr = self.repo.get_pull(number)
        data = self._pr_to_dict(pr)
        self.cache.set(key, data)
        return data

    def _cached_search_commits(self, query):
        """Get commit search results from cache or GitHub API."""
        key = f"search_commits:{query}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        results = list(self.github.search_commits(query))
        self.cache.set(key, results)
        return results

    def _rate_limit_ok(self):
        """Check if GitHub API rate limit allows more requests."""
        try:
            rate = self.github.get_rate_limit()
            core_remaining = rate.core.remaining
            search_remaining = rate.search.remaining
            if core_remaining <= 0 or search_remaining <= 0:
                return False
        except GithubException:
            return True
        return True

    def _is_rate_limited_error(self, error):
        """Check if a GithubException indicates rate limiting."""
        return getattr(error, "status", None) == 403 and "rate limit" in str(error).lower()

    def resolve_contributors(self, contributors):
        """Resolve GitHub handles for contributors using commit search."""
        resolved = []
        for contributor in contributors:
            handle = contributor.get("handle") or self.resolve_github_handle(contributor)
            resolved.append({**contributor, "handle": handle})
        return resolved

    def resolve_github_handle(self, contributor):
        """Resolve a contributor's GitHub handle using commit search by email/name."""
        queries = [
            f'repo:{REPO_PATH} author-email:"{contributor["email"]}"',
            f'repo:{REPO_PATH} author-name:"{contributor["name"]}"',
        ]

        for query in queries:
            try:
                search_results = self.github.search_commits(query)
                for commit in search_results:
                    if commit.author and commit.author.login:
                        print(f"Resolved {contributor['name']} -> {commit.author.login}")
                        return commit.author.login
                    break
            except GithubException as e:
                print(f"  Warning: Could not resolve {contributor['name']} handle: {e}")

        print(f"  Warning: No GitHub handle found for {contributor['name']}")
        return None


def main():
    """Main entry point."""
    import sys

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("WARNING: No GITHUB_TOKEN environment variable set.")
        print("         Using unauthenticated requests (lower rate limit).")
        print("         Set GITHUB_TOKEN to avoid rate limiting.\n")

    fetcher = CommitFetcher(github_token=github_token)
    data = fetcher.fetch_all()
    output_path = fetcher.save_data(data)

    return output_path


if __name__ == "__main__":
    main()
