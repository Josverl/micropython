#!/usr/bin/env python3
"""
Generate Copilot review skill rules from extracted patterns.

Creates JSON/YAML rule definitions that can be used in a Copilot
review skill to enforce MicroPython coding standards.
"""

import json
from pathlib import Path


class RuleGenerator:
    """Generates review rules from patterns."""

    DEFAULT_MIN_OCCURRENCES = 1
    MAX_AUTO_RULES = 50

    AUTO_RULE_TEMPLATES = {
        "mp_printf": {
            "id": "micropy-mp-printf",
            "category": "logging",
            "severity": "suggestion",
            "title": "Use mp_printf for diagnostics",
            "description": "Prefer mp_printf/mp_vprintf for diagnostic output to integrate with MicroPython's print backend.",
            "pattern": r"\bmp_(v)?printf\b",
        },
        "vstr_usage": {
            "id": "micropy-vstr-usage",
            "category": "memory_safety",
            "severity": "suggestion",
            "title": "Use vstr for dynamic string building",
            "description": "Use vstr_* helpers for incremental string construction to avoid repeated reallocations.",
            "pattern": r"\bvstr_(init|add|add_str|add_byte|add_char|add_len|printf)\b",
        },
        "const_fun_obj": {
            "id": "micropy-const-fun-obj",
            "category": "api_binding",
            "severity": "warning",
            "title": "Use MP_DEFINE_CONST_FUN_OBJ_* for function bindings",
            "description": "Expose C functions to Python using MP_DEFINE_CONST_FUN_OBJ_* macros for consistent bindings.",
            "pattern": r"\bMP_DEFINE_CONST_FUN_OBJ(_\d+)?\b",
        },
        "rom_table": {
            "id": "micropy-rom-table",
            "category": "memory_safety",
            "severity": "suggestion",
            "title": "Use MP_ROM_PTR/MP_ROM_QSTR for ROM tables",
            "description": "Store constant pointers and qstrs in ROM with MP_ROM_PTR/MP_ROM_QSTR to reduce RAM usage.",
            "pattern": r"\bMP_ROM_(PTR|QSTR)\b",
        },
        "mp_obj_new": {
            "id": "micropy-mp-obj-new",
            "category": "api_usage",
            "severity": "suggestion",
            "title": "Use mp_obj_new_* helpers",
            "description": "Create MicroPython objects using mp_obj_new_* helpers for consistent object construction.",
            "pattern": r"\bmp_obj_new_\w+\b",
        },
        "qstr_usage": {
            "id": "micropy-qstr-usage",
            "category": "memory_safety",
            "severity": "suggestion",
            "title": "Prefer qstr for interned strings",
            "description": "Use qstr (MP_QSTR_*) for interned strings to save memory and enable fast comparisons.",
            "pattern": r"\bMP_QSTR_\w+\b|\bqstr_\w+\b",
        },
        "mp_stream": {
            "id": "micropy-mp-stream",
            "category": "io",
            "severity": "suggestion",
            "title": "Use mp_stream_* for stream protocol",
            "description": "Use mp_stream_* helpers to implement stream protocol consistently across ports.",
            "pattern": r"\bmp_stream_\w+\b",
        },
        "mp_arg": {
            "id": "micropy-mp-arg",
            "category": "api_usage",
            "severity": "suggestion",
            "title": "Use mp_arg_* for argument parsing",
            "description": "Use mp_arg_* helpers for consistent argument parsing and validation.",
            "pattern": r"\bmp_arg_\w+\b|\bMP_ARG_\w+\b",
        },
    }

    # Predefined rules based on MicroPython best practices
    BASE_RULES = [
        {
            "id": "micropy-memory-allocation",
            "category": "memory_safety",
            "severity": "error",
            "title": "Use MicroPython memory allocation functions",
            "description": "Use m_new, m_renew, and m_del for memory management instead of malloc/free. "
            "This ensures consistent memory tracking and debugging.",
            "pattern": r"\b(malloc|calloc|realloc|free)\s*\(",
            "replacement_pattern": "m_new/m_renew/m_del",
            "examples": {
                "bad": "void *ptr = malloc(size);",
                "good": "mp_obj_t *ptr = m_new(mp_obj_t, size);",
            },
        },
        {
            "id": "micropy-error-handling",
            "category": "error_handling",
            "severity": "warning",
            "title": "Use mp_raise_* functions for exceptions",
            "description": "Raise MicroPython exceptions using mp_raise_* functions with proper error types. "
            "This ensures consistent exception handling across the codebase.",
            "pattern": r"\b(raise|throw|assert)\b",
            "reference": "mp_raise_ValueError, mp_raise_TypeError, mp_raise_NotImplementedError, etc.",
            "examples": {
                "bad": "if (!valid) assert(0);",
                "good": 'if (!valid) mp_raise_ValueError(MP_ERROR_TEXT("invalid value"));',
            },
        },
        {
            "id": "micropy-error-text-macro",
            "category": "error_handling",
            "severity": "warning",
            "title": "Use MP_ERROR_TEXT for error messages",
            "description": "Wrap error message strings with MP_ERROR_TEXT macro for proper handling "
            "of compile-time error text storage.",
            "pattern": r"mp_raise_\w+\s*\(\s*['\"]",
            "note": "Check that mp_raise_* calls use MP_ERROR_TEXT for string messages",
            "examples": {
                "bad": 'mp_raise_ValueError("invalid");',
                "good": 'mp_raise_ValueError(MP_ERROR_TEXT("invalid"));',
            },
        },
        {
            "id": "micropy-config-guard",
            "category": "configuration",
            "severity": "suggestion",
            "title": "Consider using configuration guards for optional features",
            "description": "Use #if MICROPY_* preprocessor guards for optional features to reduce "
            "binary size on constrained devices.",
            "pattern": r"#define\s+FEATURE_",
            "recommendation": "Wrap feature flags with #if MICROPY_* guards",
            "examples": {"pattern": "#if MICROPY_PY_FEATURE_NAME\n    // implementation\n#endif"},
        },
        {
            "id": "micropy-type-safety",
            "category": "type_safety",
            "severity": "warning",
            "title": "Use MicroPython type definitions",
            "description": "Use mp_obj_t, mp_int_t, size_t, and other MicroPython types for consistency "
            "and portability across platforms.",
            "proper_types": ["mp_obj_t", "mp_int_t", "mp_uint_t", "size_t", "uint32_t", "int32_t"],
            "examples": {
                "bad": "void process(int *data, int len) {}",
                "good": "void process(mp_obj_t *data, size_t len) {}",
            },
        },
        {
            "id": "micropy-encapsulation",
            "category": "code_style",
            "severity": "suggestion",
            "title": "Use static and const for encapsulation",
            "description": "Mark internal functions and data as static, and use const for immutable data "
            "to reduce namespace pollution and enable optimization.",
            "note": "Check that module-internal items are marked static",
        },
        {
            "id": "micropy-inline-docs",
            "category": "documentation",
            "severity": "suggestion",
            "title": "Add inline comments for non-obvious code",
            "description": "Include comments explaining intent for complex logic, memory optimizations, "
            "and MicroPython-specific decisions.",
            "note": "Check for documentation of optimization trade-offs",
        },
        {
            "id": "micropy-boundary-check",
            "category": "memory_safety",
            "severity": "error",
            "title": "Validate buffer boundaries and sizes",
            "description": "Always validate array bounds and buffer sizes to prevent buffer overflows "
            "on embedded systems with limited memory.",
            "note": "Check for boundary validation before array/buffer access",
        },
    ]

    def __init__(self, patterns_file=None):
        """Initialize rule generator."""
        self.patterns_file = patterns_file
        self.patterns = {}
        self.code_samples = {}
        self.statistics = {}
        if patterns_file and Path(patterns_file).exists():
            with open(patterns_file, "r") as f:
                data = json.load(f)
                self.patterns = data.get("patterns", {})
                self.statistics = data.get("statistics", {})
                self.code_samples = data.get("code_samples", {})

    def generate_rules(self):
        """Generate complete rule set."""
        rules = []

        for rule in self.BASE_RULES:
            enhanced_rule = self._enhance_rule(rule)
            rules.append(enhanced_rule)

        rules.extend(self._generate_auto_rules(rules))

        return rules

    def _generate_auto_rules(self, existing_rules):
        """Generate additional rules based on extracted patterns."""
        if not self.patterns:
            return []

        existing_ids = {rule.get("id") for rule in existing_rules}
        auto_rules = []

        # Template-based rules
        for pattern_name, author_counts in self.patterns.items():
            template = self.AUTO_RULE_TEMPLATES.get(pattern_name)
            if not template:
                continue

            total = sum(author_counts.values())
            if total < self.DEFAULT_MIN_OCCURRENCES:
                continue

            if template["id"] in existing_ids:
                continue

            rule = dict(template)
            rule["statistics"] = {"occurrences": total, "by_author": author_counts}

            samples = self.code_samples.get(pattern_name, [])
            if samples:
                rule["examples"] = {
                    "observed": "\n".join(s["line"] for s in samples[:3])
                }

            auto_rules.append(rule)

        # Generic rules for remaining patterns
        for pattern_name, author_counts in self.patterns.items():
            if len(auto_rules) >= self.MAX_AUTO_RULES:
                break

            if pattern_name in self.AUTO_RULE_TEMPLATES:
                continue

            total = sum(author_counts.values())
            if total < self.DEFAULT_MIN_OCCURRENCES:
                continue

            generic_id = f"micropy-auto-{pattern_name.replace('_', '-') }"
            if generic_id in existing_ids:
                continue

            samples = self.code_samples.get(pattern_name, [])
            rule = {
                "id": generic_id,
                "category": "auto",
                "severity": "suggestion",
                "title": f"Review pattern: {pattern_name.replace('_', ' ')}",
                "description": (
                    "This rule was auto-generated from observed code patterns. "
                    "Review usage for consistency with MicroPython practices."
                ),
                "statistics": {"occurrences": total, "by_author": author_counts},
            }

            if samples:
                rule["examples"] = {
                    "observed": "\n".join(s["line"] for s in samples[:3])
                }

            auto_rules.append(rule)

        return auto_rules[: self.MAX_AUTO_RULES]

    def _enhance_rule(self, rule):
        """Enhance a rule with statistics from patterns."""
        enhanced = dict(rule)

        # Add pattern statistics if available
        for pattern_name, author_counts in self.patterns.items():
            if pattern_name in rule.get("id", ""):
                total = sum(author_counts.values())
                enhanced["statistics"] = {"occurrences": total, "by_author": author_counts}
                break

        return enhanced

    def export_as_json(self, output_file=None):
        """Export rules as JSON."""
        if output_file is None:
            output_file = Path(__file__).parent / "data" / "review_rules.json"

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        rules = self.generate_rules()

        export_data = {
            "skill": {
                "name": "MicroPython C Code Review",
                "version": "1.0.0",
                "description": "Automated code review rules for MicroPython C code based on "
                "analysis of commits from core contributors",
                "target_language": "c",
                "rules": rules,
            }
        }

        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"Rules exported to JSON: {output_file}")
        return output_file

    def export_as_yaml(self, output_file=None):
        """Export rules as YAML (for GitHub Copilot extensions)."""
        if output_file is None:
            output_file = Path(__file__).parent / "data" / "review_rules.yaml"

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        rules = self.generate_rules()

        # Simple YAML generation without external dependency
        yaml_content = """# MicroPython C Code Review Skill
# Generated from analysis of core contributor commits and PRs

skill:
  name: MicroPython C Code Review
  version: "1.0.0"
  description: >
    Automated code review rules for MicroPython C code based on
    analysis of commits from core contributors.
  target_language: c
  
rules:
"""
        for rule in rules:
            yaml_content += f"\n  - id: {rule['id']}\n"
            yaml_content += f"    category: {rule.get('category', 'general')}\n"
            yaml_content += f"    severity: {rule.get('severity', 'suggestion')}\n"
            yaml_content += f"    title: {rule['title']}\n"
            yaml_content += f"    description: |\n"
            for line in rule["description"].split("\n"):
                yaml_content += f"      {line}\n"

            if "pattern" in rule:
                yaml_content += f"    pattern: '{rule['pattern']}'\n"

            if "examples" in rule:
                yaml_content += f"    examples:\n"
                for key, value in rule["examples"].items():
                    if isinstance(value, dict):
                        for ex_key, ex_val in value.items():
                            yaml_content += f"      {ex_key}: |\n"
                            yaml_content += f"        {ex_val}\n"
                    else:
                        yaml_content += f"      {key}: |\n"
                        yaml_content += f"        {value}\n"

        with open(output_file, "w") as f:
            f.write(yaml_content)

        print(f"Rules exported to YAML: {output_file}")
        return output_file

    def export_as_markdown(self, output_file=None):
        """Export rules as Markdown for documentation."""
        if output_file is None:
            output_file = Path(__file__).parent / "data" / "REVIEW_RULES.md"

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        rules = self.generate_rules()

        md_content = """# MicroPython C Code Review Rules

This document describes the automated code review rules for MicroPython C code.
These rules were derived from analysis of ~100 commits and PRs from core MicroPython
contributors.

## Rule Summary

| ID | Category | Severity | Title |
|----|----------|----------|-------|
"""

        for rule in rules:
            md_content += f"| `{rule['id']}` | {rule.get('category', 'general')} | "
            md_content += f"**{rule.get('severity', 'suggestion').upper()}** | {rule['title']} |\n"

        md_content += "\n## Detailed Rules\n"

        for rule in rules:
            md_content += f"\n### {rule['id']}\n\n"
            md_content += f"**Category:** {rule.get('category', 'general')}  \n"
            md_content += f"**Severity:** {rule.get('severity', 'suggestion').upper()}  \n\n"
            md_content += f"{rule['description']}\n\n"

            if "examples" in rule and isinstance(rule["examples"], dict):
                md_content += "**Examples:**\n\n"
                examples = rule["examples"]

                if "bad" in examples and "good" in examples:
                    md_content += "❌ **Bad:**\n```c\n"
                    md_content += f"{examples['bad']}\n```\n\n"
                    md_content += "✅ **Good:**\n```c\n"
                    md_content += f"{examples['good']}\n```\n"

        with open(output_file, "w") as f:
            f.write(md_content)

        print(f"Rules exported to Markdown: {output_file}")
        return output_file


def main():
    """Main entry point."""
    patterns_file = Path(__file__).parent / "data" / "extracted_patterns.json"

    if not patterns_file.exists():
        print(f"Warning: Patterns file not found at {patterns_file}")
        print("Proceeding with base rules only.")
        generator = RuleGenerator()
    else:
        generator = RuleGenerator(str(patterns_file))

    print("Generating review rules...\n")

    # Generate and export in multiple formats
    json_file = generator.export_as_json()
    yaml_file = generator.export_as_yaml()
    md_file = generator.export_as_markdown()

    print(f"\nGenerated {len(generator.generate_rules())} review rules")
    print(f"Output files:")
    print(f"  - JSON: {json_file}")
    print(f"  - YAML: {yaml_file}")
    print(f"  - Markdown: {md_file}")


if __name__ == "__main__":
    main()
