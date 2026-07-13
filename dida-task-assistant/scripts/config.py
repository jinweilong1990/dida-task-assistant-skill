"""Private local configuration and storage paths for Dida Task Assistant."""

from __future__ import annotations

import json
import os
import platform
import tempfile
from pathlib import Path
from typing import Any

SERVICE_ENDPOINTS = {
    "dida365": {
        "api_base_url": "https://api.dida365.com/open/v1",
        "authorize_url": "https://dida365.com/oauth/authorize",
        "token_url": "https://dida365.com/oauth/token",
    }
}
DEFAULT_REDIRECT_URI = "http://localhost:8080/callback"


def user_config_dir() -> Path:
    override = os.environ.get("DIDA_TASK_CAPTURE_CONFIG_DIR")
    if override:
        return Path(override).expanduser()
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "dida-task-assistant"
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "dida-task-assistant"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "dida-task-assistant"


def user_data_dir() -> Path:
    override = os.environ.get("DIDA_TASK_CAPTURE_DATA_DIR")
    if override:
        return Path(override).expanduser()
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "dida-task-assistant"
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "dida-task-assistant"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "dida-task-assistant"


def config_path() -> Path:
    return user_config_dir() / "config.json"


def ensure_private_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        directory.chmod(0o700)


def write_private_json(path: Path, payload: Any) -> None:
    ensure_private_dir(path.parent)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        if os.name != "nt":
            temp_path.chmod(0o600)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"配置文件不是有效 JSON: {path}") from exc


def save_config(config: dict[str, Any]) -> None:
    write_private_json(config_path(), config)


def current_service(config: dict[str, Any]) -> dict[str, str]:
    service_name = config.get("service", "dida365")
    try:
        return SERVICE_ENDPOINTS[service_name]
    except KeyError as exc:
        raise RuntimeError(f"不支持的服务: {service_name}") from exc


def missing_oauth_fields(config: dict[str, Any]) -> list[str]:
    return [field for field in ("client_id", "client_secret", "redirect_uri") if not config.get(field)]


def require_access_token() -> tuple[dict[str, Any], str]:
    config = load_config()
    token = config.get("access_token")
    if not token:
        raise RuntimeError("尚未授权。请先运行 configure.py 和 auth.py。")
    return config, token


def redact(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}…{value[-4:]}"
