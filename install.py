#!/usr/bin/env python3
"""Install the canonical Agent Skill into one or more supported client roots."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "dida-task-assistant"
REPOSITORY_ROOT = Path(__file__).resolve().parent
SOURCE = REPOSITORY_ROOT / SKILL_NAME


def known_skill_roots() -> dict[str, Path]:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return {
        "codex": codex_home / "skills",
        "claude-code": Path.home() / ".claude" / "skills",
        "agents": Path.home() / ".agents" / "skills",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="安装 Dida Task Assistant Agent Skill")
    parser.add_argument(
        "--target",
        action="append",
        choices=["codex", "claude-code", "agents", "all", "custom"],
        required=True,
        help="可重复指定；all 安装到三个已知的用户级 Skill 目录",
    )
    parser.add_argument("--dest", type=Path, help="target=custom 时的 Skill 根目录")
    parser.add_argument("--force", action="store_true", help="覆盖同名的公开版 Skill")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def selected_roots(args: argparse.Namespace) -> list[tuple[str, Path]]:
    known = known_skill_roots()
    selected: list[tuple[str, Path]] = []
    for target in args.target:
        if target == "all":
            selected.extend(known.items())
        elif target == "custom":
            if args.dest is None:
                raise ValueError("target=custom 时必须提供 --dest")
            selected.append(("custom", args.dest.expanduser()))
        else:
            selected.append((target, known[target]))
    deduplicated: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for name, root in selected:
        resolved = root.resolve()
        if resolved not in seen:
            deduplicated.append((name, root))
            seen.add(resolved)
    return deduplicated


def install(root: Path, force: bool, dry_run: bool) -> dict[str, str | bool]:
    destination = root / SKILL_NAME
    if destination.exists() and not force:
        return {
            "success": False,
            "destination": str(destination),
            "error": "目标已存在；确认它是公开版后使用 --force 更新",
        }
    if destination.exists() and force:
        marker = destination / "SKILL.md"
        marker_text = marker.read_text(encoding="utf-8", errors="replace") if marker.exists() else ""
        if "name: dida-task-assistant" not in marker_text:
            return {
                "success": False,
                "destination": str(destination),
                "error": "目标目录不是可识别的 dida-task-assistant Skill，拒绝覆盖",
            }
    if not dry_run:
        root.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(
            SOURCE,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
    return {"success": True, "destination": str(destination), "dry_run": dry_run}


def main() -> None:
    args = parse_args()
    if not SOURCE.joinpath("SKILL.md").exists():
        raise SystemExit(f"找不到标准 Skill: {SOURCE}")
    try:
        roots = selected_roots(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    results = []
    for target, root in roots:
        result = install(root, args.force, args.dry_run)
        result["target"] = target
        results.append(result)
    payload = {"success": all(item["success"] for item in results), "skill": SKILL_NAME, "results": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if not payload["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
