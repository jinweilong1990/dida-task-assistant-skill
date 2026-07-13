from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "dida-task-assistant" / "scripts" / "memory.py"
TASK = ROOT / "dida-task-assistant" / "scripts" / "task.py"


class LocalMemoryTests(unittest.TestCase):
    def run_memory(self, data_dir: Path, *arguments: str) -> dict:
        environment = os.environ.copy()
        environment["DIDA_TASK_CAPTURE_DATA_DIR"] = str(data_dir)
        completed = subprocess.run(
            [sys.executable, str(MEMORY), *arguments],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        return json.loads(completed.stdout)

    def test_capture_link_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            data_dir = Path(temporary)
            captured = self.run_memory(
                data_dir,
                "capture",
                "--kind",
                "idea",
                "--title",
                "验证口播视频精修工具",
                "--tag",
                "产品",
                "--tag",
                "灵感",
                "--sync-status",
                "pending",
            )
            record_id = captured["record"]["record_id"]
            linked = self.run_memory(data_dir, "link", "--record-id", record_id, "--task-id", "task-1", "--project-id", "project-1")
            self.assertEqual(linked["record"]["sync_status"], "synced")
            self.assertEqual(linked["record"]["remote"]["task_id"], "task-1")
            listed = self.run_memory(data_dir, "list", "--kind", "idea")
            self.assertEqual(listed["count"], 1)
            self.assertTrue((data_dir / "inbox.md").exists())
            self.assertTrue((data_dir / "events.jsonl").exists())

    def test_task_cli_help_does_not_require_an_account(self) -> None:
        completed = subprocess.run([sys.executable, str(TASK), "--help"], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0)
        self.assertIn("Dida365", completed.stdout)


if __name__ == "__main__":
    unittest.main()
