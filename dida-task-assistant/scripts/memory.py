#!/usr/bin/env python3
"""Local-first record store. It never calls Dida365."""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config import ensure_private_dir, user_data_dir, write_private_json


def paths() -> tuple[Path, Path, Path]:
    directory = user_data_dir()
    ensure_private_dir(directory)
    return directory / "records.json", directory / "events.jsonl", directory / "inbox.md"


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def load_records() -> list[dict[str, Any]]:
    records_path, _, _ = paths()
    if not records_path.exists():
        return []
    try:
        data = json.loads(records_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"本地记录文件损坏: {records_path}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"本地记录格式错误: {records_path}")
    return data


def save_records(records: list[dict[str, Any]]) -> None:
    records_path, _, _ = paths()
    write_private_json(records_path, records)


def append_event(event_type: str, record_id: str, details: dict[str, Any] | None = None) -> None:
    _, event_path, _ = paths()
    event = {"at": now(), "event": event_type, "record_id": record_id, "details": details or {}}
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    if os.name != "nt":
        event_path.chmod(0o600)


def append_inbox(record: dict[str, Any]) -> None:
    _, _, inbox_path = paths()
    tags = " ".join(f"#{tag}" for tag in record["tags"])
    body = record.get("body") or record.get("raw") or ""
    with inbox_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- [{record['created_at']}] ({record['kind']}) {record['title']} {tags}\n")
        if body:
            handle.write(f"  - {body}\n")
    if os.name != "nt":
        inbox_path.chmod(0o600)


def create_record(kind: str, title: str, body: str | None, raw: str | None, tags: list[str], sync_status: str) -> dict[str, Any]:
    clean_tags = list(dict.fromkeys(tag.strip() for tag in tags if tag.strip()))
    record = {
        "schema_version": 1,
        "record_id": uuid.uuid4().hex,
        "created_at": now(),
        "updated_at": now(),
        "kind": kind,
        "title": title.strip(),
        "body": body.strip() if body else None,
        "raw": raw.strip() if raw else None,
        "tags": clean_tags,
        "local_status": "completed" if kind == "completion" else "active",
        "sync_status": sync_status,
        "remote": None,
    }
    if not record["title"]:
        raise RuntimeError("本地记录需要 title")
    records = load_records()
    records.append(record)
    save_records(records)
    append_inbox(record)
    append_event("record_created", record["record_id"], {"kind": kind, "sync_status": sync_status})
    return record


def update_record(record_id: str, mutate: Any, event_type: str) -> dict[str, Any]:
    records = load_records()
    for record in records:
        if record.get("record_id") == record_id:
            mutate(record)
            record["updated_at"] = now()
            save_records(records)
            append_event(event_type, record_id, {"sync_status": record.get("sync_status")})
            return record
    raise RuntimeError(f"找不到本地记录: {record_id}")


def link_remote(record_id: str, task_id: str, project_id: str) -> dict[str, Any]:
    def mutate(record: dict[str, Any]) -> None:
        record["remote"] = {"connector": "dida365", "task_id": task_id, "project_id": project_id}
        record["sync_status"] = "synced"

    return update_record(record_id, mutate, "remote_linked")


def mark_status(record_id: str, local_status: str, sync_status: str | None) -> dict[str, Any]:
    def mutate(record: dict[str, Any]) -> None:
        record["local_status"] = local_status
        if sync_status:
            record["sync_status"] = sync_status

    return update_record(record_id, mutate, "status_changed")


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    raise SystemExit(code)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dida Task Assistant 本地记录工具")
    commands = parser.add_subparsers(dest="command", required=True)

    capture = commands.add_parser("capture", help="创建本地记录")
    capture.add_argument("--kind", choices=["task", "reminder", "completion", "idea", "note"], required=True)
    capture.add_argument("--title", required=True)
    capture.add_argument("--body")
    capture.add_argument("--raw")
    capture.add_argument("--tag", action="append", default=[])
    capture.add_argument("--sync-status", choices=["local_only", "pending"], default="local_only")

    link = commands.add_parser("link", help="写回远端任务 ID")
    link.add_argument("--record-id", required=True)
    link.add_argument("--task-id", required=True)
    link.add_argument("--project-id", required=True)

    status = commands.add_parser("set-status", help="更新本地状态")
    status.add_argument("--record-id", required=True)
    status.add_argument("--local-status", choices=["active", "completed", "archived"], required=True)
    status.add_argument("--sync-status", choices=["local_only", "pending", "synced", "failed"])

    listing = commands.add_parser("list", help="列出本地记录")
    listing.add_argument("--kind", choices=["task", "reminder", "completion", "idea", "note"])
    listing.add_argument("--sync-status", choices=["local_only", "pending", "synced", "failed"])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "capture":
            record = create_record(args.kind, args.title, args.body, args.raw, args.tag, args.sync_status)
            emit({"success": True, "record": record})
        if args.command == "link":
            record = link_remote(args.record_id, args.task_id, args.project_id)
            emit({"success": True, "record": record})
        if args.command == "set-status":
            record = mark_status(args.record_id, args.local_status, args.sync_status)
            emit({"success": True, "record": record})
        records = load_records()
        if args.kind:
            records = [record for record in records if record.get("kind") == args.kind]
        if args.sync_status:
            records = [record for record in records if record.get("sync_status") == args.sync_status]
        emit({"success": True, "count": len(records), "records": records})
    except RuntimeError as exc:
        emit({"success": False, "error": str(exc)}, 1)


if __name__ == "__main__":
    main()
