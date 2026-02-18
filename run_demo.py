#!/usr/bin/env python3
"""Quick demo: run every contaminated case through the naive executor.

Usage:
    python run_demo.py

This shows what happens when action bundles are executed without a gate.
Every contaminated case produces state corruption — that is the point.
"""

import json
import pathlib
import sys

from sim.executor import Executor
from sim.resources import ResourceManager
from sim.logger import TraceLogger


CASES_DIR = pathlib.Path(__file__).resolve().parent / "cases"

DIVIDER = "-" * 60


def load_case(name: str) -> dict:
    with open(CASES_DIR / name) as f:
        return json.load(f)


def run_one(name: str, bundle: dict) -> None:
    """Execute a single bundle with a fresh naive executor and print results."""
    resources = ResourceManager()
    logger = TraceLogger()
    executor = Executor(resources=resources, logger=logger, gate=None)

    print(f"\n{DIVIDER}")
    print(f"CASE: {name}")
    print(f"  operation : {bundle.get('operation_type')}")
    print(f"  target    : {bundle.get('target_resource')}")
    print(DIVIDER)

    result = executor.execute(bundle)

    print(f"  result    : {result}")
    print(f"  trace len : {len(logger.get_trace())} events")

    # Show corruption indicators
    fs = resources.fs.snapshot()
    db = resources.db.snapshot()
    if fs:
        print(f"  fs state  : {json.dumps(fs, indent=2)[:200]}")
    if db:
        print(f"  db state  : {json.dumps(db, indent=2)[:200]}")


def main():
    print("=" * 60)
    print("EXECUTION BOUNDARY LAB — Naive Executor Demo")
    print("=" * 60)
    print()
    print("Running all contaminated cases WITHOUT a gate.")
    print("Each case demonstrates a different pre-positioning failure.")

    cases = sorted(CASES_DIR.glob("contaminated_case_*.json"))
    if not cases:
        print("ERROR: No contaminated case files found.", file=sys.stderr)
        sys.exit(1)

    for path in cases:
        bundle = load_case(path.name)
        run_one(path.stem, bundle)

    # Also run the clean case for comparison
    clean = CASES_DIR / "clean_case_1.json"
    if clean.exists():
        bundle = load_case("clean_case_1.json")
        run_one("clean_case_1 (control)", bundle)

    print(f"\n{'=' * 60}")
    print("DONE. All cases above executed without gate intervention.")
    print("A conformant gate would HOLD or DENY the contaminated cases.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
