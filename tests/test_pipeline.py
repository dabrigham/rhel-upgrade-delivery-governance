from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from rhel_upgrade_governance.pipeline import run_governance_pipeline


ROOT = Path(__file__).resolve().parents[1]


class GovernancePipelineTests(unittest.TestCase):
    def test_synthetic_pipeline_flags_review_gates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            output = tmp_path / "demo_output.csv"
            exceptions = tmp_path / "exception_report.csv"

            results = run_governance_pipeline(
                ROOT / "examples" / "synthetic_inventory.csv",
                ROOT / "examples" / "synthetic_change_records.csv",
                output,
                exceptions,
            )

            self.assertEqual(len(results), 5)
            self.assertEqual(sum(1 for result in results if result.decision == "include"), 2)
            self.assertEqual(sum(1 for result in results if result.decision == "hold"), 3)
            exception_text = exceptions.read_text(encoding="utf-8")
            self.assertIn("missing_task_assignment_group", exception_text)
            self.assertIn("invalid_schedule_window", exception_text)


if __name__ == "__main__":
    unittest.main()
