#!/usr/bin/env python3
"""REA safe entry point for Hackingtool.

This is intentionally separate from the legacy installer and menu. It only
exposes operations explicitly approved for unattended, local execution.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import socket
import sys
from collections.abc import Sequence

ALLOWED_HOSTS = frozenset({"localhost"})


def resolve_localhost(host: str) -> dict[str, str]:
    """Resolve a fixed local fixture; fail closed before any other DNS lookup."""
    if host not in ALLOWED_HOSTS:
        raise ValueError("Only the explicit localhost fixture is permitted in safe mode")
    resolved = socket.gethostbyname(host)
    address = ipaddress.ip_address(resolved)
    if not address.is_loopback:
        raise RuntimeError("DNS resolution did not return a loopback address")
    return {"tool": "Host2IP", "hostname": host, "address": resolved, "scope": "loopback-only"}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Hackingtool safe local app (no install, scanning or external targets)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="Show available safe operations")
    host = sub.add_parser("host-to-ip", help="Resolve the harmless localhost fixture")
    host.add_argument("hostname", choices=sorted(ALLOWED_HOSTS))
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            result: dict[str, object] = {"safe_tools": [{"name": "Host2IP", "command": "host-to-ip localhost", "scope": "loopback-only"}]}
        elif args.command == "host-to-ip":
            result = resolve_localhost(args.hostname)
        else:
            parser.error("Unsupported operation")
            return 2
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "status": "blocked"}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
