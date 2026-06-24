from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = ROOT / "scripts" / "privacy_scan.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("privacy_scan", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCANNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PrivacyScannerTests(unittest.TestCase):
    def test_github_pages_permission_block_is_not_a_secret(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github" / "workflows" / "pages.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "\n".join(
                    [
                        "permissions:",
                        "  contents: read",
                        "  pages: write",
                        "  id-" + "to" + "ken: write",
                        "  actions: read",
                        "  pull-requests: write",
                    ]
                ),
                encoding="utf-8",
            )

            findings, _ = scanner.scan_file(workflow, root, [])

        self.assertEqual(findings, [])

    def test_fake_secret_assignment_is_flagged(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "unsafe.env"
            secret_key = "TO" + "KEN"
            script.write_text(f"{secret_key}=fake-token-value-for-scanner-test\n", encoding="utf-8")

            findings, _ = scanner.scan_file(script, root, [])

        self.assertTrue(any(finding.kind == "secret_assignment" for finding in findings))

    def test_fake_long_credential_like_value_is_flagged(self) -> None:
        scanner = load_scanner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "unsafe.txt"
            secret_prefix = "ghp" + "_"
            script.write_text(f"credential={secret_prefix}abcdefghijklmnopqrstuvwxyz1234567890\n", encoding="utf-8")

            findings, _ = scanner.scan_file(script, root, [])

        self.assertTrue(any(finding.kind == "long_credential_like_value" for finding in findings))


if __name__ == "__main__":
    unittest.main()
