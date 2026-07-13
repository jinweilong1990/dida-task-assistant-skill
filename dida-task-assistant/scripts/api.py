"""Small Dida365 Open API client used by task.py."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import current_service, require_access_token


class DidaApiError(RuntimeError):
    pass


def api_request(method: str, endpoint: str, data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> Any:
    config, token = require_access_token()
    url = f"{current_service(config)['api_base_url']}{endpoint}"
    if params:
        url = f"{url}?{urlencode(params)}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    request = Request(
        url,
        data=body,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            response_body = response.read()
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")[:500]
        if exc.code == 401:
            raise DidaApiError("Dida365 授权已失效。请重新运行 auth.py；不要在聊天中粘贴 Token。") from exc
        raise DidaApiError(f"Dida365 API 请求失败 ({exc.code}): {error_body}") from exc
    except URLError as exc:
        raise DidaApiError(f"Dida365 网络请求失败: {exc.reason}") from exc
    if not 200 <= status < 300:
        raise DidaApiError(f"Dida365 API 请求失败 ({status})")
    if not response_body:
        return {"ok": True}
    try:
        return json.loads(response_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DidaApiError("Dida365 API 返回了非 JSON 响应") from exc


def get_projects() -> list[dict[str, Any]]:
    return api_request("GET", "/project")


def get_inbox_project() -> dict[str, Any]:
    projects = get_projects()
    for project in projects:
        if project.get("groupId") in (None, ""):
            return project
    if projects:
        return projects[0]
    raise DidaApiError("Dida365 未返回可用清单")


def get_project_data(project_id: str) -> dict[str, Any]:
    return api_request("GET", f"/project/{project_id}/data")


def get_task(project_id: str, task_id: str) -> dict[str, Any]:
    return api_request("GET", f"/project/{project_id}/task/{task_id}")


def create_project(name: str, color: str = "#4A90D9", view_mode: str = "list", kind: str = "TASK") -> dict[str, Any]:
    return api_request("POST", "/project", {"name": name, "color": color, "viewMode": view_mode, "kind": kind, "sortOrder": 0})


def create_task(payload: dict[str, Any]) -> dict[str, Any]:
    return api_request("POST", "/task", payload)


def update_task(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return api_request("POST", f"/task/{task_id}", payload)


def complete_task(project_id: str, task_id: str) -> dict[str, Any]:
    return api_request("POST", f"/project/{project_id}/task/{task_id}/complete")


def delete_task(project_id: str, task_id: str) -> dict[str, Any]:
    return api_request("DELETE", f"/project/{project_id}/task/{task_id}")


def filter_tasks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return api_request("POST", "/task/filter", payload)
