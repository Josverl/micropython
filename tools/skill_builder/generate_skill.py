#!/usr/bin/env python3
"""
Generate a GitHub Copilot SKILL.md file from extracted patterns.

This replaces the old generate_rules.py which created incorrect JSON/YAML formats.
A proper skill is a Markdown file with YAML frontmatter that provides natural
language instructions for the Copilot agent to follow.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Configuration
DATA_DIR = "data"
INPUT_FILE = os.path.join(DATA_DIR, "extracted_patterns.json")
OUTPUT_DIR = "../../.github/skills/micropython-c-code-review"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "SKILL.md")


def load_patterns() -> Dict[str, Any]:
    """Load extracted patterns from JSON file."""
    with open(INPUT_FILE, 'r') as f:
        return json.load(f)


def format_examples(examples: List[str], max_examples: int = 3) -> str:
    """Format code examples for markdown."""
    if not examples:
        return "   No examples available\n"
    
    result = ""
    for i, example in enumerate(examples[:max_examples], 1):
        # Clean up example
        example = example.strip()
        if example:
            result += f"   - `{example}`\n"
    
    return result


def generate_critical_safety_section(patterns: Dict) -> str:
    """Generate the critical safety checks section."""
    stats = patterns["statistics"]["patterns_by_type"]
    samples = patterns["samples"]
    
    section = """### 1. Critical Safety Checks

#### Memory Management (Priority: Critical)
Despite appearing in only 21 instances per 605 commits, memory issues are critical. Check:

1. **Allocation/Deallocation Pairing**
   - Every `m_new()` must have a corresponding `m_del()` in all code paths
   - Look for potential leaks in error paths
"""
    
    if "memory_allocation" in samples:
        section += "   - Examples from commits:\n"
        section += format_examples(samples["memory_allocation"][:3])
    
    section += """
2. **Error Path Cleanup**
   - Verify all exception/error paths free allocated memory
   - Check for leaks in early returns

3. **Buffer Allocation**
   - Confirm proper size calculations (avoid overflow)

#### Error Handling ({} occurrences)

1. **MP_ERROR_TEXT Usage**
   - Error messages MUST use `MP_ERROR_TEXT()` macro
   - Enables internationalization and memory optimization
""".format(stats["error_handling"]["total"] + stats.get("error_text_macro", {}).get("total", 0))
    
    if "error_text_macro" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["error_text_macro"][:3])
    
    section += """
2. **Error Checking Completeness**
   - All API calls that can fail must be checked
   - Don't silently ignore errors

3. **Appropriate Exception Types**
   - Use correct exception type (ValueError, TypeError, OSError, etc.)

#### Type Safety ({} occurrences - most common pattern)

1. **Explicit Casts**
   - Cast before operations that change type width
   - Prevent undefined behavior from implicit conversions

2. **Integer Type Consistency**
   - Use `mp_int_t`/`mp_uint_t` for VM integers
   - Use sized types (`int32_t`, `uint8_t`) for hardware values

3. **Pointer Type Safety**
   - Check pointer casts are valid
   - Verify alignment requirements

#### Boundary Checking ({} occurrences - security critical)

1. **Array Access**
   - Always validate indices before array access
   - Check both lower and upper bounds

2. **Buffer Operations**
   - Verify buffer size before read/write operations
   - Check for potential overflow in size calculations

3. **String Operations**
   - Validate string lengths
   - Ensure null termination where required

""".format(stats["type_safety"]["total"], stats["boundary_check"]["total"])
    
    return section


def generate_micropython_patterns_section(patterns: Dict) -> str:
    """Generate MicroPython-specific patterns section."""
    stats = patterns["statistics"]["patterns_by_type"]
    samples = patterns["samples"]
    
    section = """### 2. MicroPython-Specific Patterns

#### QSTR Usage ({} occurrences)

1. **QSTR Definition**
   - Use `MP_QSTR_*` constants for frequently used strings
   - Check qstr is registered in `qstrdefs.h` if new

2. **QSTR Performance**
   - QSTRs enable fast string comparison (pointer equality)
   - Prefer QSTR over C string literals for internal strings
""".format(stats["qstr_usage"]["total"])
    
    if "qstr_usage" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["qstr_usage"][:2])
    
    section += """
#### Object Creation ({} occurrences)

1. **Type-Specific Constructors**
   - Use correct `mp_obj_new_*()` function for type
   - Common constructors: `mp_obj_new_int()`, `mp_obj_new_str()`, `mp_obj_new_bytes()`

2. **Reference Management**
   - Understand object lifetime and GC implications
   - Don't hold raw pointers across potential GC points
""".format(stats["mp_obj_new"]["total"])
    
    if "mp_obj_new" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["mp_obj_new"][:3])
    
    section += """
#### ROM Tables ({} occurrences)

1. **MP_ROM_QSTR / MP_ROM_PTR**
   - Use ROM table macros for static data
   - Reduces RAM usage by placing data in read-only memory

2. **Table Termination**
   - Ensure tables are properly terminated
   - Check for correct sentinel values
""".format(stats["rom_table"]["total"])
    
    if "rom_table" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["rom_table"][:2])
    
    section += """
#### Function Arguments ({} occurrences)

1. **MP_ARG Parsing**
   - Use `mp_arg_parse_*()` functions for argument handling
   - Define argument specs with `MP_ARG_*` flags

2. **Argument Validation**
   - Check argument count with `mp_arg_check_num()`
   - Validate types and ranges
""".format(stats.get("mp_arg", {}).get("total", 0))
    
    if "mp_arg" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["mp_arg"][:2])
    
    return section


def generate_platform_compatibility_section(patterns: Dict) -> str:
    """Generate platform compatibility section."""
    stats = patterns["statistics"]["patterns_by_type"]
    samples = patterns["samples"]
    
    section = """### 3. Platform Compatibility

#### Configuration Guards ({} occurrences - critical for multi-platform)

1. **Feature Guards**
   - Wrap platform-specific code in `#if MICROPY_*` guards
   - Enables/disables features at compile time
""".format(stats["config_guard"]["total"])
    
    if "config_guard" in samples:
        section += "   - Examples:\n"
        section += format_examples(samples["config_guard"][:3])
    
    section += """
2. **Guard Consistency**
   - Match guard style with existing code
   - Ensure guards are correctly nested

3. **Feature Detection**
   - Check `MICROPY_*` macros are defined before use
   - Provide fallbacks where appropriate

"""
    
    return section


def generate_checklist_section(patterns: Dict) -> str:
    """Generate review checklist."""
    return """## Review Checklist

Use this checklist for every review:

- [ ] **Memory**: All allocations have matching deallocations
- [ ] **Errors**: All error messages use `MP_ERROR_TEXT()`
- [ ] **Types**: Explicit casts where type width changes
- [ ] **Bounds**: Array/buffer accesses are validated
- [ ] **Config**: Platform-specific code has `#if MICROPY_*` guards
- [ ] **QSTRs**: Internal strings use QSTR constants
- [ ] **Objects**: Use correct `mp_obj_new_*()` constructors
- [ ] **Tables**: ROM tables use `MP_ROM_*` macros
- [ ] **Args**: Function arguments use `mp_arg_*()` parsing
- [ ] **Streams**: Stream operations use `mp_stream_*()` functions

"""


def generate_priority_section(patterns: Dict) -> str:
    """Generate pattern priority section based on frequency."""
    stats = patterns["statistics"]["patterns_by_type"]
    
    # Sort by frequency
    sorted_patterns = sorted(
        stats.items(),
        key=lambda x: x[1]["total"],
        reverse=True
    )
    
    section = "## Priority by Frequency\n\n"
    section += "Pattern frequency analysis (from 605 commits, 281 PRs):\n\n"
    
    for i, (pattern, data) in enumerate(sorted_patterns[:10], 1):
        total = data["total"]
        pattern_name = pattern.replace("_", " ").title()
        section += f"{i}. **{pattern_name}** ({total:,}) - "
        
        # Add context based on pattern type
        if pattern == "type_safety":
            section += "Most common, critical for correctness\n"
        elif pattern == "boundary_check":
            section += "Security and stability\n"
        elif pattern == "qstr_usage":
            section += "MicroPython efficiency pattern\n"
        elif pattern == "config_guard":
            section += "Platform compatibility\n"
        elif pattern == "memory_allocation":
            section += "Rare but critical when present\n"
        else:
            section += "\n"
    
    section += "\nFocus review effort on high-frequency patterns first, but treat "
    section += "low-frequency critical patterns (memory allocation) with extra scrutiny.\n\n"
    
    return section


def generate_skill_md(patterns: Dict) -> str:
    """Generate complete SKILL.md content."""
    
    # YAML frontmatter
    content = """---
name: micropython-c-code-review
description: Comprehensive C code review guidelines for MicroPython contributions. Use when reviewing C code changes in MicroPython repositories, especially for pull requests or commits modifying core VM, runtime, ports, or extmod functionality.
---

# MicroPython C Code Review Guide

This skill provides comprehensive guidelines for reviewing C code contributions to MicroPython, based on analysis of 605 commits and 281 pull requests from 9 core maintainers.

## When to Use This Skill

Apply this skill when:
- Reviewing pull requests with C code changes in MicroPython
- Analyzing commits that modify `py/`, `extmod/`, `ports/`, or `shared/` directories
- Evaluating contributions to MicroPython's core VM, runtime, or port implementations
- Checking code for MicroPython-specific patterns and best practices

## Review Process

Follow these steps systematically when reviewing MicroPython C code:

"""
    
    # Add sections
    content += generate_critical_safety_section(patterns)
    content += generate_micropython_patterns_section(patterns)
    content += generate_platform_compatibility_section(patterns)
    content += generate_checklist_section(patterns)
    content += generate_priority_section(patterns)
    
    # Footer
    content += """## Additional Notes

- See `patterns-reference.json` for detailed statistics
- Pattern data updated: {}
- For questions or updates, see `tools/skill_builder/`
""".format(datetime.now().strftime("%Y-%m-%d"))
    
    return content


def main():
    """Main execution."""
    print("Generating GitHub Copilot SKILL.md...")
    
    # Load patterns
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run analyze_patterns.py first.")
        return 1
    
    patterns = load_patterns()
    
    # Generate skill content
    skill_content = generate_skill_md(patterns)
    
    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Write SKILL.md
    with open(OUTPUT_FILE, 'w') as f:
        f.write(skill_content)
    
    print(f"\n✅ Generated: {OUTPUT_FILE}")
    print(f"\nSkill structure:")
    print(f"  - Name: micropython-c-code-review")
    print(f"  - Location: {OUTPUT_DIR}/")
    print(f"  - Supporting files: patterns-reference.json, README.md")
    print(f"\nThe skill is now available to GitHub Copilot in this repository.")
    
    return 0


if __name__ == "__main__":
    exit(main())
