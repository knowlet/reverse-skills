#!/usr/bin/env python3
r"""ida_panic_paths.py — `py_eval`-ready panic/source path harvester.

Designed to be pasted into `ida-pro-mcp.py_eval`. Reads bytes from
`.rodata` via IDA's API, extracts Rust source paths and panic strings,
and returns a compact list of `(ea, path)` tuples so the analyst can
jump straight to the referencing instruction.

Paste this into `py_eval` inside IDA
------------------------------------

```python
# -- BEGIN IDA WRAPPER --
import re, ida_bytes, ida_segment

SOURCE_PATH_RE = re.compile(
    rb'(?:/[\w.+@\-]+)+\.rs(?::\d+(?::\d+)?)?'
    rb'|[A-Z]:\\[\w\\.+@\-]+\.rs'
)

def _seg_bytes(name):
    s = ida_segment.get_segm_by_name(name)
    if s is None:
        return None, None
    return s.start_ea, ida_bytes.get_bytes(s.start_ea, s.end_ea - s.start_ea)

def ida_find_panic_paths(seg=".rodata", limit=500):
    base, buf = _seg_bytes(seg)
    if buf is None:
        return f"no segment {seg}"
    out, seen = [], set()
    for m in SOURCE_PATH_RE.finditer(buf):
        path = m.group(0).decode("latin-1", "replace")
        if path in seen:
            continue
        seen.add(path)
        out.append((base + m.start(), path))
        if len(out) >= limit:
            break
    return out

ida_find_panic_paths(".rodata", 500)
# -- END IDA WRAPPER --
```

After you get the `(ea, path)` list back, the natural next step is:

    for ea, path in result:
        # For each address, run ida-pro-mcp xrefs_to <ea> and record
        # the caller. The caller is the function that panics on that
        # source line — very often a dispatcher or parser.

Standalone usage
----------------
    ida_panic_paths.py sample.bin
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SOURCE_PATH_RE = re.compile(
    rb"(?:/[\w.+@\-]+)+\.rs(?::\d+(?::\d+)?)?"
    rb"|[A-Z]:\\[\w\\.+@\-]+\.rs"
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Standalone panic path scanner.")
    ap.add_argument("sample", type=Path)
    args = ap.parse_args()

    data = args.sample.read_bytes()
    seen: set[str] = set()
    for m in SOURCE_PATH_RE.finditer(data):
        path = m.group(0).decode("latin-1", "replace")
        if path in seen:
            continue
        seen.add(path)
        print(path)
    print(f"# unique paths: {len(seen)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
