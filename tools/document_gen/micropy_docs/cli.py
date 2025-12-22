"""Command-line interface for MicroPython macro documentation generator."""

import argparse
import sys
from pathlib import Path

# Default root: 3 levels up from this module (micropy_docs -> document_gen -> tools -> root)
DEFAULT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
DEFAULT_DB_DIR = Path(__file__).parent.parent

# Supported macro prefixes (all stored in single database)
MACRO_PRESETS = {
    "MICROPY": {"prefix": "MICROPY_", "output_name": "macros_micropy.md"},
    "MP": {"prefix": "MP_", "output_name": "macros_mp.md"},
    "MBOOT": {"prefix": "MBOOT_", "output_name": "macros_mboot.md"},
    "MIMXRT": {"prefix": "MIMXRT_", "output_name": "macros_mimxrt.md"},
}


def get_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="micropy-docs",
        description="Generate documentation for MicroPython MICROPY_* and MP_* macros",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan codebase for MICROPY_* macros (default)
  python -m micropy_docs scan --root /path/to/micropython
  
  # Scan codebase for MP_* macros
  python -m micropy_docs scan --prefix MP
  
  # Generate markdown from existing database
  python -m micropy_docs render --db macros.db -o docs/macros.md
  
  # Enrich descriptions with AI
  python -m micropy_docs enrich --root /path/to/micropython
  
  # Full pipeline: scan, enrich, render
  python -m micropy_docs all --root /path/to/micropython
  
  # Full pipeline for MP_* macros
  python -m micropy_docs all --prefix MP
""",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan codebase for macros")
    scan_parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=DEFAULT_ROOT,
        help="Root directory of MicroPython repository (default: auto-detected)",
    )
    scan_parser.add_argument(
        "--db",
        "-d",
        type=Path,
        default=None,
        help="Path to SQLite database (default: auto based on prefix)",
    )
    scan_parser.add_argument(
        "--prefix",
        "-p",
        choices=list(MACRO_PRESETS.keys()),
        default="MICROPY",
        help="Macro prefix to scan for (default: MICROPY)",
    )
    scan_parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Process all known prefixes",
    )
    scan_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress output")

    # Render command
    render_parser = subparsers.add_parser("render", help="Generate markdown from database")
    render_parser.add_argument(
        "--db", "-d", type=Path, default=None, help="Path to SQLite database"
    )
    render_parser.add_argument(
        "--output", "-o", type=Path, default=None, help="Output markdown file (default: macros.md)"
    )
    render_parser.add_argument(
        "--prefix",
        "-p",
        choices=list(MACRO_PRESETS.keys()),
        default="MICROPY",
        help="Macro prefix for rendering (default: MICROPY)",
    )
    render_parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Process all known prefixes",
    )
    render_parser.add_argument(
        "--min-group-size",
        type=int,
        default=10,
        help="Minimum items for a category section (default: 10)",
    )
    render_parser.add_argument(
        "--root", "-r", type=Path, default=None, help="Root directory for output path resolution"
    )

    # Enrich command
    enrich_parser = subparsers.add_parser("enrich", help="Enrich descriptions using Azure OpenAI")
    enrich_parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=DEFAULT_ROOT,
        help="Root directory of MicroPython repository (default: auto-detected)",
    )
    enrich_parser.add_argument(
        "--db", "-d", type=Path, default=None, help="Path to SQLite database"
    )
    enrich_parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Batch size for parallel API calls (default: 20)",
    )
    enrich_parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress progress output"
    )

    # All command (full pipeline)
    all_parser = subparsers.add_parser("all", help="Run full pipeline: scan, enrich, render")
    all_parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=DEFAULT_ROOT,
        help="Root directory of MicroPython repository (default: auto-detected)",
    )
    all_parser.add_argument("--db", "-d", type=Path, default=None, help="Path to SQLite database")
    all_parser.add_argument("--output", "-o", type=Path, default=None, help="Output markdown file")
    all_parser.add_argument(
        "--prefix",
        "-p",
        choices=list(MACRO_PRESETS.keys()),
        default="MICROPY",
        help="Macro prefix to process (default: MICROPY)",
    )
    all_parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Process all known prefixes",
    )
    all_parser.add_argument(
        "--min-group-size",
        type=int,
        default=5,
        help="Minimum items for a category section (default: 5)",
    )
    all_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress output")

    return parser


def _get_prefixes(args) -> list:
    """Get list of prefixes to process based on args."""
    if getattr(args, "all", False):
        return list(MACRO_PRESETS.keys())
    return [args.prefix]


def cmd_scan(args) -> int:
    """Execute the scan command."""
    from .scanner import MacroScanner

    prefixes = _get_prefixes(args)
    root = args.root.resolve()
    db_path = args.db or (DEFAULT_DB_DIR / MacroScanner.DEFAULT_DB_NAME)

    for prefix_key in prefixes:
        preset = MACRO_PRESETS[prefix_key]
        if not args.quiet and len(prefixes) > 1:
            print(f"\n{'='*60}")
            print(f"Processing {prefix_key}...")
            print("=" * 60)

        scanner = MacroScanner(root, db_path, prefix=preset["prefix"])
        try:
            def_count, occ_count = scanner.scan(verbose=not args.quiet)
        finally:
            scanner.close()

    if not args.quiet:
        print(f"\nDatabase saved to: {db_path}")
    return 0


def cmd_render(args) -> int:
    """Execute the render command."""
    from .ai_enricher import AIEnricher
    from .renderer import MarkdownRenderer
    from .scanner import MacroScanner

    prefixes = _get_prefixes(args)
    db_path = (args.db or (DEFAULT_DB_DIR / MacroScanner.DEFAULT_DB_NAME)).resolve()
    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        return 1

    root = args.root.resolve() if args.root else db_path.parent.parent.parent

    for prefix_key in prefixes:
        preset = MACRO_PRESETS[prefix_key]
        if len(prefixes) > 1:
            print(f"\n{'='*60}")
            print(f"Rendering {prefix_key}...")
            print("=" * 60)

        output_path = args.output or (root / "docs" / "develop" / preset["output_name"])

        scanner = MacroScanner(root, db_path, prefix=preset["prefix"])
        try:
            summary = scanner.build_summary_with_ai()
            renderer = MarkdownRenderer(
                output_path, min_group_size=args.min_group_size, prefix=preset["prefix"]
            )

            # Generate group summaries using AI
            groups = renderer.collect_groups_for_summaries(summary)
            enricher = AIEnricher(root=root, db_path=db_path)
            try:
                group_summaries = enricher.generate_group_summaries(groups, verbose=True)
            finally:
                enricher.close()

            result_path = renderer.render(summary, group_summaries)
            print(f"Markdown saved to: {result_path}")
        finally:
            scanner.close()

    return 0


def cmd_enrich(args) -> int:
    """Execute the enrich command."""
    from .ai_enricher import AIEnricher
    from .scanner import MacroScanner

    root = args.root.resolve()
    db_path = args.db or (DEFAULT_DB_DIR / MacroScanner.DEFAULT_DB_NAME)

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        print("Run 'scan' command first to create the database.")
        return 1

    enricher = AIEnricher(
        root=root,
        db_path=db_path,
        batch_size=args.batch_size,
    )
    try:
        enricher.generate_missing_descriptions(verbose=not args.quiet)
        return 0
    finally:
        enricher.close()


def cmd_all(args) -> int:
    """Execute the full pipeline."""
    from .ai_enricher import AIEnricher
    from .renderer import MarkdownRenderer
    from .scanner import MacroScanner

    prefixes = _get_prefixes(args)
    root = args.root.resolve()
    db_path = args.db or (DEFAULT_DB_DIR / MacroScanner.DEFAULT_DB_NAME)
    verbose = not args.quiet

    for prefix_key in prefixes:
        preset = MACRO_PRESETS[prefix_key]
        output_path = args.output or (root / "docs" / "develop" / preset["output_name"])

        if len(prefixes) > 1 and verbose:
            print(f"\n{'#'*60}")
            print(f"# Processing {prefix_key}")
            print("#" * 60)

        # Step 1: Scan
        if verbose:
            print("=" * 60)
            print(f"Step 1: Scanning codebase for {preset['prefix']}* macros...")
            print("=" * 60)

        scanner = MacroScanner(root, db_path, prefix=preset["prefix"])
        try:
            scanner.scan(verbose=verbose)
        finally:
            scanner.close()

        # Step 2: Enrich
        if verbose:
            print("\n" + "=" * 60)
            print("Step 2: Enriching with AI...")
            print("=" * 60)

        enricher = AIEnricher(root=root, db_path=db_path)
        try:
            enricher.generate_missing_descriptions(verbose=verbose)

            # Generate group summaries
            scanner = MacroScanner(root, db_path, prefix=preset["prefix"])
            try:
                summary = scanner.build_summary_with_ai()
            finally:
                scanner.close()

            renderer = MarkdownRenderer(
                output_path,
                min_group_size=args.min_group_size,
                prefix=preset["prefix"],
            )
            groups = renderer.collect_groups_for_summaries(summary)
            group_summaries = enricher.generate_group_summaries(groups, verbose=verbose)
        finally:
            enricher.close()

        # Step 3: Render
        if verbose:
            print("\n" + "=" * 60)
            print("Step 3: Rendering markdown...")
            print("=" * 60)

        scanner = MacroScanner(root, db_path, prefix=preset["prefix"])
        try:
            summary = scanner.build_summary_with_ai()
        finally:
            scanner.close()

        renderer = MarkdownRenderer(
            output_path,
            min_group_size=args.min_group_size,
            prefix=preset["prefix"],
        )
        result_path = renderer.render(summary, group_summaries)

        if verbose:
            print(f"\nMarkdown saved to: {result_path}")

    return 0


def main(argv=None) -> int:
    """Main entry point."""
    parser = get_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    commands = {
        "scan": cmd_scan,
        "render": cmd_render,
        "enrich": cmd_enrich,
        "all": cmd_all,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
