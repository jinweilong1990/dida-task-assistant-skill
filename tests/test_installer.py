from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.py"


class InstallerTests(unittest.TestCase):
    def test_custom_install_copies_the_canonical_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination_root = Path(temporary) / "skills"
            completed = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "custom", "--dest", str(destination_root)],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            installed = destination_root / "dida-task-assistant"
            self.assertTrue(payload["success"])
            self.assertTrue((installed / "SKILL.md").exists())
            self.assertTrue((installed / "scripts" / "task.py").exists())
            self.assertFalse((installed / "__pycache__").exists())

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination_root = Path(temporary) / "skills"
            completed = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "custom", "--dest", str(destination_root), "--dry-run"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(completed.stdout)["success"])
            self.assertFalse(destination_root.exists())


if __name__ == "__main__":
    unittest.main()
