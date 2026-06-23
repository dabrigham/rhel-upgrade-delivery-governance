from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_governance_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the synthetic RHEL upgrade delivery governance demo.",
    )
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--changes", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--exceptions", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = run_governance_pipeline(
        Path(args.inventory),
        Path(args.changes),
        Path(args.output),
        Path(args.exceptions),
    )
    holds = sum(1 for result in results if result.decision == "hold")
    print(f"Processed {len(results)} synthetic servers")
    print(f"Ready for wave review: {len(results) - holds}")
    print(f"Requires human review: {holds}")
    print(f"Output: {args.output}")
    print(f"Exceptions: {args.exceptions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

