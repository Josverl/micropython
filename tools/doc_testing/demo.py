#!/usr/bin/env python3
"""
Demo script showing the complete MicroPython documentation sample testing workflow
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show the result"""
    print(f"\n=== {description} ===")
    print(f"Running: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=".")
        print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    print("MicroPython Documentation Sample Testing Demo")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("docs").exists() or not Path("tools/doc_testing").exists():
        print("Error: Please run this script from the MicroPython root directory")
        print("Expected structure:")
        print("  docs/")
        print("  tools/doc_testing/")
        sys.exit(1)
    
    # Step 1: Extract samples
    success = run_command(
        "python tools/doc_testing/extract_doc_samples.py docs/library --output demo_samples --stats",
        "Extracting code samples from documentation"
    )
    
    if not success:
        print("Failed to extract samples")
        return
    
    # Step 2: Show what was extracted
    run_command(
        "find demo_samples -name '*.py' | head -10" if os.name != 'nt' else "dir demo_samples\\*.py | findstr /C:\".py\"",
        "Sample files extracted"
    )
    
    # Step 3: Basic syntax check
    run_command(
        "python -c \"import ast; [ast.parse(open(f).read()) for f in __import__('glob').glob('demo_samples/*.py')[:5]]; print('✓ Syntax checks passed for first 5 samples')\"",
        "Basic syntax validation"
    )
    
    # Step 4: Show sample content
    sample_files = list(Path("demo_samples").glob("*.py"))
    if sample_files:
        print(f"\n=== Sample Content (first file: {sample_files[0].name}) ===")
        with open(sample_files[0], 'r') as f:
            print(f.read())
    
    # Step 5: Statistics
    run_command(
        f"python -c \"import pathlib; samples = list(pathlib.Path('demo_samples').glob('*.py')); print(f'Total samples: {{len(samples)}}'); platforms = set(); [platforms.add(p.name.split('_')[0]) for p in samples if '_' in p.name]; print(f'Platforms found: {{sorted(platforms)}}')\"",
        "Sample statistics"
    )
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nNext steps:")
    print("1. Install micropython-stubs: git clone https://github.com/josverl/micropython-stubs.git")
    print("2. Run full tests: make test-samples (after running 'make setup')")
    print("3. Set up CI: The GitHub Actions workflow is ready in .github/workflows/")
    print("4. Customize: Edit tools/doc_testing/extract_doc_samples.py for your needs")

if __name__ == "__main__":
    main()