#!/usr/bin/env python3
"""Verify the canonical Skill package before a GitHub + SkillHub release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "dida-task-assistant"
VERSION_FILE = ROOT / "VERSION"
ALLOWED_TOP_LEVEL = {"SKILL.md", "scripts", "references", "assets"}
PROHIBITED_NAMES = {
    "__pycache__",
    ".DS_Store",
    ".env",
    "config.json",
    "records.json",
    "events.jsonl",
    "inbox.md",
}
SECRET_PATTERNS = (
    re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b"),
    re.compile(
        r"(?i)(?:client[_ -]?secret|access[_ -]?token|refresh[_ -]?token|api[_ -]?key)"
        r"\s*[:=]\s*['\"][A-Za-z0-9._-]{8,}['\"]"
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the cross-channel Skill release source")
    parser.add_argument("--expected-version")
    parser.add_argument("--require-clean", action="store_true")
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(message)


def read_version() -> str:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"VERSION is not semantic versioning: {version!r}")
    return version


def list_source_files() -> list[Path]:
    unexpected = sorted(path.name for path in SKILL_DIR.iterdir() if path.name not in ALLOWED_TOP_LEVEL)
    if unexpected:
        fail(f"Unsupported top-level Skill entries: {', '.join(unexpected)}")

    files: list[Path] = []
    for path in sorted(SKILL_DIR.rglob("*"), key=lambda item: item.as_posix()):
        if path.name in PROHIBITED_NAMES or path.suffix == ".pyc":
            fail(f"Prohibited runtime/private file in Skill: {path.relative_to(SKILL_DIR)}")
        if path.is_file():
            files.append(path)
    if (SKILL_DIR / "SKILL.md") not in files:
        fail("SKILL.md is missing")
    return files


def read_skill_identifier() -> str:
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", content)
    if not match:
        fail("SKILL.md has no valid name field")
    identifier = match.group(1)
    if identifier != SKILL_DIR.name:
        fail(f"Skill name {identifier!r} does not match directory {SKILL_DIR.name!r}")
    return identifier


def scan_secrets(files: list[Path]) -> None:
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            fail(f"Potential credential found in {path.relative_to(SKILL_DIR)}")


def fingerprint(files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(SKILL_DIR).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\0")
    return digest.hexdigest()


def require_clean_worktree() -> None:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if completed.stdout.strip():
        fail("Git worktree is not clean")


def main() -> None:
    args = parse_args()
    version = read_version()
    if args.expected_version and version != args.expected_version:
        fail(f"VERSION mismatch: expected {args.expected_version}, got {version}")
    files = list_source_files()
    identifier = read_skill_identifier()
    scan_secrets(files)
    if args.require_clean:
        require_clean_worktree()
    print(json.dumps({
        "success": True,
        "version": version,
        "skill_identifier": identifier,
        "source_directory": SKILL_DIR.name,
        "file_count": len(files),
        "source_fingerprint_sha256": fingerprint(files),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
