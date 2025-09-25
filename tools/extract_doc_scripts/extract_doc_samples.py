#!/usr/bin/env python3
r"""
MicroPython Documentation Sample Extractor

This tool extracts Python code samples from MicroPython RST documentation
and prepares them for testing with micropython-stubs.
"""

import os
import re
import ast
import argparse
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import yaml


@dataclass
class CodeSample:
    """Represents a code sample extracted from documentation"""

    content: str
    source_file: str
    line_number: int
    sample_type: str  # 'code_block', 'interactive'
    platform_context: Optional[str] = None
    has_syntax_error: bool = False
    syntax_error_message: Optional[str] = None
    is_fixed: bool = False
    fix_applied: Optional[str] = None


class DocSampleExtractor:
    """Extracts code samples from MicroPython documentation"""

    # Patterns to match different code block formats
    CODE_BLOCK_PATTERNS = [
        # Double colon blocks (most common in MicroPython docs) - Updated for better matching
        (
            re.compile(r"([^\n]*?)::\s*\n\n((?:    .*\n)*?)(?=\n  \w|\n\w|\Z)", re.MULTILINE),
            "code_block",
        ),
        # Standard RST code blocks - Fixed to capture complete blocks including blank lines
        (
            re.compile(
                r"\.\. code-block::\s*(?:python|pycon)?\s*\n\n((?:    .*\n|\s*\n)*?)\n(?=\S|\Z)",
                re.MULTILINE,
            ),
            "code_block",
        ),
        # Interactive Python sessions with >>>
        (
            re.compile(r"((?:^\s*>>>.*\n(?:\s*\.\.\..*\n)*(?:\s*[^>\s].*\n)*)*)", re.MULTILINE),
            "interactive",
        ),
    ]

    # Platform-specific keywords to identify samples
    PLATFORM_KEYWORDS = {
        "esp32": ["esp32", "ESP32", "wifi", "machine.Pin", "machine.ADC", "network"],
        "pyboard": ["pyboard", "Pyboard", "machine.Pin", "machine.ADC"],
        "rp2": ["rp2", "RP2", "Pico", "machine.Pin"],
        "unix": ["unix", "Unix", "micropython"],
    }

    def __init__(self, include_syntax_errors: bool = False):
        self.samples: List[CodeSample] = []
        self.include_syntax_errors = include_syntax_errors
        self.stats = {
            "total_files_processed": 0,
            "total_samples_found": 0,
            "valid_samples": 0,
            "syntax_errors": 0,
            "fixed_samples": 0,
            "platform_breakdown": {},
        }

    def extract_from_directory(self, docs_path: Path) -> List[CodeSample]:
        """Extract code samples from all RST files in directory"""
        rst_files = list(docs_path.rglob("*.rst"))
        print(f"Found {len(rst_files)} RST files to process")

        for rst_file in rst_files:
            self._process_file(rst_file)

        self.stats["total_files_processed"] = len(rst_files)
        return self.samples

    def _process_file(self, file_path: Path):
        """Process a single RST file"""
        # Skip index.rst files
        if file_path.name == "index.rst":
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Warning: Could not decode {file_path}")
            return

        # Get relative path from docs root for better folder structure
        try:
            # Find the docs directory in the path
            docs_path = None
            for parent in file_path.parents:
                if parent.name == "docs":
                    docs_path = parent
                    break

            if docs_path:
                relative_path = file_path.relative_to(docs_path)
            else:
                relative_path = Path(file_path.name)
        except ValueError:
            relative_path = Path(file_path.name)

        content_lines = content.split("\n")

        for pattern, sample_type in self.CODE_BLOCK_PATTERNS:
            for match in pattern.finditer(content):
                if sample_type == "code_block":
                    # For code blocks, the code is the second group
                    if len(match.groups()) >= 2:
                        # Check if this is an output block we should skip
                        intro_text = match.group(1)
                        if self._is_output_block(intro_text):
                            continue

                        code = match.group(2)
                    else:
                        continue
                else:
                    # For interactive sessions, the whole match is the code
                    code = match.group(0)

                if code and code.strip():
                    # Calculate line number where the match starts
                    line_number = content[: match.start()].count("\n") + 1

                    processed_code = self._process_code_block(code)
                    if processed_code:
                        sample = self._create_sample(
                            processed_code, relative_path, sample_type, line_number
                        )
                        if sample:
                            self.samples.append(sample)
                            self.stats["total_samples_found"] += 1

    def _process_code_block(self, raw_code: str) -> Optional[str]:
        """Process and clean raw code block"""
        if not raw_code or not raw_code.strip():
            return None

        lines = raw_code.split("\n")

        # Remove common leading whitespace (typically 4 spaces from RST)
        if lines and lines[0].strip() == "":
            lines = lines[1:]  # Remove leading empty line

        # Find minimum indentation (ignoring empty lines)
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return None

        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)

        # Remove the common indentation
        cleaned_lines = []
        for line in lines:
            if line.strip():  # Non-empty line
                cleaned_lines.append(line[min_indent:] if len(line) > min_indent else line)
            else:  # Empty line
                cleaned_lines.append("")

        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()

        return "\n".join(cleaned_lines)

    def _create_sample(
        self, code: str, source_file: Path, sample_type: str, line_number: int
    ) -> Optional[CodeSample]:
        """Create a CodeSample object with validation"""
        if not code.strip():
            return None

        # Detect platform context
        platform = self._detect_platform(code)

        # Validate syntax
        is_valid, error_msg = self._validate_python_syntax(code)

        sample = CodeSample(
            content=code,
            source_file=str(source_file),
            line_number=line_number,
            sample_type=sample_type,
            platform_context=platform,
            has_syntax_error=not is_valid,
            syntax_error_message=error_msg,
        )

        if not is_valid:
            self.stats["syntax_errors"] += 1

            if self.include_syntax_errors:
                # Try to fix syntax errors
                fixed_code = self._try_fix_syntax_errors(code)
                if fixed_code:
                    # Validate the fixed code
                    fixed_valid, _ = self._validate_python_syntax(fixed_code)
                    if fixed_valid:
                        sample.content = fixed_code
                        sample.is_fixed = True
                        sample.fix_applied = (
                            "Applied automatic fixes for documentation placeholders"
                        )
                        sample.has_syntax_error = False
                        self.stats["fixed_samples"] += 1
                        is_valid = True

            if not is_valid and not self.include_syntax_errors:
                return None  # Skip samples with syntax errors unless explicitly requested

        if is_valid or (self.include_syntax_errors and sample.is_fixed):
            self.stats["valid_samples"] += 1

        # Update platform stats
        platform_key = platform or "generic"
        self.stats["platform_breakdown"][platform_key] = (
            self.stats["platform_breakdown"].get(platform_key, 0) + 1
        )

        return sample

    def _is_output_block(self, intro_text: str) -> bool:
        """Check if this is an output/result block that should be skipped"""
        intro_lower = intro_text.lower().strip()

        # Common patterns for output/result blocks
        output_indicators = ["output is", "result is", "returns", "prints", "displays", "shows"]

        return any(indicator in intro_lower for indicator in output_indicators)

    def _detect_platform(self, code: str) -> Optional[str]:
        """Detect platform context from code content"""
        for platform, keywords in self.PLATFORM_KEYWORDS.items():
            if any(keyword in code for keyword in keywords):
                return platform
        return None

    def _validate_python_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax using AST"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Parsing error: {str(e)}"

    def _try_fix_syntax_errors(self, code: str) -> Optional[str]:
        """Attempt to fix common syntax errors in documentation code"""
        fixed_code = code

        # Apply various fixes
        fixed_code = self._fix_ellipsis_placeholders(fixed_code)
        fixed_code = self._fix_pseudo_placeholders(fixed_code)
        fixed_code = self._fix_indentation_issues(fixed_code)

        # Check if our fixes worked
        is_valid, _ = self._validate_python_syntax(fixed_code)
        return fixed_code if is_valid else None

    def _fix_ellipsis_placeholders(self, code: str) -> str:
        """Replace ellipsis placeholders with pass statements"""
        # Handle standalone ... on their own lines
        code = re.sub(r"^(\s*)\.\.\.(\s*)$", r"\1pass\2", code, flags=re.MULTILINE)

        # Handle ... in expressions (replace with None)
        code = re.sub(r"\.\.\.(?=\s*[,\)\]\}])", "None", code)

        return code

    def _fix_pseudo_placeholders(self, code: str) -> str:
        """Fix common undefined variables in documentation"""
        undefined_vars = {
            "PIN_MDC": "5",
            "PIN_MDIO": "23",
            "PIN_PHY_POWER": "12",
            "PIN_CLK": "18",
            "PIN_DATA": "19",
            "CHANNEL": "1",
            "FREQ": "440",
            "your_wifi_ssid": '"MyWifi"',
            "your_wifi_password": '"password123"',
            "YOUR_NETWORK": '"192.168.1"',
        }

        for var, replacement in undefined_vars.items():
            # Replace variable assignments
            code = re.sub(rf"\b{re.escape(var)}\b", replacement, code)

        return code

    def _fix_indentation_issues(self, code: str) -> str:
        """Fix basic indentation problems"""
        lines = code.split("\n")

        # Fix mixed tabs/spaces (convert tabs to 4 spaces)
        lines = [line.expandtabs(4) for line in lines]

        return "\n".join(lines)

    def save_samples(self, output_dir: Path, output_format: str = "files"):
        """Save extracted samples to disk"""
        output_dir.mkdir(parents=True, exist_ok=True)

        if output_format == "files":
            self._save_as_files(output_dir)
        elif output_format == "yaml":
            self._save_as_yaml(output_dir)
        elif output_format == "json":
            self._save_as_json(output_dir)

    def _save_as_files(self, output_dir: Path):
        """Save each sample as a separate Python file in organized folder structure"""
        for i, sample in enumerate(self.samples):
            # Parse the source file path to create folder structure
            source_path = Path(sample.source_file)
            content_hash = hashlib.md5(sample.content.encode()).hexdigest()[:8]

            # Create folder structure based on source path
            if len(source_path.parts) > 1:
                # Remove .rst extension and create folder path
                # e.g., library/machine.rst -> library/machine/
                folder_parts = list(source_path.parts[:-1])  # Remove filename
                file_stem = source_path.stem  # filename without .rst
                folder_parts.append(file_stem)
                folder_path = Path(*folder_parts)
            else:
                # Single file, just use the stem as folder
                folder_path = Path(source_path.stem)

            # Create the target directory
            target_dir = output_dir / folder_path
            target_dir.mkdir(parents=True, exist_ok=True)

            # Create filename with line number and hash
            # e.g., machine_0092_985dee80.py or UART_0113_abc12345.py
            line_num_str = f"{sample.line_number:04d}"
            if "." in source_path.stem:
                # Handle files like machine.UART.rst -> UART_0113_hash.py
                base_name = source_path.stem.split(".")[-1]
            else:
                base_name = source_path.stem

            filename = f"{base_name}_{line_num_str}_{content_hash}.py"
            file_path = target_dir / filename

            with open(file_path, "w", encoding="utf-8") as f:
                # Add metadata as comments
                f.write(f"# Source: {sample.source_file}:{sample.line_number}\n")
                f.write(f"# Type: {sample.sample_type}\n")
                if sample.platform_context:
                    f.write(f"# Platform: {sample.platform_context}\n")
                if sample.is_fixed:
                    f.write(f"# Fixed: {sample.fix_applied}\n")
                f.write("\n")
                f.write(sample.content)
                if not sample.content.endswith("\n"):
                    f.write("\n")

    def _save_as_yaml(self, output_dir: Path):
        """Save all samples as YAML"""
        yaml_data = [asdict(sample) for sample in self.samples]
        with open(output_dir / "samples.yaml", "w") as f:
            yaml.dump(yaml_data, f, default_flow_style=False)

    def _save_as_json(self, output_dir: Path):
        """Save all samples as JSON"""
        json_data = [asdict(sample) for sample in self.samples]
        with open(output_dir / "samples.json", "w") as f:
            json.dump(json_data, f, indent=2)

    def print_stats(self):
        """Print extraction statistics"""
        print("\n" + "=" * 50)
        print("EXTRACTION STATISTICS")
        print("=" * 50)
        print(f"Files processed: {self.stats['total_files_processed']}")
        print(f"Total samples found: {self.stats['total_samples_found']}")
        print(f"Valid samples extracted: {self.stats['valid_samples']}")
        print(f"Samples with syntax errors: {self.stats['syntax_errors']}")
        if self.include_syntax_errors:
            print(f"Syntax errors fixed: {self.stats['fixed_samples']}")
            print(
                f"Unfixable syntax errors: {self.stats['syntax_errors'] - self.stats['fixed_samples']}"
            )

        print(f"\nPlatform breakdown:")
        for platform, count in sorted(self.stats["platform_breakdown"].items()):
            print(f"  {platform}: {count}")
        print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Extract code samples from MicroPython docs")
    parser.add_argument("docs_path", help="Path to MicroPython docs directory")
    parser.add_argument("--output", "-o", default="doc_samples", help="Output directory")
    parser.add_argument(
        "--format", choices=["files", "yaml", "json"], default="files", help="Output format"
    )
    parser.add_argument("--stats", action="store_true", help="Show extraction statistics")
    parser.add_argument("--platform", help="Only extract samples for specific platform")
    parser.add_argument(
        "--include-syntax-errors",
        action="store_true",
        help="Include samples with syntax errors (with fixes and comments)",
    )

    args = parser.parse_args()

    docs_path = Path(args.docs_path)
    if not docs_path.exists():
        print(f"Error: Documentation path {docs_path} does not exist")
        return 1

    print(f"Extracting code samples from: {docs_path}")
    print(f"Output directory: {args.output}")
    print(f"Output format: {args.format}")
    if args.include_syntax_errors:
        print("Including syntax error samples with automatic fixes")

    extractor = DocSampleExtractor(include_syntax_errors=args.include_syntax_errors)
    samples = extractor.extract_from_directory(docs_path)

    # Filter by platform if specified
    if args.platform:
        samples = [s for s in samples if s.platform_context == args.platform]
        print(f"Filtered to {args.platform} platform: {len(samples)} samples")

    if samples:
        output_path = Path(args.output)
        extractor.save_samples(output_path, args.format)
        print(f"Saved {len(samples)} samples to {output_path}")
    else:
        print("No valid code samples found")

    if args.stats:
        extractor.print_stats()

    return 0


if __name__ == "__main__":
    exit(main())
