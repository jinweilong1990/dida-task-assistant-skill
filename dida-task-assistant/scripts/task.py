#!/usr/bin/env python3
"""JSON CLI for Dida365 task and project operations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from typing import Any

from api import DidaApiError, complete_task, create_project, create_task, delete_task, filter_tasks, get_inbox_project, get_project_data, get_projects, get_task, update_task


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    raise SystemExit(code)


def parse_relative_date(value: str | None) -> str | None:
    if not value:
        return None
    today = datetime.now().date()
    names = {"今天": 0, "today": 0, "明天": 1, "tomorrow": 1, "后天": 2, "day-after-tomorrow": 2}
    if value in names:
        return str(today + timedelta(days=names[value]))
    weekdays = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}
    if value in weekdays:
        days = weekdays[value] - today.weekday()
        return str(today + timedelta(days=days if days > 0 else days + 7))
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return value


def infer_date(raw: str | None) -> str | None:
    if not raw:
        return None
    for term in ("今天", "明天", "后天", "周一", "周二", "周三", "周四", "周五", "周六", "周日"):
        if term in raw:
            return parse_relative_date(term)
    return None


def infer_reminder(raw: str | None) -> list[str] | None:
    if not raw or not any(term in raw for term in ("提醒", "记得", "提前")):
        return None
    if "1小时" in raw or "一小时" in raw:
        return ["TRIGGER:-PT1H"]
    if "15分钟" in raw:
        return ["TRIGGER:-PT15M"]
    if "半小时" in raw or "30分钟" in raw:
        return ["TRIGGER:-PT30M"]
    return ["TRIGGER:PT0S"]


def resolve_project_id(value: str | None, default_to_inbox: bool = True) -> str:
    if value and value != "inbox":
        return value
    if value == "inbox" or default_to_inbox:
        return get_inbox_project()["id"]
    raise ValueError("该操作需要 --project-id；不要猜测任务所属清单。")


def task_summary(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": task.get("id"),
        "project_id": task.get("projectId"),
        "title": task.get("title"),
        "status": task.get("status", 0),
        "priority": task.get("priority", 0),
        "due_date": (task.get("dueDate") or "")[:10] or None,
        "tags": task.get("tags", []),
        "subtask_count": len(task.get("items", [])),
    }


def json_argument(value: str | None, argument_name: str, default: Any = None) -> Any:
    if value is None:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{argument_name} 必须是 JSON: {exc.msg}") from exc


def command_create(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(args.project_id)
    due_date = parse_relative_date(args.due_date) or infer_date(args.raw)
    reminders = json_argument(args.reminders_json, "--reminders-json") or infer_reminder(args.raw)
    items = json_argument(args.items_json, "--items-json")
    payload: dict[str, Any] = {
        "title": args.title,
        "projectId": project_id,
        "priority": args.priority,
        "isAllDay": args.is_all_day,
        "kind": "CHECKLIST" if items else args.kind,
        "status": 0,
        "sortOrder": 0,
    }
    if args.content:
        payload["content"] = args.content
    if args.desc:
        payload["desc"] = args.desc
    if args.tag:
        payload["tags"] = list(dict.fromkeys(args.tag))
    if due_date:
        payload["dueDate"] = f"{due_date}T00:00:00+0800" if args.is_all_day else f"{due_date}T23:59:59+0800"
    if args.start_date:
        start_date = parse_relative_date(args.start_date)
        payload["startDate"] = f"{start_date}T09:00:00+0800" if "T" not in start_date else start_date
    if reminders:
        payload["reminders"] = reminders
    if items:
        if not isinstance(items, list):
            raise ValueError("--items-json 必须是子任务数组")
        payload["items"] = [
            {"title": item["title"] if isinstance(item, dict) else str(item), "status": 0, "sortOrder": index}
            for index, item in enumerate(items)
        ]
    result = create_task(payload)
    return {"success": True, "action": "created", "task": task_summary(result), "raw_result": result}


def command_list(args: argparse.Namespace) -> dict[str, Any]:
    if args.project_id:
        project_id = resolve_project_id(args.project_id)
        data = get_project_data(project_id)
        tasks = data.get("tasks", [])
        return {"success": True, "project_id": project_id, "count": len(tasks), "tasks": [task_summary(task) for task in tasks]}
    result: list[dict[str, Any]] = []
    for project in get_projects():
        if project.get("kind") != "TASK":
            continue
        data = get_project_data(project["id"])
        result.append({"project_id": project["id"], "project_name": project.get("name"), "tasks": [task_summary(task) for task in data.get("tasks", [])]})
    return {"success": True, "projects": result}


def command_filter(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.project_id:
        payload["projectId"] = resolve_project_id(args.project_id)
    if args.status is not None:
        payload["status"] = args.status
    if args.priority is not None:
        payload["priority"] = args.priority
    if args.tag:
        payload["tags"] = args.tag
    if args.start_date or args.end_date:
        payload["startDate"] = parse_relative_date(args.start_date) or "1970-01-01"
        payload["endDate"] = parse_relative_date(args.end_date) or "2099-12-31"
    try:
        tasks = filter_tasks(payload)
        return {"success": True, "source": "api", "count": len(tasks), "tasks": [task_summary(task) for task in tasks]}
    except DidaApiError:
        if not payload.get("projectId"):
            raise
        tasks = get_project_data(payload["projectId"]).get("tasks", [])
        filtered = [task for task in tasks if _matches(task, args)]
        return {"success": True, "source": "project-data-fallback", "count": len(filtered), "tasks": [task_summary(task) for task in filtered]}


def _matches(task: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.status is not None and task.get("status", 0) != args.status:
        return False
    if args.priority is not None and task.get("priority", 0) != args.priority:
        return False
    if args.tag and not set(args.tag).issubset(set(task.get("tags", []))):
        return False
    due = (task.get("dueDate") or "")[:10]
    if args.start_date and (not due or due < parse_relative_date(args.start_date)):
        return False
    if args.end_date and (not due or due > parse_relative_date(args.end_date)):
        return False
    return True


def command_update(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(args.project_id, default_to_inbox=False)
    payload: dict[str, Any] = {"id": args.task_id, "projectId": project_id}
    field_map = {"title": args.title, "desc": args.desc, "content": args.content, "priority": args.priority}
    payload.update({key: value for key, value in field_map.items() if value is not None})
    if args.due_date:
        due_date = parse_relative_date(args.due_date)
        payload["dueDate"] = f"{due_date}T23:59:59+0800"
    if args.add_tag or args.remove_tag or args.add_subtask:
        current = get_task(project_id, args.task_id)
        if args.add_tag or args.remove_tag:
            tags = list(current.get("tags", []))
            tags = [tag for tag in tags if tag != args.remove_tag]
            if args.add_tag and args.add_tag not in tags:
                tags.append(args.add_tag)
            payload["tags"] = tags
        if args.add_subtask:
            items = list(current.get("items", []))
            items.append({"title": args.add_subtask, "status": 0, "sortOrder": len(items)})
            payload["items"] = items
            payload["kind"] = "CHECKLIST"
    if len(payload) == 2:
        raise ValueError("没有可更新的字段")
    result = update_task(args.task_id, payload)
    return {"success": True, "action": "updated", "task": task_summary(result), "raw_result": result}


def command_complete(args: argparse.Namespace, complete: bool) -> dict[str, Any]:
    project_id = resolve_project_id(args.project_id, default_to_inbox=False)
    if complete:
        result = complete_task(project_id, args.task_id)
        return {"success": True, "action": "completed", "task_id": args.task_id, "project_id": project_id, "raw_result": result}
    result = update_task(args.task_id, {"id": args.task_id, "projectId": project_id, "status": 0, "completedTime": None})
    return {"success": True, "action": "uncompleted", "task": task_summary(result), "raw_result": result}


def command_delete(args: argparse.Namespace) -> dict[str, Any]:
    project_id = resolve_project_id(args.project_id, default_to_inbox=False)
    result = delete_task(project_id, args.task_id)
    return {"success": True, "action": "deleted", "task_id": args.task_id, "project_id": project_id, "raw_result": result}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dida365 任务管理 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="创建任务")
    create.add_argument("--title", required=True)
    create.add_argument("--project-id")
    create.add_argument("--due-date")
    create.add_argument("--start-date")
    create.add_argument("--priority", type=int, choices=[0, 1, 3, 5], default=0)
    create.add_argument("--content")
    create.add_argument("--desc")
    create.add_argument("--tag", action="append", default=[])
    create.add_argument("--reminders-json")
    create.add_argument("--items-json")
    create.add_argument("--kind", choices=["TEXT", "NOTE", "CHECKLIST"], default="TEXT")
    create.add_argument("--is-all-day", action="store_true")
    create.add_argument("--raw")

    listing = subparsers.add_parser("list", help="列出任务")
    listing.add_argument("--project-id")

    filtering = subparsers.add_parser("filter", help="筛选任务")
    filtering.add_argument("--project-id")
    filtering.add_argument("--status", type=int, choices=[0, 2])
    filtering.add_argument("--priority", type=int, choices=[0, 1, 3, 5])
    filtering.add_argument("--tag", action="append", default=[])
    filtering.add_argument("--start-date")
    filtering.add_argument("--end-date")

    update = subparsers.add_parser("update", help="更新任务")
    update.add_argument("--task-id", required=True)
    update.add_argument("--project-id")
    update.add_argument("--title")
    update.add_argument("--desc")
    update.add_argument("--content")
    update.add_argument("--priority", type=int, choices=[0, 1, 3, 5])
    update.add_argument("--due-date")
    update.add_argument("--add-tag")
    update.add_argument("--remove-tag")
    update.add_argument("--add-subtask")

    for command in ("complete", "uncomplete", "delete"):
        action = subparsers.add_parser(command)
        action.add_argument("--task-id", required=True)
        action.add_argument("--project-id")

    project_create = subparsers.add_parser("project-create", help="创建清单")
    project_create.add_argument("--name", required=True)
    project_create.add_argument("--color", default="#4A90D9")
    project_create.add_argument("--view-mode", choices=["list", "kanban", "timeline"], default="list")
    project_create.add_argument("--kind", choices=["TASK", "NOTE"], default="TASK")
    subparsers.add_parser("project-list", help="列出清单")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "create":
            emit(command_create(args))
        if args.command == "list":
            emit(command_list(args))
        if args.command == "filter":
            emit(command_filter(args))
        if args.command == "update":
            emit(command_update(args))
        if args.command == "complete":
            emit(command_complete(args, True))
        if args.command == "uncomplete":
            emit(command_complete(args, False))
        if args.command == "delete":
            emit(command_delete(args))
        if args.command == "project-create":
            result = create_project(args.name, args.color, args.view_mode, args.kind)
            emit({"success": True, "action": "project_created", "project": result})
        emit({"success": True, "projects": get_projects()})
    except (DidaApiError, RuntimeError, ValueError) as exc:
        emit({"success": False, "error": str(exc)}, 1)


if __name__ == "__main__":
    main()
