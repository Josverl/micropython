#!/usr/bin/env bash
# comment.sh – implementation for the pr-status-comment composite action.
# Called by action.yml; relies on env vars set there.
set -euo pipefail

# ---------------------------------------------------------------------------
# 1. Validate inputs
# ---------------------------------------------------------------------------
STATUS_LOWER=$(echo "${INPUT_STATUS}" | tr '[:upper:]' '[:lower:]')
if [ "$STATUS_LOWER" != "error" ] && [ "$STATUS_LOWER" != "passed" ]; then
    echo "::error::pr-status-comment: invalid status '${INPUT_STATUS}'. Must be 'error' or 'passed'."
    exit 1
fi

# ---------------------------------------------------------------------------
# 2. Determine category (default: workflow name)
# ---------------------------------------------------------------------------
CATEGORY="${INPUT_CATEGORY:-}"
if [ -z "$CATEGORY" ]; then
    CATEGORY="${_WORKFLOW_NAME}"
fi
if [ -z "$CATEGORY" ]; then
    echo "::error::pr-status-comment: could not determine category (INPUT_CATEGORY and GITHUB_WORKFLOW are both empty)."
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Determine PR number from the event payload
# ---------------------------------------------------------------------------
EVENT_NAME="${_EVENT_NAME:-${GITHUB_EVENT_NAME:-}}"
if [ "$EVENT_NAME" != "pull_request" ] && [ "$EVENT_NAME" != "pull_request_target" ]; then
    echo "::error::pr-status-comment: this action only works on pull_request or pull_request_target events (got: '${EVENT_NAME}')."
    exit 1
fi

PR_NUMBER=$(jq -r '.pull_request.number // .number // empty' "${GITHUB_EVENT_PATH}")
if [ -z "$PR_NUMBER" ] || [ "$PR_NUMBER" = "null" ]; then
    echo "::error::pr-status-comment: could not determine PR number from event payload."
    exit 1
fi

OWNER="${_REPO%%/*}"
REPO="${_REPO#*/}"

echo "pr-status-comment: PR=#${PR_NUMBER}  category='${CATEGORY}'  status='${STATUS_LOWER}'"

# ---------------------------------------------------------------------------
# 4. Find existing comment (by marker + github-actions[bot])
# ---------------------------------------------------------------------------
MARKER="<!-- pr-status-comment:${CATEGORY} -->"

# gh api --paginate returns one JSON array per page; jq -s merges them all.
# At most one comment per category+bot should exist; take the first match.
COMMENT_JSON=$(
    gh api "/repos/${OWNER}/${REPO}/issues/${PR_NUMBER}/comments" \
        --paginate \
        2>/dev/null \
    | jq -s \
        --arg bot "github-actions[bot]" \
        --arg marker "$MARKER" \
        'add // [] | first(.[] | select(.user.login == $bot and (.body | contains($marker)))) // empty'
)

COMMENT_ID=""
COMMENT_NODE_ID=""
if [ -n "$COMMENT_JSON" ] && [ "$COMMENT_JSON" != "null" ] && [ "$COMMENT_JSON" != "" ]; then
    COMMENT_ID=$(echo "$COMMENT_JSON" | jq -r '.id')
    COMMENT_NODE_ID=$(echo "$COMMENT_JSON" | jq -r '.node_id')
    echo "pr-status-comment: found existing comment id=${COMMENT_ID}"
else
    echo "pr-status-comment: no existing comment found for category '${CATEGORY}'"
fi

# ---------------------------------------------------------------------------
# 5. Build comment body
# ---------------------------------------------------------------------------
if [ "$STATUS_LOWER" = "error" ]; then
    STATUS_EMOJI="❌"
    STATUS_LABEL="Error"
else
    STATUS_EMOJI="✅"
    STATUS_LABEL="Passed"
fi

# Marker first so it is invisible at the top; title on next line.
BODY="${MARKER}
## ${STATUS_EMOJI} ${CATEGORY}: ${STATUS_LABEL}"

if [ -n "${INPUT_DESCRIPTION:-}" ]; then
    BODY="${BODY}

${INPUT_DESCRIPTION}"
fi

# ---------------------------------------------------------------------------
# 6. Create / update / skip
# ---------------------------------------------------------------------------
if [ "$STATUS_LOWER" = "error" ]; then
    if [ -z "$COMMENT_ID" ]; then
        echo "pr-status-comment: creating new comment..."
        RESPONSE=$(
            jq -n --arg body "$BODY" '{body: $body}' \
            | gh api "/repos/${OWNER}/${REPO}/issues/${PR_NUMBER}/comments" \
                -X POST \
                --input -
        )
        COMMENT_NODE_ID=$(echo "$RESPONSE" | jq -r '.node_id')
        echo "pr-status-comment: created comment, node_id=${COMMENT_NODE_ID}"
    else
        echo "pr-status-comment: updating comment id=${COMMENT_ID}..."
        jq -n --arg body "$BODY" '{body: $body}' \
        | gh api "/repos/${OWNER}/${REPO}/issues/comments/${COMMENT_ID}" \
            -X PATCH \
            --input - \
            > /dev/null

        echo "pr-status-comment: unminimizing comment..."
        GQL_UNMINIMIZE="mutation {
          unminimizeComment(input: {subjectId: \"${COMMENT_NODE_ID}\"}) {
            unminimizedComment { isMinimized }
          }
        }"
        gh api graphql -f query="$GQL_UNMINIMIZE" \
        || echo "::warning::pr-status-comment: unminimizeComment GraphQL call failed (non-fatal)."
    fi

elif [ "$STATUS_LOWER" = "passed" ]; then
    if [ -n "$COMMENT_ID" ]; then
        echo "pr-status-comment: updating comment id=${COMMENT_ID} with passed status..."
        jq -n --arg body "$BODY" '{body: $body}' \
        | gh api "/repos/${OWNER}/${REPO}/issues/comments/${COMMENT_ID}" \
            -X PATCH \
            --input - \
            > /dev/null

        echo "pr-status-comment: minimizing comment..."
        GQL_MINIMIZE="mutation {
          minimizeComment(input: {subjectId: \"${COMMENT_NODE_ID}\", classifier: RESOLVED}) {
            minimizedComment { isMinimized }
          }
        }"
        gh api graphql -f query="$GQL_MINIMIZE" \
        || echo "::warning::pr-status-comment: minimizeComment GraphQL call failed (non-fatal)."
    else
        echo "pr-status-comment: no existing comment and status is 'passed' — nothing to do."
    fi
fi

echo "pr-status-comment: done."
