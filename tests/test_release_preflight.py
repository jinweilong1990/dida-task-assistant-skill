import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleasePreflightTests(unittest.TestCase):
    def test_canonical_skill_matches_release_version(self):
        for cache_dir in (ROOT / "dida-task-assistant").rglob("__pycache__"):
            shutil.rmtree(cache_dir)

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "release_preflight.py"),
                "--expected-version",
                (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        result = json.loads(completed.stdout)
        self.assertTrue(result["success"])
        self.assertEqual(result["version"], "1.0.1")
        self.assertEqual(result["skill_identifier"], "dida-task-assistant")
        self.assertRegex(result["source_fingerprint_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
