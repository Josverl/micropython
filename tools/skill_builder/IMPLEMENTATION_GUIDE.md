# IMPLEMENTATION GUIDE: MicroPython C Code Review Skill Builder

## What Was Built

A complete, fully-automated system for extracting best practices from MicroPython commits and generating code review rules. **No manual work required** — everything runs end-to-end via Python scripts.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  fetch_commits.py                                               │
│  • Connects to GitHub API                                       │
│  • Fetches ~100 commits from 5 target authors                   │
│  • Extracts full diffs and metadata                             │
│  • Stores in micropython_analysis_data.json                     │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  analyze_patterns.py                                            │
│  • Parses unified diff format                                   │
│  • Detects patterns in C code:                                  │
│    - Memory allocation (m_new, malloc)                          │
│    - Error handling (mp_raise_*)                                │
│    - Config guards (#if MICROPY_*)                              │
│    - Type safety patterns                                       │
│    - Encapsulation (static, const)                              │
│  • Stores statistics in extracted_patterns.json                 │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  generate_rules.py                                              │
│  • Maps patterns to review rules                                │
│  • Assigns severity levels (error/warning/suggestion)           │
│  • Generates 8+ actionable rules                                │
│  • Exports in 3 formats:                                        │
│    - JSON (for Copilot extensions)                              │
│    - YAML (for CI/CD integration)                               │
│    - Markdown (for documentation)                               │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  test_skill.py                                                  │
│  • Validates rules with sample code                             │
│  • Tests against real commits                                   │
│  • Generates validation report                                  │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  main.py (Orchestrator)                                         │
│  • Coordinates all steps                                        │
│  • Handles errors gracefully                                    │
│  • Generates summary report                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Core Scripts

### 1. **fetch_commits.py** — GitHub API Data Collection

**What it does:** Fetches ~100 commits and PRs from the 5 target authors

**Key features:**

- Paginated GitHub API requests (respects rate limits)
- Automatic token handling for authentication
- Extracts full patch diffs from each commit
- Stores metadata: author, date, files changed, additions/deletions
- Handles API errors gracefully

**Key functions:**

- `CommitFetcher.fetch_commits_by_author()` — Retrieves commits
- `CommitFetcher.fetch_pull_requests_by_author()` — Retrieves PRs
- `CommitFetcher._commit_to_dict()` — Normalizes commit data
- `CommitFetcher.save_data()` — Writes to JSON

**Output:** `data/micropython_analysis_data.json` (~2-5 MB)

### 2. **analyze_patterns.py** — Pattern Extraction Engine

**What it does:** Parses diffs and extracts C code best practices

**Key patterns detected:**

- **memory_allocation** — Usage of `m_new`, `m_del`, `m_renew`
- **error_handling** — `mp_raise_*` function calls
- **config_guard** — `#if MICROPY_*` preprocessor guards
- **error_text_macro** — `MP_ERROR_TEXT` usage
- **boundary_check** — Size validation before buffer access
- **type_safety** — MicroPython type definitions (mp_obj_t, size_t, etc.)
- **inline_comments** — Documentation quality
- **encapsulation** — `static` and `const` usage

**Key functions:**

- `PatternAnalyzer._analyze_patch()` — Parses unified diff
- `PatternAnalyzer._check_patterns()` — Regex-based pattern detection
- `PatternAnalyzer._calculate_statistics()` — Aggregates findings
- `PatternAnalyzer.export_patterns()` — Saves results

**Output:** `data/extracted_patterns.json` (pattern statistics)

### 3. **generate_rules.py** — Rule Generation

**What it does:** Converts patterns into review rules

**Rules generated (8 base + extensible):**

1. `micropy-memory-allocation` (ERROR) — Use m_new/m_del
2. `micropy-error-handling` (WARNING) — Use mp*raise*\*
3. `micropy-error-text-macro` (WARNING) — Wrap with MP_ERROR_TEXT
4. `micropy-config-guard` (SUGGESTION) — Use #if MICROPY\_\*
5. `micropy-type-safety` (WARNING) — MicroPython types
6. `micropy-encapsulation` (SUGGESTION) — Mark internal code static
7. `micropy-inline-docs` (SUGGESTION) — Document complex logic
8. `micropy-boundary-check` (ERROR) — Validate buffer bounds

**Key functions:**

- `RuleGenerator.generate_rules()` — Creates rule set
- `RuleGenerator.export_as_json()` — JSON format for Copilot
- `RuleGenerator.export_as_yaml()` — YAML format for CI/CD
- `RuleGenerator.export_as_markdown()` — Markdown documentation

**Outputs:**

- `data/review_rules.json` — Copilot extension format
- `data/review_rules.yaml` — CI/CD pipeline format
- `data/REVIEW_RULES.md` — Developer documentation

### 4. **test_skill.py** — Validation Framework

**What it does:** Validates rules work correctly

**Validation includes:**

- Unit tests with sample C code snippets
- Integration tests against real commits
- Pattern matching accuracy checks
- Rule coverage statistics

**Key functions:**

- `RuleValidator.validate_code()` — Tests code against rules
- `RuleValidator.test_samples()` — Unit test suite
- `RuleValidator.test_real_commits()` — Integration testing
- `RuleValidator._find_pattern_matches()` — Regex matching

**Output:** Validation report with pass/fail statistics

### 5. **main.py** — Orchestrator

**What it does:** Coordinates the full pipeline

**Features:**

- Step-by-step execution with progress tracking
- Error handling and graceful failures
- Command-line interface with argument parsing
- Optional `--all` flag to run complete pipeline

**Key functions:**

- `run_pipeline()` — Main execution logic
- `create_summary_report()` — Generates SKILL_BUILDER_REPORT.md

**Usage:**

```bash
python3 main.py --all                           # Full pipeline
python3 main.py --step 2                        # Run up to step 2
python3 main.py --all --github-token TOKEN      # With authentication
python3 main.py --all --ignore-errors           # Continue on error
```

## Generated Artifacts

### 1. **micropython_analysis_data.json**

```json
{
  "metadata": {...},
  "commits": {
    "damien": [...],
    "jepler": [...]
  },
  "pull_requests": {
    "damien": [...],
    "jepler": [...]
  }
}
```

Size: ~2-5 MB | Raw data from GitHub API

### 2. **extracted_patterns.json**

```json
{
  "statistics": {
    "total_patterns": 8,
    "patterns_by_type": {
      "memory_allocation": {"total": 145, "by_author": {...}},
      "error_handling": {"total": 203, "by_author": {...}}
    }
  },
  "code_samples": {...},
  "patterns": {...}
}
```

Size: ~100-200 KB | Analyzed patterns and statistics

### 3. **review_rules.json** (Copilot Format)

```json
{
  "skill": {
    "name": "MicroPython C Code Review",
    "version": "1.0.0",
    "rules": [
      {
        "id": "micropy-memory-allocation",
        "category": "memory_safety",
        "severity": "error",
        "title": "Use MicroPython memory allocation functions",
        "pattern": "\\b(malloc|calloc|realloc|free)\\s*\\(",
        "examples": {...}
      }
    ]
  }
}
```

Size: ~50 KB | Copilot extension compatible format

### 4. **review_rules.yaml** (CI/CD Format)

YAML-based rule format for GitHub Actions, pre-commit hooks, etc.

### 5. **REVIEW_RULES.md** (Documentation)

Human-readable rule documentation with examples and explanations.

## How It Works — Step by Step

### Step 1: Data Fetch (5-10 minutes)

```
fetch_commits.py
├── Authenticate with GitHub (using GITHUB_TOKEN if provided)
├── Query for commits from each author:
│   └── GET /repos/micropython/micropython/commits?author=USERNAME
├── Extract fields: SHA, message, files, diffs
├── Query for PRs from each author:
│   └── GET /repos/micropython/micropython/pulls?creator=USERNAME
├── Fetch PR files and diffs
├── Store complete data structure in JSON
└── Log progress and timing
```

**Rate limiting:**

- Unauthenticated: 60 requests/hour (may hit limit)
- Authenticated: 5,000 requests/hour (recommended)

### Step 2: Pattern Analysis (30 seconds)

```
analyze_patterns.py
├── Load micropython_analysis_data.json
├── For each commit/PR:
│   ├── Extract C files only
│   ├── Parse unified diff format
│   ├── Get added lines (starting with +)
│   └── Run pattern checks on each line:
│       ├── Regex: \bm_new\b (memory allocation)
│       ├── Regex: \bmp_raise_\w+\b (error handling)
│       ├── Regex: #if\s+MICROPY_ (config guards)
│       └── ... (6 more patterns)
├── Aggregate statistics by author
├── Collect sample code snippets
└── Export to extracted_patterns.json
```

**Pattern detection uses:**

- Regular expressions for syntax matching
- Line-by-line analysis
- Frequency counting per author

### Step 3: Rule Generation (<1 second)

```
generate_rules.py
├── Load extracted_patterns.json (optional)
├── Define 8 base rules with:
│   ├── Rule ID (e.g., "micropy-memory-allocation")
│   ├── Severity level (error/warning/suggestion)
│   ├── Title and description
│   ├── Pattern (regex)
│   └── Examples (bad and good code)
├── Enhance with pattern statistics
├── Generate three formats:
│   ├── JSON (for programmatic use)
│   ├── YAML (for CI/CD)
│   └── Markdown (for documentation)
└── Write to data/ directory
```

### Step 4: Validation (2-5 minutes)

```
test_skill.py
├── Unit tests:
│   ├── Load predefined test cases
│   ├── Run each case through rule engine
│   ├── Compare actual vs expected results
│   └── Report pass/fail status
├── Integration tests:
│   ├── Load real commits from analysis data
│   ├── Apply rules to actual C code diffs
│   ├── Count issues by severity
│   └── Generate statistics
└── Output validation report
```

## Key Design Decisions

### 1. **No Manual Work Required**

- Fully automated GitHub API integration
- All extraction and analysis in Python
- Single-command pipeline execution

### 2. **Three Output Formats**

- **JSON:** For programmatic integration with Copilot
- **YAML:** For CI/CD pipelines and GitHub Actions
- **Markdown:** For human documentation

### 3. **Pattern-Based, Not AST-Based**

- Regex patterns for quick analysis
- Works with partial/incomplete code
- Can be extended without code recompilation

### 4. **Author-Centric Analysis**

- Tracks which author contributed each pattern
- Shows evolution of practices over time
- Identifies consensus practices

### 5. **Graceful Error Handling**

- Optional GitHub token (works without, with limits)
- `--ignore-errors` flag for partial failures
- Detailed error logging

## Extension Points

### Add New Pattern Detection

Edit `analyze_patterns.py`, modify `_check_patterns()`:

```python
def _check_patterns(self, line, author, ref):
    # Add new pattern
    if re.search(r"your_new_pattern", line):
        pattern = "your_pattern_name"
        self.patterns[pattern][author] += 1
```

### Add Custom Rules

Edit `generate_rules.py`, add to `BASE_RULES`:

```python
{
    "id": "your-rule-id",
    "category": "your_category",
    "severity": "error",
    "title": "Your rule title",
    "description": "Detailed description",
    "pattern": r"regex_pattern"
}
```

### Filter Different Authors

Edit `fetch_commits.py`, modify `TARGET_AUTHORS`:

```python
TARGET_AUTHORS = [
    "new_author1",
    "new_author2",
]
```

## Performance Characteristics

| Step              | Time         | Notes                             |
| ----------------- | ------------ | --------------------------------- |
| Fetch (step 1)    | 5-10 min     | Depends on GitHub API rate limits |
| Analyze (step 2)  | 30 sec       | Fast regex-based pattern matching |
| Generate (step 3) | <1 sec       | Pure JSON/YAML generation         |
| Test (step 4)     | 2-5 min      | Real commit analysis + validation |
| **Total**         | **8-16 min** | **One-time cost**                 |

**To speed up:**

- Use GitHub token (avoid rate limiting)
- Reduce `MAX_COMMITS_PER_AUTHOR` in fetch_commits.py
- Skip test step with `--step 3`

## Dependencies

```
PyGithub==2.1.1          # GitHub API client
gitpython==3.1.43        # Git operations
requests==2.31.0         # HTTP library
python-dateutil==2.8.2   # Date handling
```

**Why these?**

- PyGithub: Official GitHub API wrapper, handles authentication
- gitpython: For local repo operations if needed
- requests: Fallback HTTP support
- python-dateutil: Cross-platform date handling

## Next Steps to Use the Skill

### 1. **Run the Complete Pipeline**

```bash
cd tools/skill_builder
export GITHUB_TOKEN=your_token
python3 main.py --all
```

### 2. **Review Generated Rules**

```bash
cat data/REVIEW_RULES.md
```

### 3. **Test Against Real Code**

```bash
python3 test_skill.py
```

### 4. **Integrate with Copilot**

- Use `data/review_rules.json` in a Copilot extension
- See Copilot extension documentation for integration

### 5. **Use in CI/CD**

- Use `data/review_rules.yaml` in GitHub Actions
- Implement custom linter using the rules

---

**Status:** ✅ Complete and ready to run
**Next Action:** Execute `python3 main.py --all` in the skill_builder directory
