# Quick Reference Card — MicroPython Skill Builder

## 🚀 Quick Start (30 seconds)

```bash
cd tools/skill_builder

# One-time setup
pip install -r requirements.txt

# Run everything (8-16 minutes)
export GITHUB_TOKEN=YOUR_TOKEN  # Optional
python3 main.py --all
```

## 📁 File Structure

```
tools/skill_builder/
├── main.py                      ← Start here (orchestrator)
├── fetch_commits.py             ← Step 1: Get data
├── analyze_patterns.py          ← Step 2: Find patterns
├── generate_rules.py            ← Step 3: Make rules
├── test_skill.py                ← Step 4: Validate
├── quickstart.py                ← Interactive guide
├── setup.sh                     ← Installation helper
├── README.md                    ← Full documentation
├── IMPLEMENTATION_GUIDE.md      ← Technical details
└── data/                        ← Generated files (auto-created)
    ├── micropython_analysis_data.json      (raw data)
    ├── extracted_patterns.json            (patterns)
    ├── review_rules.json                  (for Copilot)
    ├── review_rules.yaml                  (for CI/CD)
    ├── REVIEW_RULES.md                    (documentation)
    └── SKILL_BUILDER_REPORT.md           (summary)
```

## 🎯 Common Commands

```bash
# Full pipeline (all steps)
python3 main.py --all

# Run up to specific step
python3 main.py --step 1    # Just fetch
python3 main.py --step 2    # Fetch + analyze
python3 main.py --step 3    # Fetch + analyze + generate

# With GitHub token (recommended)
python3 main.py --all --github-token YOUR_TOKEN

# Continue on errors
python3 main.py --all --ignore-errors

# Interactive setup
python3 quickstart.py

# Test the rules
python3 test_skill.py

# View results
cat data/REVIEW_RULES.md
ls -lh data/
```

## 📊 What Gets Generated

| File                             | Size       | Purpose                     |
| -------------------------------- | ---------- | --------------------------- |
| `micropython_analysis_data.json` | 2-5 MB     | Raw commits/PRs from GitHub |
| `extracted_patterns.json`        | 100-200 KB | Analyzed patterns           |
| `review_rules.json`              | ~50 KB     | **Use for Copilot**         |
| `review_rules.yaml`              | ~50 KB     | Use for CI/CD               |
| `REVIEW_RULES.md`                | ~30 KB     | Documentation               |
| `SKILL_BUILDER_REPORT.md`        | ~10 KB     | Summary report              |

## 🔍 8 Generated Rules

| #   | Rule ID                     | Severity   | Purpose                    |
| --- | --------------------------- | ---------- | -------------------------- |
| 1   | `micropy-memory-allocation` | ERROR      | Use m_new/m_del not malloc |
| 2   | `micropy-boundary-check`    | ERROR      | Validate buffer bounds     |
| 3   | `micropy-error-handling`    | WARNING    | Use mp*raise*\*            |
| 4   | `micropy-error-text-macro`  | WARNING    | Wrap with MP_ERROR_TEXT    |
| 5   | `micropy-type-safety`       | WARNING    | Use MicroPython types      |
| 6   | `micropy-config-guard`      | SUGGESTION | Use #if MICROPY\_\*        |
| 7   | `micropy-encapsulation`     | SUGGESTION | Mark internal code static  |
| 8   | `micropy-inline-docs`       | SUGGESTION | Document complex code      |

## ⏱️ Timeline

| Step      | Time         | What Happens                          |
| --------- | ------------ | ------------------------------------- |
| 1         | 5-10 min     | Download ~100 commits/PRs from GitHub |
| 2         | 30 sec       | Extract patterns from diffs           |
| 3         | <1 sec       | Generate rules in 3 formats           |
| 4         | 2-5 min      | Validate and test rules               |
| **Total** | **8-16 min** | Complete skill ready to use           |

## 🔧 Configuration

**Adjust in `fetch_commits.py`:**

```python
MAX_COMMITS_PER_AUTHOR = 20     # Default: get 20 per author (~100 total)
LOOK_BACK_DAYS = 730            # Default: last 2 years
TARGET_AUTHORS = [...]          # Edit for different authors
```

**Add patterns in `analyze_patterns.py`:**

```python
if re.search(r"your_pattern", line):
    pattern = "pattern_name"
    self.patterns[pattern][author] += 1
```

## 🐛 Troubleshooting

| Problem               | Solution                                          |
| --------------------- | ------------------------------------------------- |
| "Rate limit exceeded" | Add `--github-token YOUR_TOKEN`                   |
| "Data file not found" | Run `python3 main.py --step 1` first              |
| "Import error"        | Run `pip install -r requirements.txt`             |
| "Slow fetch"          | Use GitHub token to get 5000 req/hr instead of 60 |
| "Just want rules?"    | Run `python3 main.py --step 3` (skip fetch)       |

## 📝 Authors Analyzed

- 👤 **Damien George** (damien) — MicroPython creator
- 👤 **Jeff Epler** (jepler) — Embedded systems expert
- 👤 **Andrew Leech** (andrewleech) — Platform specialist
- 👤 **Alessandro Gatti** (agattidev) — Performance expert
- 👤 **Angus Gratton** (angus) — Hardware integration

## 🎓 What You Get

✅ **Rules based on 100+ real commits**
✅ **Three output formats** (JSON, YAML, Markdown)
✅ **Fully automated** — no manual work
✅ **Ready for Copilot** — JSON format
✅ **Ready for CI/CD** — YAML format
✅ **Ready for docs** — Markdown format
✅ **Tested & validated** — against real code
✅ **Extensible** — easy to add more patterns/rules

## 📚 Where to Go Next

1. **Quick start:** `python3 main.py --all`
2. **Learn more:** Read `README.md`
3. **Deep dive:** Read `IMPLEMENTATION_GUIDE.md`
4. **See rules:** `cat data/REVIEW_RULES.md`
5. **Test rules:** `python3 test_skill.py`
6. **Integrate:** Use `data/review_rules.json` with Copilot

## 💡 Pro Tips

```bash
# Speed up (skip commits, focus on generation)
python3 main.py --step 3

# Run just validation without re-fetching
python3 test_skill.py

# View generated rules
cat data/REVIEW_RULES.md | less

# Check output file sizes
du -sh data/*

# Parse the JSON programmatically
python3 -m json.tool data/review_rules.json | head -50

# Use with GitHub Actions
# See README.md for CI/CD integration example
```

## 🔗 Integration Examples

**With Copilot Extension:**

```javascript
const rules = require("./data/review_rules.json");
// Apply rules to code during review
```

**With GitHub Actions:**

```yaml
- run: python3 tools/skill_builder/test_skill.py
```

**As Pre-commit Hook:**

```bash
#!/bin/sh
python3 tools/skill_builder/test_skill.py
```

---

**Status:** ✅ Ready to use
**Next:** Run `python3 main.py --all` in `tools/skill_builder/`
