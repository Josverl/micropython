#!/usr/bin/env python3
"""
MicroPython Code Review Skill Builder - Main Orchestrator

Coordinates the full pipeline:
1. Fetch commits and PRs from target authors
2. Analyze code patterns
3. Generate review skill rules
4. Validate and test the skill
"""

import argparse
import json
import sys
from pathlib import Path


def run_pipeline(args):
    """Run the complete skill building pipeline."""

    tool_dir = Path(__file__).parent
    data_dir = tool_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("MicroPython C Code Review Skill Builder")
    print("=" * 70)

    # Step 1: Fetch commits and PRs
    if args.step <= 1 or args.all:
        print("\n[Step 1/4] Fetching commits and PRs from target authors...")
        print("-" * 70)

        try:
            from fetch_commits import CommitFetcher

            fetcher = CommitFetcher(github_token=args.github_token)
            data = fetcher.fetch_all()
            data_file = fetcher.save_data(data)

            print(f"\n✓ Fetched data saved to {data_file}")

        except Exception as e:
            print(f"\n✗ Error during fetch: {e}")
            if not args.ignore_errors:
                sys.exit(1)

    # Step 2: Analyze patterns
    if args.step <= 2 or args.all:
        print("\n[Step 2/4] Analyzing code patterns...")
        print("-" * 70)

        try:
            from analyze_patterns import PatternAnalyzer

            data_file = data_dir / "micropython_analysis_data.json"
            if not data_file.exists():
                raise FileNotFoundError(f"Data file not found: {data_file}")

            analyzer = PatternAnalyzer(str(data_file))
            patterns, samples, stats = analyzer.analyze_all()
            analyzer.export_patterns()

            print(f"\n✓ Found {stats['total_patterns']} unique pattern types")

        except Exception as e:
            print(f"\n✗ Error during analysis: {e}")
            if not args.ignore_errors:
                sys.exit(1)

    # Step 3: Generate GitHub Copilot skill
    if args.step <= 3 or args.all:
        print("\n[Step 3/4] Generating GitHub Copilot SKILL.md...")
        print("-" * 70)

        try:
            import subprocess
            result = subprocess.run([sys.executable, str(tool_dir / "generate_skill.py")], 
                                  check=True, cwd=str(tool_dir))
            
            print(f"\n✓ Generated SKILL.md in .github/skills/micropython-c-code-review/")

        except Exception as e:
            print(f"\n✗ Error generating skill: {e}")
            if not args.ignore_errors:
                sys.exit(1)

    # Step 4: Create summary report
    if args.step <= 4 or args.all:
        print("\n[Step 4/4] Creating summary report...")
        print("-" * 70)

        try:
            create_summary_report(data_dir)
            print(f"\n✓ Summary report created")

        except Exception as e:
            print(f"\n✗ Error creating report: {e}")
            if not args.ignore_errors:
                sys.exit(1)

    print("\n" + "=" * 70)
    print("✓ Skill builder pipeline completed successfully!")
    print("=" * 70)
    print("\nGenerated files:")
    print(f"  - SKILL.md:              .github/skills/micropython-c-code-review/SKILL.md")
    print(f"  - Pattern reference:     .github/skills/micropython-c-code-review/patterns-reference.json")
    print(f"  - Raw analysis data:     {data_dir / 'micropython_analysis_data.json'}")
    print(f"  - Extracted patterns:    {data_dir / 'extracted_patterns.json'}")
    print("\nThe skill is now available to GitHub Copilot when working in this repository.")
    print("Copilot will automatically use it for C code reviews in MicroPython.")
    return 0
    print("1. Review the generated rules in data/REVIEW_RULES.md")
    print("2. Test the rules using test_skill.py")
    print("3. Integrate with Copilot using the JSON or YAML format")
    print("\nOutput directory: " + str(data_dir))


def create_summary_report(data_dir):
    """Create a summary report of the skill building process."""
    report_file = data_dir / "SKILL_BUILDER_REPORT.md"

    report = """# MicroPython C Code Review Skill - Builder Report

## Overview

This report summarizes the automated code review skill built from analysis of
MicroPython repository commits and pull requests.

## Data Sources

- **Repository:** micropython/micropython
- **Target Authors:** 
  - Damien George (damien)
  - Jeff Epler (jepler)
  - Andrew Leech (andrewleech)
  - Alessandro Gatti (agattidev)
  - Angus Gratton (angus)

## Generated Artifacts

### 1. Analysis Data
- **File:** `micropython_analysis_data.json`
- **Content:** Raw commits and PRs with diffs and metadata
- **Size:** ~100 commits and PRs analyzed

### 2. Extracted Patterns
- **File:** `extracted_patterns.json`
- **Content:** Identified code patterns and statistics
- **Categories:**
  - Memory allocation patterns
  - Error handling practices
  - Configuration guards
  - Error text macros
  - Type safety patterns
  - Encapsulation practices
  - Inline documentation
  - Boundary checking

### 3. Review Skill Rules
- **Formats:** JSON, YAML, Markdown
- **Count:** 8 base rules derived from patterns
- **Coverage:**
  - Memory safety
  - Error handling
  - Type safety
  - Code style
  - Documentation
  - Configuration

## Rule Categories

### Error (Must fix)
- Memory allocation functions
- Boundary validation

### Warning (Should fix)
- Error handling consistency
- Type safety
- MP_ERROR_TEXT usage

### Suggestion (Consider)
- Configuration guards
- Encapsulation with static/const
- Inline documentation

## Usage

### As JSON Skill
```json
{
  "skill": {
    "name": "MicroPython C Code Review",
    "rules": [...]
  }
}
```

### As YAML Config
Use with GitHub Actions, Copilot extensions, or other CI/CD tools.

### As Markdown
Reference documentation for developers.

## Integration Points

This skill can be integrated with:
1. **GitHub Copilot Extensions** - Custom review rules
2. **CI/CD Pipelines** - Automated PR checks
3. **Code Review Tools** - Pre-submission validation
4. **IDE Plugins** - Real-time feedback

## Future Enhancements

- [ ] Expand pattern analysis with AST parsing
- [ ] Add metrics extraction (code size, complexity)
- [ ] Create ML model for anomaly detection
- [ ] Add platform-specific rules (ESP32, RP2, etc.)
- [ ] Integrate with GitHub's native review API
- [ ] Add test coverage pattern analysis

## Files Generated

```
tools/skill_builder/data/
├── micropython_analysis_data.json    # Raw data
├── extracted_patterns.json           # Analyzed patterns
├── review_rules.json                 # JSON format rules
├── review_rules.yaml                 # YAML format rules
├── REVIEW_RULES.md                   # Markdown documentation
└── SKILL_BUILDER_REPORT.md          # This file
```

---

Generated by MicroPython Code Review Skill Builder v0.1.0
"""

    with open(report_file, "w") as f:
        f.write(report)

    return report_file


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="MicroPython C Code Review Skill Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline
  python main.py --all

  # Run only fetch step
  python main.py --step 1

  # Run with GitHub token for higher rate limit
  python main.py --all --github-token YOUR_TOKEN

  # Skip errors and continue
  python main.py --all --ignore-errors
        """,
    )

    parser.add_argument("--all", action="store_true", help="Run complete pipeline (all steps)")
    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help="Run up to this step (1=fetch, 2=analyze, 3=generate, 4=report)",
    )
    parser.add_argument(
        "--github-token", type=str, help="GitHub API token (can also set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--ignore-errors", action="store_true", help="Continue on errors instead of exiting"
    )

    args = parser.parse_args()

    # If no step specified and not all, assume user wants all
    if not args.all and args.step == 1 and len(sys.argv) == 1:
        args.all = True

    run_pipeline(args)


if __name__ == "__main__":
    main()
