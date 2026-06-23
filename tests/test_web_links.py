from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_web_links.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_web_links", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class WebLinkTests(unittest.TestCase):
    def test_static_web_bundle_links_resolve_inside_web_root(self) -> None:
        checker = load_checker()
        self.assertEqual(checker.check_web_links(ROOT / "web"), [])


if __name__ == "__main__":
    unittest.main()
