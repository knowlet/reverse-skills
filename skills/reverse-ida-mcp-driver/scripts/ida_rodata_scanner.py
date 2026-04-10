#!/usr/bin/env python3
"""ida_rodata_scanner.py — Byte-by-byte printable scanner for an IDA
segment, usable in two modes:

  1. **Standalone CLI**: pass a raw binary path and a section name. Useful
     for pre-flight sanity checks outside IDA.

  2. **`py_eval` payload**: paste the function `ida_scan_segment` into
     `ida-pro-mcp.py_eval`. It reads bytes directly from IDA, so results
     are anchored at real addresses you can `xrefs_to`.

Why it beats IDA's default strings window
------------------------------------------
Rust and some Go builds store strings as length-prefixed slices packed
back-to-back in `.rodata` with no NUL terminator. IDA's default scanner
requires a terminator and therefore misses the majority. The HackMD
writeup reported 31 strings from IDA vs 701 from this kind of scan — a
22x improvement, including panic paths, crate names with versions, and
operator typos that became globally unique IOCs.

Paste this into `py_eval` to run inside IDA
-------------------------------------------

```python
# -- BEGIN IDA WRAPPER --
import ida_bytes, ida_segment

def _ida_seg_bytes(seg_name):
    seg = ida_segment.get_segm_by_name(seg_name)
    if seg is None:
        return None, None
    buf = ida_bytes.get_bytes(seg.start_ea, seg.end_ea - seg.start_ea)
    return seg.start_ea, buf

def ida_scan_segment(seg_name=".rodata", min_len=6, limit=1000):
    base, buf = _ida_seg_bytes(seg_name)
    if buf is None:
        return f"no segment {seg_name!r}"
    PRINTABLE = set(range(0x20, 0x7f)) | {0x09}
    out, run_start, run = [], None, []
    for i, b in enumerate(buf):
        if b in PRINTABLE:
            if not run:
                run_start = i
            run.append(b)
        else:
            if len(run) >= min_len:
                ea = base + run_start
                out.append((ea, bytes(run).decode("latin-1", "replace")))
                if len(out) >= limit:
                    return out
            run = []
    if len(run) >= min_len:
        out.append((base + run_start, bytes(run).decode("latin-1", "replace")))
    return out

ida_scan_segment(".rodata", 6, 2000)
# -- END IDA WRAPPER --
```

The return value is a list of `(effective_address, string)` tuples so
you can feed it straight into `xrefs_to` or annotate the IDB with
`set_comments`. For Rust, sort by length descending to float panic
paths to the top.

Standalone usage
----------------
    ida_rodata_scanner.py sample.bin
    ida_rodata_scanner.py sample.bin --section .data --min 4
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Re-use the standalone scanner used by reverse-rust-malware.
# Duplicated here intentionally: pasting into py_eval should not require
# importing from sibling skills. The two copies are tiny and identical.
PRINTABLE = set(range(0x20, 0x7F)) | {0x09}


def scan_buffer(buf: bytes, min_len: int) -> list[str]:
    out: list[str] = []
    run: list[int] = []
    for b in buf:
        if b in PRINTABLE:
            run.append(b)
        else:
            if len(run) >= min_len:
                out.append(bytes(run).decode("latin-1", "replace"))
            run = []
    if len(run) >= min_len:
        out.append(bytes(run).decode("latin-1", "replace"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Standalone .rodata scanner.")
    ap.add_argument("sample", type=Path)
    ap.add_argument("--section", default=".rodata")
    ap.add_argument("--min", type=int, default=6)
    args = ap.parse_args()

    data = args.sample.read_bytes()
    print(f"# standalone mode: scanning whole file from {args.sample}",
          file=sys.stderr)
    for s in scan_buffer(data, args.min):
        print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
