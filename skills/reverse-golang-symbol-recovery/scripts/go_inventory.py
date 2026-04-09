#!/usr/bin/env python3
"""Summarize GoReSym JSON into a practical user-code inventory."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def get_name(entry: object) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        for key in ("Name", "name", "FullName", "full_name", "Symbol", "symbol"):
            value = entry.get(key)
            if isinstance(value, str):
                return value
    return str(entry)


def normalize_package(symbol_name: str) -> str:
    if ".(" in symbol_name:
        return symbol_name.split(".(", 1)[0]

    trimmed = symbol_name
    while "." in trimmed:
        head, tail = trimmed.rsplit(".", 1)
        if tail.startswith("func") and tail[4:].isdigit():
            trimmed = head
            continue
        if tail in {"deferwrap", "stub", "abi0", "abiinternal"}:
            trimmed = head
            continue
        break

    if "." not in trimmed:
        return trimmed
    return trimmed.rsplit(".", 1)[0]


def summarize(goresym: dict[str, object], limit: int) -> dict[str, object]:
    user_functions = goresym.get("UserFunctions", [])
    std_functions = goresym.get("StdFunctions", [])
    files = goresym.get("Files", [])
    types = goresym.get("Types", [])

    user_names = [get_name(entry) for entry in user_functions]
    std_names = [get_name(entry) for entry in std_functions]
    package_counts = Counter(normalize_package(name) for name in user_names if name)

    file_paths: list[str] = []
    for entry in files:
        if isinstance(entry, str):
            file_paths.append(entry)
        elif isinstance(entry, dict):
            for key in ("Path", "path", "Name", "name"):
                value = entry.get(key)
                if isinstance(value, str):
                    file_paths.append(value)
                    break

    build_info = goresym.get("BuildInfo", {}) if isinstance(goresym.get("BuildInfo"), dict) else {}
    summary = {
        "go_version": goresym.get("Version") or build_info.get("GoVersion"),
        "build_id": goresym.get("BuildId"),
        "main_path": build_info.get("Path"),
        "user_function_count": len(user_names),
        "std_function_count": len(std_names),
        "type_count": len(types) if isinstance(types, list) else 0,
        "top_user_packages": package_counts.most_common(limit),
        "main_candidates": [name for name in user_names if name.startswith("main.")][:limit],
        "file_paths": file_paths[:limit],
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goresym_json", help="Path to GoReSym JSON output")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    parser.add_argument("--limit", type=int, default=10, help="Max rows for summaries")
    args = parser.parse_args()

    path = Path(args.goresym_json)
    payload = json.loads(path.read_text())
    summary = summarize(payload, args.limit)

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    print(f"Go version: {summary.get('go_version') or 'unknown'}")
    print(f"Build ID: {summary.get('build_id') or 'unknown'}")
    print(f"Main path: {summary.get('main_path') or 'unknown'}")
    print(f"User functions: {summary['user_function_count']}")
    print(f"Std functions: {summary['std_function_count']}")
    print(f"Types: {summary['type_count']}")

    print("Top user packages:")
    for package_name, count in summary["top_user_packages"]:
        print(f"  - {package_name}: {count}")

    if summary["main_candidates"]:
        print("Main candidates:")
        for name in summary["main_candidates"]:
            print(f"  - {name}")

    if summary["file_paths"]:
        print("File paths:")
        for path_name in summary["file_paths"]:
            print(f"  - {path_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
