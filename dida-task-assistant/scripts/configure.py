#!/usr/bin/env python3
"""Interactively configure this user's Dida365 OAuth application."""

from __future__ import annotations

import argparse
import getpass
import json

from config import DEFAULT_REDIRECT_URI, SERVICE_ENDPOINTS, load_config, missing_oauth_fields, redact, save_config


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="配置 Dida Task Assistant 的 Dida365 OAuth 凭据")
    result.add_argument("--client-id")
    result.add_argument("--client-secret")
    result.add_argument("--redirect-uri", default=DEFAULT_REDIRECT_URI)
    result.add_argument("--show", action="store_true", help="显示脱敏后的配置状态")
    return result


def main() -> None:
    args = parser().parse_args()
    config = load_config()
    if args.show:
        missing = missing_oauth_fields(config)
        print(json.dumps({
            "configured": not missing,
            "missing": missing,
            "service": config.get("service", "dida365"),
            "client_id": redact(config.get("client_id")),
            "redirect_uri": config.get("redirect_uri"),
            "authorized": bool(config.get("access_token")),
        }, ensure_ascii=False, sort_keys=True))
        return

    client_id = args.client_id or input("Dida365 Client ID: ").strip()
    client_secret = args.client_secret or getpass.getpass("Dida365 Client Secret (不会回显): ").strip()
    if not client_id or not client_secret:
        raise SystemExit("Client ID 和 Client Secret 都不能为空。")
    config.update({
        "service": "dida365",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": args.redirect_uri,
    })
    save_config(config)
    print(json.dumps({
        "success": True,
        "service": "dida365",
        "redirect_uri": args.redirect_uri,
        "next": "运行 auth.py 完成浏览器授权",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
