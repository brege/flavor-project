#!/usr/bin/env python
"""
Flavor Project Pipeline
Runs the complete data processing pipeline to generate flavor network outputs.

Usage:
    python main.py
"""

import subprocess
import sys

def run_step(script, args):
    """Run a pipeline step."""
    print(f"\nRunning {script}...")
    result = subprocess.run([sys.executable, script] + args, check=False)
    return result.returncode == 0

def main():
    print("=" * 50)
    print("FLAVOR PROJECT PIPELINE")
    print("=" * 50)

    steps = [
        ("parse.py", [], "Parse HTML chapters"),
        ("clean.py", ["output/bible.json", "output/clean.json"], "Clean and normalize data"),
        ("similarity.py", ["-i", "output/clean.json", "-o", "output/similarity.json"], "Compute similarity matrix"),
        ("graph.py", ["output/clean.json", "output/edges.json", "output/nodes.json"], "Create network graph"),
    ]

    for i, (script, args, description) in enumerate(steps, 1):
        print(f"\nStep {i}: {description}")
        if not run_step(script, args):
            print(f"ERROR: {script} failed")
            return 1

    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    print("=" * 50)
    print("\nOutput files in ./output/:")
    print("  • bible.json (raw parsed data)")
    print("  • clean.json (cleaned/normalized)")
    print("  • similarity.json (Jaccard similarities)")
    print("  • nodes.json (network nodes)")
    print("  • edges.json (network edges)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
