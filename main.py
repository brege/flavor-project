#!/usr/bin/env python
"""
Flavor Project Pipeline
Runs the complete data processing pipeline to generate flavor network outputs.

Usage:
    python main.py
"""

import subprocess
import sys
import os

def run_step(script, args):
    """Run a pipeline step."""
    print(f"\nRunning {script}...")
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    result = subprocess.run([sys.executable, script] + args, env=env, check=False)
    return result.returncode == 0

def main():
    print("=" * 50)
    print("FLAVOR PROJECT PIPELINE")
    print("=" * 50)

    steps = [
        ("src/pipeline/parse.py", [], "Parse HTML chapters"),
        ("src/pipeline/clean.py", ["data/bible.json", "data/clean.json"], "Clean and normalize data"),
        ("src/pipeline/similarity.py", ["-i", "data/clean.json", "-o", "data/similarity.json"], "Compute similarity matrix"),
        ("src/pipeline/graph.py", ["data/clean.json", "data/edges.json", "data/nodes.json"], "Create network graph"),
    ]

    for i, (script, args, description) in enumerate(steps, 1):
        print(f"\nStep {i}: {description}")
        if not run_step(script, args):
            print(f"ERROR: {script} failed")
            return 1

    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    print("=" * 50)
    print("\nOutput files in ./data/:")
    print("  • bible.json (raw parsed data)")
    print("  • clean.json (cleaned/normalized)")
    print("  • similarity.json (Jaccard similarities)")
    print("  • nodes.json (network nodes)")
    print("  • edges.json (network edges)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
