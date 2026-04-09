#!/usr/bin/env python3
"""Extract Go build metadata with a practical `go` tool path and a heuristic fallback."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ASCII_RE = re.compile(rb"[\x20-\x7e]{8,}")
GO_VERSION_RE = re.compile(rb"\bgo1\.\d+(?:\.\d+)?(?:[a-z0-9-]+)?\b")
BUILD_ID_RE = re.compile(rb"\b[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{8,}\b")
MODULE_PATH_RE = re.compile(
    rb"\b(?:github\.com|gitlab\.com|bitbucket\.org|gopkg\.in|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
    rb"/[A-Za-z0-9_.\-/]{3,}\b"
)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def run_command(argv: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(argv, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def parse_go_version_m(stdout: str) -> dict[str, object]:
    result: dict[str, object] = {
        "source": "go version -m",
        "go_version": None,
        "build_id": None,
        "main_path": None,
        "module_path": None,
        "module_version": None,
        "dependencies": [],
        "build_settings": {},
    }

    lines = [line.rstrip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        return result

    if ":" in lines[0]:
        _, version = lines[0].split(":", 1)
        result["go_version"] = version.strip() or None

    dependencies: list[dict[str, str | None]] = []
    build_settings: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        parts = stripped.split("\t")
        if len(parts) < 2:
            continue
        key = parts[0]
        values = parts[1:]
        if key == "path":
            result["main_path"] = values[0]
        elif key == "mod":
            result["module_path"] = values[0]
            if len(values) > 1:
                result["module_version"] = values[1]
        elif key == "dep":
            dep: dict[str, str | None] = {
                "path": values[0],
                "version": values[1] if len(values) > 1 else None,
                "sum": values[2] if len(values) > 2 else None,
            }
            dependencies.append(dep)
        elif key == "build":
            build_value = values[0]
            if "=" in build_value:
                name, value = build_value.split("=", 1)
                build_settings[name] = value
            else:
                build_settings[build_value] = ""

    result["dependencies"] = dependencies
    result["build_settings"] = build_settings
    return result


def heuristic_scan(binary_path: Path) -> dict[str, object]:
    data = binary_path.read_bytes()
    ascii_strings = [match.group().decode("ascii", "ignore") for match in ASCII_RE.finditer(data)]
    versions = dedupe([match.group().decode("ascii", "ignore") for match in GO_VERSION_RE.finditer(data)])
    build_ids = dedupe([match.group().decode("ascii", "ignore") for match in BUILD_ID_RE.finditer(data)])
    module_paths = dedupe([match.group().decode("ascii", "ignore") for match in MODULE_PATH_RE.finditer(data)])

    likely_paths = [
        value
        for value in ascii_strings
        if "/" in value and " " not in value and len(value) < 200 and ("src/" in value or "/pkg/mod/" in value)
    ]

    return {
        "source": "heuristic-ascii-scan",
        "go_version": versions[0] if versions else None,
        "build_id": build_ids[0] if build_ids else None,
        "main_path": module_paths[0] if module_paths else None,
        "module_path_candidates": module_paths[:10],
        "source_path_candidates": dedupe(likely_paths)[:10],
        "version_candidates": versions[:10],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", help="Path to the suspected Go binary")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    parser.add_argument(
        "--no-go-tool",
        action="store_true",
        help="Skip `go version -m` and `go tool buildid`, use only heuristic scanning",
    )
    args = parser.parse_args()

    binary_path = Path(args.binary)
    if not binary_path.is_file():
        print(f"[ERROR] File not found: {binary_path}", file=sys.stderr)
        return 1

    result: dict[str, object]
    if not args.no_go_tool and shutil.which("go"):
        code, stdout, _ = run_command(["go", "version", "-m", str(binary_path)])
        if code == 0 and stdout.strip():
            result = parse_go_version_m(stdout)
            buildid_code, buildid_stdout, _ = run_command(["go", "tool", "buildid", str(binary_path)])
            if buildid_code == 0 and buildid_stdout.strip():
                result["build_id"] = buildid_stdout.strip()
        else:
            result = heuristic_scan(binary_path)
    else:
        result = heuristic_scan(binary_path)

    result["binary"] = str(binary_path)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"Binary: {result['binary']}")
    print(f"Source: {result.get('source')}")
    print(f"Go version: {result.get('go_version') or 'unknown'}")
    print(f"Build ID: {result.get('build_id') or 'unknown'}")
    if result.get("main_path"):
        print(f"Main path: {result['main_path']}")
    if result.get("module_path"):
        print(f"Module path: {result['module_path']}")
    if result.get("module_version"):
        print(f"Module version: {result['module_version']}")
    if result.get("module_path_candidates"):
        print("Module path candidates:")
        for candidate in result["module_path_candidates"]:
            print(f"  - {candidate}")
    if result.get("source_path_candidates"):
        print("Source path candidates:")
        for candidate in result["source_path_candidates"]:
            print(f"  - {candidate}")
    if result.get("dependencies"):
        print("Dependencies:")
        for dep in result["dependencies"][:10]:
            print(f"  - {dep['path']} {dep.get('version') or ''}".rstrip())
    if result.get("build_settings"):
        print("Build settings:")
        for key, value in sorted(result["build_settings"].items()):
            suffix = f"={value}" if value else ""
            print(f"  - {key}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
