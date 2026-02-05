#!/usr/bin/env python3
"""
Analyze C code patterns from commit diffs.

Extracts best practices from MicroPython commits:
- Memory allocation patterns (m_new, m_del, m_renew)
- Error handling (mp_raise_* functions)
- Configuration guards (#if MICROPY_*)
- Code size impacts
- Testing patterns
- Memory-conscious coding
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class PatternAnalyzer:
    """Analyzes C code patterns from commit diffs."""

    def __init__(self, data_file=None):
        """Initialize analyzer with fetched data."""
        self.data = None
        if data_file:
            with open(data_file, "r") as f:
                self.data = json.load(f)

        self.patterns = defaultdict(lambda: defaultdict(int))
        self.code_samples = defaultdict(list)
        self.statistics = {}

    def analyze_all(self):
        """Analyze all commits and PRs."""
        if not self.data:
            raise ValueError("No data loaded. Provide a data file.")

        print("Analyzing patterns...")

        # Analyze commits
        for author, commits in self.data.get("commits", {}).items():
            for commit in commits:
                self._analyze_commit(commit, author)

        # Analyze PRs
        for author, prs in self.data.get("pull_requests", {}).items():
            for pr in prs:
                self._analyze_pr(pr, author)

        self.statistics = self._calculate_statistics()
        return self.patterns, self.code_samples, self.statistics

    def _analyze_commit(self, commit, author):
        """Analyze a single commit."""
        for file_info in commit.get("files", []):
            if file_info["filename"].endswith(".c"):
                patch = file_info.get("patch", "")
                self._analyze_patch(patch, author, commit["sha"][:8])

    def _analyze_pr(self, pr, author):
        """Analyze files in a PR."""
        for file_info in pr.get("files", []):
            if file_info["filename"].endswith(".c"):
                patch = file_info.get("patch", "")
                self._analyze_patch(patch, author, f"PR#{pr['number']}")

    def _analyze_patch(self, patch, author, ref):
        """Analyze a unified diff patch."""
        if not patch:
            return

        # Extract only added lines (starting with +)
        added_lines = [
            line[1:]
            for line in patch.split("\n")
            if line.startswith("+") and not line.startswith("+++")
        ]

        for line in added_lines:
            self._check_patterns(line, author, ref)

    def _check_patterns(self, line, author, ref):
        """Check for specific code patterns in a line."""

        # Memory allocation patterns
        if re.search(r"\bm_new\b|\bm_renew\b|\bm_del\b", line):
            pattern = "memory_allocation"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # Error handling patterns
        if re.search(r"\bmp_raise_\w+\b", line):
            pattern = "error_handling"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # Configuration guards
        if re.search(r"#if\s+MICROPY_", line):
            pattern = "config_guard"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # String constants with MP_ERROR_TEXT
        if "MP_ERROR_TEXT" in line:
            pattern = "error_text_macro"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # Boundary checks
        if re.search(r"if\s*\([^)]*[<>][^)]*\)", line) and "if" in line:
            pattern = "boundary_check"
            self.patterns[pattern][author] += 1

        # Type safety (size_t, uint32_t, etc.)
        if re.search(r"\b(size_t|uint\d+_t|int\d+_t|mp_obj_t|mp_int_t)\b", line):
            pattern = "type_safety"
            self.patterns[pattern][author] += 1

        # Comments and documentation
        if "//" in line or "/*" in line:
            pattern = "inline_comments"
            self.patterns[pattern][author] += 1

        # Static/const for encapsulation
        if re.search(r"\b(static|const)\s+(int|char|void|uint|size_t)", line):
            pattern = "encapsulation"
            self.patterns[pattern][author] += 1

        # mp_printf / mp_vprintf usage
        if re.search(r"\bmp_(v)?printf\b", line):
            pattern = "mp_printf"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # vstr usage for dynamic strings
        if re.search(r"\bvstr_(init|add|add_str|add_byte|add_char|add_len|printf)\b", line):
            pattern = "vstr_usage"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # MP_DEFINE_CONST_FUN_OBJ_* usage
        if re.search(r"\bMP_DEFINE_CONST_FUN_OBJ(_\d+)?\b", line):
            pattern = "const_fun_obj"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # MP_ROM_PTR / MP_ROM_QSTR usage
        if re.search(r"\bMP_ROM_(PTR|QSTR)\b", line):
            pattern = "rom_table"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # mp_obj_new_* usage
        if re.search(r"\bmp_obj_new_\w+\b", line):
            pattern = "mp_obj_new"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # qstr usage (interned strings)
        if re.search(r"\bMP_QSTR_\w+\b|\bqstr_\w+\b", line):
            pattern = "qstr_usage"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # mp_stream protocol usage
        if re.search(r"\bmp_stream_\w+\b", line):
            pattern = "mp_stream"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

        # mp_arg parsing usage
        if re.search(r"\bmp_arg_\w+\b|\bMP_ARG_\w+\b", line):
            pattern = "mp_arg"
            self.patterns[pattern][author] += 1
            if len(self.code_samples[pattern]) < 10:
                self.code_samples[pattern].append({"line": line.strip(), "ref": ref})

    def _calculate_statistics(self):
        """Calculate summary statistics."""
        stats = {
            "total_patterns": len(self.patterns),
            "patterns_by_type": {},
            "authors": list(self.data.get("commits", {}).keys()),
        }

        for pattern_name, author_counts in self.patterns.items():
            total = sum(author_counts.values())
            stats["patterns_by_type"][pattern_name] = {
                "total": total,
                "by_author": dict(author_counts),
            }

        return stats

    def export_patterns(self, output_file=None):
        """Export patterns to JSON for rule generation."""
        if output_file is None:
            output_file = Path(__file__).parent / "data" / "extracted_patterns.json"

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        export_data = {
            "timestamp": str(Path(output_file).parent.stat()),
            "statistics": self.statistics,
            "code_samples": dict(self.code_samples),
            "patterns": {k: dict(v) for k, v in self.patterns.items()},
        }

        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"Patterns exported to: {output_file}")
        return output_file


def main():
    """Main entry point."""
    data_file = Path(__file__).parent / "data" / "micropython_analysis_data.json"

    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        print("Run fetch_commits.py first to fetch the data.")
        return

    analyzer = PatternAnalyzer(str(data_file))
    patterns, samples, stats = analyzer.analyze_all()

    # Print summary
    print("\n" + "=" * 60)
    print("PATTERN ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total unique patterns: {stats['total_patterns']}")
    print("\nPatterns by type:")
    for pattern_name, info in stats["patterns_by_type"].items():
        print(f"  {pattern_name:25} {info['total']:5} occurrences")
        for author, count in info["by_author"].items():
            print(f"    - {author:20} {count:5}")

    print("\nSample code patterns:")
    for pattern_name, samples_list in samples.items():
        if samples_list:
            print(f"\n  {pattern_name}:")
            for i, sample in enumerate(samples_list[:3], 1):
                print(f"    {i}. [{sample['ref']}] {sample['line'][:70]}")

    # Export for rule generation
    analyzer.export_patterns()


if __name__ == "__main__":
    main()
