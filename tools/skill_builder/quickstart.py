#!/usr/bin/env python3
"""
Quick start script for the MicroPython Skill Builder.

This script provides interactive guidance for running the skill builder pipeline.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header():
    """Print welcome header."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   MicroPython C Code Review Skill Builder                    ║
║                                                                              ║
║  Analyze commits from core MicroPython contributors and generate automated  ║
║  code review rules for enforcing best practices.                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def check_dependencies():
    """Check if required packages are installed."""
    print("Checking dependencies...")

    required = ["github", "git"]
    missing = []

    for package in required:
        try:
            if package == "github":
                import github
            elif package == "git":
                import git
        except ImportError:
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install -r requirements.txt")
        return False

    print("✓ All dependencies available\n")
    return True


def get_github_token():
    """Get or prompt for GitHub token."""
    token = os.environ.get("GITHUB_TOKEN")

    if token:
        print("✓ GitHub token found in GITHUB_TOKEN environment variable")
        return token

    print("\n⚠️  No GitHub token found.")
    print("\nWithout a token, you'll be limited to 60 API requests per hour.")
    print("With a token, you can make 5000 requests per hour.")
    print("\nGet a token at: https://github.com/settings/tokens")
    print("(Create a new token with 'public_repo' scope)")

    response = input("\nDo you want to proceed? (y/n): ").strip().lower()
    return None if response != "y" else ""


def run_pipeline(token_arg):
    """Run the skill builder pipeline."""
    script_dir = Path(__file__).parent

    print("\n" + "=" * 70)
    print("Running MicroPython Skill Builder Pipeline")
    print("=" * 70)

    # Build command
    cmd = ["python3", str(script_dir / "main.py"), "--all"]

    if token_arg:
        cmd.extend(["--github-token", token_arg])

    # Run pipeline
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Pipeline completed successfully!")
        print_next_steps(script_dir)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Pipeline failed with error code: {e.returncode}")
        sys.exit(1)


def print_next_steps(script_dir):
    """Print next steps after successful run."""
    data_dir = script_dir / "data"

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)

    print("\n1. Review the generated rules:")
    print(f"   cat {data_dir}/REVIEW_RULES.md")

    print("\n2. Test the rules with sample code:")
    print(f"   python3 {script_dir}/test_skill.py")

    print("\n3. View the generated artifacts:")
    print(f"   ls -la {data_dir}/")

    print("\n4. Integrate with your code review process:")
    print(f"   - Use review_rules.json with Copilot extensions")
    print(f"   - Use review_rules.yaml with GitHub Actions")
    print(f"   - Reference REVIEW_RULES.md in your documentation")

    print("\nGenerated files:")
    for file in sorted(data_dir.glob("*")):
        if file.is_file():
            size = file.stat().st_size
            print(f"   - {file.name:30} ({size:,} bytes)")

    print()


def main():
    """Main entry point."""
    print_header()

    # Check dependencies
    if not check_dependencies():
        print("Please install dependencies and try again.")
        sys.exit(1)

    # Get GitHub token
    token = get_github_token()

    if token is None:
        print("\nAborted.")
        sys.exit(0)

    # Run pipeline
    run_pipeline(token)


if __name__ == "__main__":
    main()
