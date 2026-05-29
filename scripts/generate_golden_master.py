#!/usr/bin/env python3
"""Generate tests/golden_master_expected.txt from live Magic Square Solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master import EXPECTED_PATH, write_expected  # noqa: E402


def main() -> int:
    """Write Golden Master baseline and print destination path."""
    parser = argparse.ArgumentParser(
        description="Generate Golden Master baseline from current solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPECTED_PATH,
        help=f"Output path (default: {EXPECTED_PATH})",
    )
    args = parser.parse_args()

    target = write_expected(args.output)
    print(f"Golden Master baseline written: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
