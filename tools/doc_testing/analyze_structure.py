#!/usr/bin/env python3
"""
Organized Sample Structure Summary

This script provides information about the organized folder structure
created by the MicroPython documentation sample extractor.
"""

from pathlib import Path
import argparse


def analyze_structure(samples_dir: Path):
    """Analyze and display the organized sample structure"""
    if not samples_dir.exists():
        print(f"Samples directory {samples_dir} does not exist")
        return
    
    print(f"📁 Sample Structure Analysis: {samples_dir}")
    print("=" * 60)
    
    total_files = 0
    folders_by_depth = {}
    
    for path in samples_dir.rglob('*.py'):
        total_files += 1
        depth = len(path.relative_to(samples_dir).parts) - 1
        folders_by_depth[depth] = folders_by_depth.get(depth, 0) + 1
    
    print(f"📊 Total Python files: {total_files}")
    print(f"📊 Folder depth distribution:")
    for depth, count in sorted(folders_by_depth.items()):
        print(f"   Level {depth}: {count} files")
    print()
    
    # Show top-level categories
    print("📂 Top-level categories:")
    top_level_dirs = [d for d in samples_dir.iterdir() if d.is_dir()]
    for directory in sorted(top_level_dirs):
        file_count = len(list(directory.rglob('*.py')))
        print(f"   {directory.name}/  ({file_count} samples)")
    print()
    
    # Show specific examples
    print("🔍 Example file structure:")
    examples = [
        "library/machine/machine_0092_*.py",
        "library/machine.UART/UART_0113_*.py", 
        "pyboard/tutorial/accel/accel_0024_*.py",
        "esp32/quickref/quickref_0038_*.py"
    ]
    
    for pattern in examples:
        matches = list(samples_dir.glob(pattern))
        if matches:
            example_file = matches[0]
            rel_path = example_file.relative_to(samples_dir)
            print(f"   ✓ {rel_path}")
        else:
            print(f"   ✗ {pattern} (not found)")
    print()
    
    print("📋 File naming convention:")
    print("   <module>_<line_number>_<hash>.py")
    print("   - module: from source filename")
    print("   - line_number: 4-digit padded line number") 
    print("   - hash: 8-character content hash")
    print()
    
    print("🗂️ Folder structure rules:")
    print("   • library/machine.rst → library/machine/")
    print("   • library/machine.UART.rst → library/machine.UART/")  
    print("   • pyboard/tutorial/accel.rst → pyboard/tutorial/accel/")
    print("   • docs/esp32/quickref.rst → esp32/quickref/")


def show_sample_content(samples_dir: Path, pattern: str):
    """Show content of matching samples"""
    matches = list(samples_dir.glob(pattern))
    if not matches:
        print(f"No samples found matching: {pattern}")
        return
        
    for sample_file in matches[:3]:  # Show first 3 matches
        print(f"\n📄 {sample_file.relative_to(samples_dir)}")
        print("-" * 50)
        with open(sample_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Show first few metadata lines and first few code lines
            for i, line in enumerate(lines[:10]):
                print(f"{i+1:2}: {line.rstrip()}")
        if len(lines) > 10:
            print(f"... (+{len(lines)-10} more lines)")


def main():
    parser = argparse.ArgumentParser(description='Analyze organized sample structure')
    parser.add_argument('--samples-dir', default='organized_samples', 
                       help='Path to organized samples directory')
    parser.add_argument('--show-sample', 
                       help='Show content of samples matching pattern (e.g., "**/machine/*.py")')
    
    args = parser.parse_args()
    samples_dir = Path(args.samples_dir)
    
    if args.show_sample:
        show_sample_content(samples_dir, args.show_sample)
    else:
        analyze_structure(samples_dir)


if __name__ == '__main__':
    main()