# MicroPython C Code Review Skill Builder

A comprehensive system to analyze commits and pull requests from key MicroPython contributors and automatically generate code review rules that enforce best practices in C/C++ and embedded development.

## Overview

This skill builder extracts patterns from ~100 commits and PRs by 5 core MicroPython contributors:

- **Damien George** — MicroPython creator and lead maintainer
- **Jeff Epler** — Core contributor and embedded systems expert
- **Andrew Leech** — Platform support and optimization specialist
- **Alessandro Gatti** — Memory and performance optimization
- **Angus Gratton** — Hardware integration and platform support

The analysis generates actionable review rules covering:

- Memory safety and allocation patterns
- Error handling and exception management
- Type safety and embedded development practices
- Code style and encapsulation
- Configuration management and build optimizations
- Documentation and inline comments

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set GitHub token (optional but recommended)
export GITHUB_TOKEN=your_github_token_here
```

### Run the Full Pipeline

```bash
# Interactive setup
python3 quickstart.py

# Or run directly
python3 main.py --all

# With GitHub token
python3 main.py --all --github-token YOUR_TOKEN
```

### Run Individual Steps

```bash
# Step 1: Fetch commits and PRs
python3 main.py --step 1

# Step 2: Analyze patterns
python3 main.py --step 2

# Step 3: Generate rules
python3 main.py --step 3

# Step 4: Create report
python3 main.py --step 4
```

## Directory Structure

```
tools/skill_builder/
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── main.py                         # Main orchestrator
├── quickstart.py                   # Interactive setup
├── fetch_commits.py                # GitHub API data collector
├── analyze_patterns.py             # Code pattern analyzer
├── generate_rules.py               # Rule generator
├── test_skill.py                   # Validation and testing
└── data/                           # Generated artifacts
    ├── micropython_analysis_data.json    # Raw commits/PRs
    ├── extracted_patterns.json          # Analyzed patterns
    ├── review_rules.json                # JSON format rules
    ├── review_rules.yaml                # YAML format rules
    ├── REVIEW_RULES.md                  # Markdown documentation
    └── SKILL_BUILDER_REPORT.md         # Summary report
```

## Usage Examples

### Example 1: Generate Rules from Commits

```bash
python3 main.py --all --github-token YOUR_TOKEN
```

This will:

1. Fetch ~100 commits and PRs from the 5 target authors
2. Extract code patterns (memory allocation, error handling, etc.)
3. Generate 8+ review rules in JSON, YAML, and Markdown formats
4. Create a summary report

### Example 2: Test Rules Against Code

```bash
python3 test_skill.py
```

This will:

1. Test rules with predefined sample code snippets
2. Validate against real MicroPython commits
3. Generate a validation report with statistics

### Example 3: Use Rules in GitHub Actions

```yaml
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: MicroPython Code Review
        run: |
          python3 tools/skill_builder/main.py --all
          python3 tools/skill_builder/test_skill.py
```

## Generated Artifacts

### 1. `review_rules.json`

Complete rule set in JSON format suitable for:

- Copilot extensions
- Custom CI/CD integration
- IDE plugins

**Structure:**

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
        "description": "...",
        "pattern": "...",
        "examples": { "bad": "...", "good": "..." }
      }
    ]
  }
}
```

### 2. `review_rules.yaml`

YAML format for GitHub Actions and other CI/CD tools.

### 3. `REVIEW_RULES.md`

Human-readable documentation with examples and rationale.

### 4. `extracted_patterns.json`

Detailed pattern statistics from commit analysis:

- Frequency of each pattern type
- Occurrences by author
- Code samples

### 5. `SKILL_BUILDER_REPORT.md`

Summary report of the analysis process and results.

## Rule Categories

### Error Rules (Must Fix)

- `micropy-memory-allocation` — Use m_new/m_del instead of malloc/free
- `micropy-boundary-check` — Validate buffer boundaries

### Warning Rules (Should Fix)

- `micropy-error-handling` — Use mp*raise*\* for exceptions
- `micropy-error-text-macro` — Wrap error messages with MP_ERROR_TEXT
- `micropy-type-safety` — Use MicroPython type definitions

### Suggestion Rules (Consider)

- `micropy-config-guard` — Use #if MICROPY\_\* for optional features
- `micropy-encapsulation` — Mark internal code as static
- `micropy-inline-docs` — Add comments for complex logic

## Integration Paths

### 1. GitHub Copilot Extensions

Create a VS Code extension that uses the JSON rules:

```javascript
// extension.js
const rules = require("./review_rules.json");
// Apply rules during code review
```

### 2. GitHub Actions Workflow

```yaml
- name: Review Code
  run: |
    python3 check_compliance.py \
      --rules tools/skill_builder/data/review_rules.json \
      --files src/**/*.c
```

### 3. CI/CD Integration

Load the YAML rules into your linting pipeline:

```bash
yamllint -d tools/skill_builder/data/review_rules.yaml src/
```

### 4. IDE Integration

Use with IDE plugins for real-time feedback:

```bash
clang-tidy --config=review_rules.yaml src/*.c
```

## Advanced Usage

### Custom Author Set

Edit `fetch_commits.py` to analyze different authors:

```python
TARGET_AUTHORS = [
    "your_author",
    "another_author",
]
```

### Adjust Analysis Scope

Modify `fetch_commits.py` constants:

```python
MAX_COMMITS_PER_AUTHOR = 30    # Get more commits
LOOK_BACK_DAYS = 365           # Look back 1 year instead of 2
```

### Filter by File Type

In `analyze_patterns.py`, modify file extension check:

```python
if file_info["filename"].endswith((".c", ".h")):  # Include headers
```

## Performance

- **Data Fetch:** ~2-5 minutes (depends on GitHub API rate limits)
- **Pattern Analysis:** ~30 seconds
- **Rule Generation:** <1 second
- **Total Runtime:** ~3-6 minutes

**Rate Limiting:**

- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour

Use `--github-token` to avoid rate limit issues.

## Troubleshooting

### "GitHub token required"

Set your token:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
python3 main.py --all
```

### "Data file not found"

Ensure step 1 (fetch) completed successfully:

```bash
python3 main.py --step 1
```

### "Pattern analysis failed"

Check that the data file is valid JSON:

```bash
python3 -m json.tool data/micropython_analysis_data.json > /dev/null
```

### Slow performance

- Check your internet connection
- Use a GitHub token to avoid rate limiting
- Reduce MAX_COMMITS_PER_AUTHOR in fetch_commits.py

## Development

### Add New Pattern Detection

Edit `analyze_patterns.py`, add to `_check_patterns()`:

```python
if re.search(r"your_pattern", line):
    pattern = "your_pattern_name"
    self.patterns[pattern][author] += 1
```

### Customize Rule Generation

Edit `generate_rules.py` and add to `BASE_RULES`:

```python
{
    "id": "your-rule-id",
    "category": "your_category",
    "severity": "error|warning|suggestion",
    "title": "Your rule title",
    "description": "Detailed description...",
    "pattern": r"regex_pattern"
}
```

### Extend Testing

Add test cases to `test_skill.py`:

```python
test_cases.append({
    "name": "Your test case",
    "code": "code to test",
    "should_trigger": "rule_id"
})
```

## Contributing

This skill builder is part of the MicroPython project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This skill builder is part of MicroPython and follows the same license terms.

## References

- [MicroPython Repository](https://github.com/micropython/micropython)
- [MicroPython Code Conventions](https://github.com/micropython/micropython/blob/master/CODECONVENTIONS.md)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub API Reference](https://docs.github.com/en/rest)

## Support

For issues or questions:

- Check existing issues in the MicroPython repository
- Review the generated SKILL_BUILDER_REPORT.md
- Run `python3 test_skill.py` for diagnostics

---

**MicroPython Code Review Skill Builder v0.1.0**
