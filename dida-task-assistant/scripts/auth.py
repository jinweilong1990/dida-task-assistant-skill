#!/usr/bin/env python3
"""OAuth authorization-code flow for the current user's Dida365 application."""

from __future__ import annotations

import argparse
import base64
import hmac
import html
import json
import secrets
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

from config import current_service, load_config, missing_oauth_fields, save_config


class CallbackHandler(BaseHTTPRequestHandler):
    expected_state = ""
    expected_path = "/callback"
    code: str | None = None
    error: str | None = None

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_page(self, status: int, title: str, body: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        safe_body = html.escape(body)
        self.wfile.write(
            f"<html><meta charset='utf-8'><title>{html.escape(title)}</title><body style='font-family:system-ui;padding:32px'><h2>{html.escape(title)}</h2><p>{safe_body}</p></body></html>".encode("utf-8")
        )

    def do_GET(self) -> None:  # noqa: N802 - HTTPServer hook
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path != self.expected_path:
            self.send_page(404, "未找到回调页面", "请回到授权流程重新开始。")
            return
        received_state = query.get("state", [""])[0]
        if not hmac.compare_digest(received_state, self.expected_state):
            self.error = "OAuth state 校验失败，已拒绝此次回调。"
            self.send_page(400, "授权失败", self.error)
            return
        if "error" in query:
            self.error = query.get("error_description", query["error"])[0]
            self.send_page(400, "授权失败", self.error)
            return
        self.code = query.get("code", [None])[0]
        if not self.code:
            self.error = "回调未包含授权码。"
            self.send_page(400, "授权失败", self.error)
            return
        self.send_page(200, "授权成功", "可以关闭此页面并回到终端。")


def callback_server(redirect_uri: str, state: str) -> HTTPServer:
    parsed = urlparse(redirect_uri)
    if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1"} or not parsed.port:
        raise RuntimeError("v0.1 仅支持 http://localhost:<port>/callback 或 127.0.0.1 本地回调地址。")
    CallbackHandler.expected_state = state
    CallbackHandler.expected_path = parsed.path or "/callback"
    CallbackHandler.code = None
    CallbackHandler.error = None
    return HTTPServer(("127.0.0.1", parsed.port), CallbackHandler)


def authorization_url(config: dict[str, str], state: str) -> str:
    endpoints = current_service(config)
    query = urlencode({
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "response_type": "code",
        "scope": "tasks:read tasks:write",
        "state": state,
    })
    return f"{endpoints['authorize_url']}?{query}"


def exchange_code(config: dict[str, str], code: str) -> dict[str, str]:
    credentials = base64.b64encode(f"{config['client_id']}:{config['client_secret']}".encode("utf-8")).decode("ascii")
    body = urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config["redirect_uri"],
    }).encode("utf-8")
    request = Request(
        current_service(config)["token_url"],
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            token_data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"交换 Token 失败 ({exc.code}): {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"交换 Token 网络请求失败: {exc.reason}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Dida365 Token 接口返回了非 JSON 响应。") from exc
    if not token_data.get("access_token"):
        raise RuntimeError("Dida365 没有返回 access_token。")
    return token_data


def main() -> None:
    parser = argparse.ArgumentParser(description="为 Dida Task Assistant 授权 Dida365")
    parser.add_argument("--print-url", action="store_true", help="只输出授权地址，不自动打开浏览器")
    args = parser.parse_args()
    config = load_config()
    missing = missing_oauth_fields(config)
    if missing:
        raise SystemExit(f"缺少配置: {', '.join(missing)}。请先运行 configure.py。")
    state = secrets.token_urlsafe(32)
    url = authorization_url(config, state)
    server = callback_server(config["redirect_uri"], state)
    print("请在浏览器中完成 Dida365 授权。")
    print(url)
    if not args.print_url:
        webbrowser.open(url)
    try:
        server.handle_request()
    finally:
        server.server_close()
    if CallbackHandler.error:
        raise SystemExit(CallbackHandler.error)
    if not CallbackHandler.code:
        raise SystemExit("没有收到授权码。")
    try:
        tokens = exchange_code(config, CallbackHandler.code)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    config["access_token"] = tokens["access_token"]
    if tokens.get("refresh_token"):
        config["refresh_token"] = tokens["refresh_token"]
    save_config(config)
    print('{"success": true, "message": "Dida365 授权成功"}')


if __name__ == "__main__":
    main()
