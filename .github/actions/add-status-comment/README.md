# PR Status Comment Action

A reusable composite GitHub Action that maintains **exactly one PR conversation
comment per category** across multiple workflow runs.  
On failure the comment is created (or updated) and made visible; on success it
is updated and minimized (collapsed) so the PR conversation stays clean.

---

## Features

| Capability | Details |
|---|---|
| One comment per category | A hidden `<!-- add-status-comment:{category} -->` marker identifies the comment |
| Create **or** update | `status: error` → create if absent, update if present |
| Pass-only update | `status: passed` → update existing comment; never creates a new one |
| Minimize / unminimize | `passed` collapses the comment (`RESOLVED`); `error` reopens it |
| Default category | Falls back to `github.workflow` when `category` is not supplied |
| Any token | Accepts a custom `token` input; defaults to the job's `GITHUB_TOKEN` |

---

## Required Permissions

The **calling job** must declare (at minimum):

```yaml
permissions:
  issues: write        # create/update issue comments (PRs are issues)
  pull-requests: write # required for GraphQL minimize/unminimize mutations
```

---

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `status` | ✅ | — | `"info"` , `"error"` or `"passed"` (case-insensitive) |
| `category` | ❌ | `github.workflow` | Label used to find/manage the single comment for this context |
| `description` | ❌ | `""` | Optional markdown appended to the comment after the status heading |
| `token` | ❌ | `github.token` | GitHub token; must have the permissions listed above |

---

## Usage Examples

### 1. Create/update on failure, update+minimize on success

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        id: tests
        run: make test

      - name: Report failure
        if: failure()
        uses: ./.github/actions/add-status-comment
        with:
          status: error
          description: |
            Tests failed. See the [workflow run](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}) for details.

      - name: Report success
        if: success()
        uses: ./.github/actions/add-status-comment
        with:
          status: passed
          description: All tests passed. ✔
```

### 2. Custom category override

Use `category` when a single workflow manages several independent checks and
you want a separate comment for each:

```yaml
      - name: Report lint status
        if: always()
        uses: ./.github/actions/add-status-comment
        with:
          status: ${{ steps.lint.outcome == 'success' && 'passed' || 'error' }}
          category: 'Code Formatting'
          description: 'Lint result: `${{ steps.lint.outcome }}`'

      - name: Report test status
        if: always()
        uses: ./.github/actions/add-status-comment
        with:
          status: ${{ steps.tests.outcome == 'success' && 'passed' || 'error' }}
          category: 'Unit Tests'
          description: 'Test result: `${{ steps.tests.outcome }}`'
```

### 3. Using a custom token

```yaml
      - name: Report status
        uses: ./.github/actions/add-status-comment
        with:
          status: error
          token: ${{ secrets.MY_BOT_TOKEN }}
```

---

## How it works

1. **Marker** – every managed comment contains a hidden HTML comment at the
   top of its body:  
   `<!-- add-status-comment:{category} -->`  
   This lets the action find its own comment reliably, even across many runs.

2. **Find** – the action lists all issue comments for the PR and selects the
   one authored by `github-actions[bot]` whose body contains the marker.

3. **Create/update** – REST API (`/repos/.../issues/{pr}/comments`).

4. **Minimize/unminimize** – GitHub GraphQL `minimizeComment` /
   `unminimizeComment` mutations with classifier `RESOLVED`.

> **Note:** GitHub does not support "pinning" comments; minimizing/collapsing
> is used as the closest equivalent to "closing" a status comment.

---

## Supported events

The action must run in a `pull_request` or `pull_request_target` event context.
It exits with an error for any other event.

---

## Limitations

- Requires `gh` (GitHub CLI) and `python3` to be available on the runner
  (both are pre-installed on all GitHub-hosted runners).
- Minimize/unminimize GraphQL calls are non-fatal; a warning is emitted if
  they fail (e.g., due to missing permissions), but the comment body is still
  updated.
