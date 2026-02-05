#!/usr/bin/env python3
"""
Test and validate the generated review skill rules.

Applies rules to sample code and tests against real MicroPython commits.
"""

import json
import re
from pathlib import Path


class RuleValidator:
    """Validates review rules against code samples."""

    def __init__(self, rules_file=None):
        """Load rules from JSON file."""
        self.rules = []
        if rules_file and Path(rules_file).exists():
            with open(rules_file, "r") as f:
                data = json.load(f)
                self.rules = data.get("skill", {}).get("rules", [])

    def validate_code(self, code, filename="test.c"):
        """Validate code against all rules."""
        findings = []

        for rule in self.rules:
            if "pattern" in rule:
                matches = self._find_pattern_matches(code, rule)
                for match in matches:
                    findings.append(
                        {
                            "rule_id": rule["id"],
                            "category": rule.get("category", "general"),
                            "severity": rule.get("severity", "suggestion"),
                            "title": rule["title"],
                            "line": match["line"],
                            "match": match["text"],
                            "description": rule["description"],
                        }
                    )

        return findings

    def _find_pattern_matches(self, code, rule):
        """Find matches for a rule's pattern."""
        matches = []
        pattern = rule.get("pattern", "")

        if not pattern:
            return matches

        try:
            regex = re.compile(pattern, re.MULTILINE | re.IGNORECASE)
            for line_num, line in enumerate(code.split("\n"), 1):
                match = regex.search(line)
                if match:
                    matches.append({"line": line_num, "text": line.strip()})
        except re.error as e:
            print(f"Warning: Invalid regex in rule {rule['id']}: {e}")

        return matches

    def test_samples(self):
        """Test rules with predefined code samples."""
        test_cases = [
            {
                "name": "Memory allocation with malloc",
                "code": "void *ptr = malloc(100);",
                "should_trigger": "micropy-memory-allocation",
            },
            {
                "name": "Correct m_new usage",
                "code": "mp_obj_t *ptr = m_new(mp_obj_t, 100);",
                "should_trigger": None,  # Should NOT trigger
            },
            {
                "name": "Raise error without MP_ERROR_TEXT",
                "code": 'mp_raise_ValueError("error");',
                "should_trigger": "micropy-error-text-macro",
            },
            {
                "name": "Correct error raising",
                "code": 'mp_raise_ValueError(MP_ERROR_TEXT("error"));',
                "should_trigger": None,  # Should NOT trigger
            },
            {
                "name": "Config guard usage",
                "code": "#if MICROPY_PY_FEATURE",
                "should_trigger": "micropy-config-guard",
            },
            {
                "name": "Type safety with int",
                "code": "void process(int *data, int len) {}",
                "should_trigger": "micropy-type-safety",
            },
            {
                "name": "Boundary check present",
                "code": "if (index < size) { data[index] = value; }",
                "should_trigger": "micropy-boundary-check",
            },
        ]

        print("\n" + "=" * 70)
        print("RULE VALIDATION - TESTING WITH SAMPLE CODE")
        print("=" * 70)

        results = {"passed": 0, "failed": 0}

        for test_case in test_cases:
            findings = self.validate_code(test_case["code"])
            triggered_rules = [f["rule_id"] for f in findings]

            expected = test_case.get("should_trigger")
            passed = False

            if expected is None:
                # Should NOT trigger any rule
                passed = len(findings) == 0
            else:
                # Should trigger specific rule
                passed = expected in triggered_rules

            status = "✓ PASS" if passed else "✗ FAIL"
            results["passed" if passed else "failed"] += 1

            print(f"\n{status}: {test_case['name']}")
            print(f"  Code: {test_case['code']}")
            print(f"  Expected: {expected or 'No triggers'}")
            print(f"  Got: {', '.join(triggered_rules) if triggered_rules else 'No triggers'}")

        print("\n" + "=" * 70)
        print(f"Test Results: {results['passed']} passed, {results['failed']} failed")
        print("=" * 70)

        return results

    def test_real_commits(self, data_file=None):
        """Test rules against real MicroPython commits."""
        if not data_file:
            data_file = Path(__file__).parent / "data" / "micropython_analysis_data.json"

        if not Path(data_file).exists():
            print(f"\nWarning: Data file not found: {data_file}")
            print("Cannot test against real commits.")
            return None

        print("\n" + "=" * 70)
        print("RULE VALIDATION - TESTING WITH REAL COMMITS")
        print("=" * 70)

        with open(data_file, "r") as f:
            data = json.load(f)

        stats = {
            "total_files": 0,
            "files_with_issues": 0,
            "total_issues": 0,
            "by_severity": {"error": 0, "warning": 0, "suggestion": 0},
            "by_rule": {},
        }

        # Test commits
        for author, commits in data.get("commits", {}).items():
            for commit in commits[:3]:  # Test first 3 commits per author
                for file_info in commit.get("files", []):
                    if not file_info["filename"].endswith(".c"):
                        continue

                    stats["total_files"] += 1
                    patch = file_info.get("patch", "")

                    # Extract added lines only
                    added_code = "\n".join(
                        line[1:]
                        for line in patch.split("\n")
                        if line.startswith("+") and not line.startswith("+++")
                    )

                    findings = self.validate_code(added_code, file_info["filename"])

                    if findings:
                        stats["files_with_issues"] += 1
                        stats["total_issues"] += len(findings)

                        for finding in findings:
                            severity = finding["severity"]
                            stats["by_severity"][severity] = (
                                stats["by_severity"].get(severity, 0) + 1
                            )

                            rule_id = finding["rule_id"]
                            stats["by_rule"][rule_id] = stats["by_rule"].get(rule_id, 0) + 1

        print(f"\nAnalyzed {stats['total_files']} C files from real commits")
        print(f"Files with issues: {stats['files_with_issues']}")
        print(f"Total issues found: {stats['total_issues']}")
        print(f"\nBy severity:")
        for severity in ["error", "warning", "suggestion"]:
            count = stats["by_severity"].get(severity, 0)
            print(f"  {severity:10} {count:5}")
        print(f"\nTop rules triggered:")
        for rule_id, count in sorted(stats["by_rule"].items(), key=lambda x: -x[1])[:5]:
            print(f"  {rule_id:30} {count:5}")

        return stats


def main():
    """Main entry point."""
    rules_file = Path(__file__).parent / "data" / "review_rules.json"

    if not rules_file.exists():
        print(f"Error: Rules file not found at {rules_file}")
        print("Run generate_rules.py first to generate the rules.")
        return

    validator = RuleValidator(str(rules_file))

    # Run sample tests
    sample_results = validator.test_samples()

    # Run real commit tests
    commit_results = validator.test_real_commits()

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(
        f"Sample Tests:    {sample_results['passed']}/{sample_results['passed'] + sample_results['failed']} passed"
    )
    if commit_results:
        print(
            f"Real Commits:    {commit_results['files_with_issues']} files with {commit_results['total_issues']} issues"
        )
    print("\nAll validation complete!")


if __name__ == "__main__":
    main()
