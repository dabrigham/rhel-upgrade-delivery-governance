#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHONPATH=src python -m rhel_upgrade_governance.cli \
  --inventory examples/synthetic_inventory.csv \
  --changes examples/synthetic_change_records.csv \
  --output outputs/demo_output.csv \
  --exceptions outputs/exception_report.csv

