#!/usr/bin/env python3
"""
Verify the skill builder installation and readiness.
"""

import sys
from pathlib import Path


def check_files():
    """Verify all required files are present."""
    script_dir = Path(__file__).parent

    required_files = [
        "__init__.py",
        "main.py",
        "fetch_commits.py",
        "analyze_patterns.py",
        "generate_rules.py",
        "test_skill.py",
        "quickstart.py",
        "requirements.txt",
        "README.md",
        "IMPLEMENTATION_GUIDE.md",
        "QUICKREF.md",
        "setup.sh",
    ]

    print("Checking required files...")
    all_present = True
    for fname in required_files:
        fpath = script_dir / fname
        status = "✓" if fpath.exists() else "✗"
        size = f"({fpath.stat().st_size:,} bytes)" if fpath.exists() else ""
        print(f"  {status} {fname:30} {size}")
        if not fpath.exists():
            all_present = False

    return all_present


def check_dependencies():
    """Check if required packages are available."""
    print("\nChecking Python dependencies...")

    required_packages = [
        ("github", "PyGithub"),
        ("git", "GitPython"),
        ("requests", "requests"),
        ("dateutil", "python-dateutil"),
    ]

    all_installed = True
    for import_name, display_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✓ {display_name:20} installed")
        except ImportError:
            print(f"  ✗ {display_name:20} NOT installed")
            all_installed = False

    if not all_installed:
        print("\n  Install with: pip install -r requirements.txt")

    return all_installed


def check_python_version():
    """Check Python version."""
    print("\nChecking Python version...")
    version_info = sys.version_info
    version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    if version_info >= (3, 7):
        print(f"  ✓ Python {version_string} (required: 3.7+)")
        return True
    else:
        print(f"  ✗ Python {version_string} (required: 3.7+)")
        return False


def check_data_directory():
    """Check if data directory can be created."""
    print("\nChecking data directory...")
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Data directory ready: {data_dir}")
        return True
    except Exception as e:
        print(f"  ✗ Cannot create data directory: {e}")
        return False


def main():
    """Run all checks."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  MicroPython Skill Builder - Verification                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    checks = [
        ("Files", check_files),
        ("Python Version", check_python_version),
        ("Data Directory", check_data_directory),
        ("Dependencies", check_dependencies),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error during {name} check: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print(f"\nTotal: {passed}/{total} checks passed")

    if passed == total:
        print("\n✅ All checks passed! You're ready to use the skill builder.")
        print("\nNext steps:")
        print("  1. Set up dependencies (if needed):")
        print("     pip install -r requirements.txt")
        print("\n  2. Run the skill builder:")
        print("     python3 main.py --all")
        print("\n  3. Or use the interactive setup:")
        print("     python3 quickstart.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Upgrade Python: python3 --version (need 3.7+)")
        print("  - Check disk space: df -h")
        return 1


if __name__ == "__main__":
    sys.exit(main())
