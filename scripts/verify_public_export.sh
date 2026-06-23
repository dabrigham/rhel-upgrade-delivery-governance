#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Running privacy scan..."
echo "Using scripts/sensitive_terms.example.txt plus optional scripts/sensitive_terms.local.txt..."
python scripts/privacy_scan.py .

echo "Checking static web links..."
python scripts/check_web_links.py web

echo "Running tests..."
PYTHONPATH=src python -m unittest discover -s tests

echo "Running synthetic demo..."
./scripts/run_demo.sh

echo "Public export verification completed."
