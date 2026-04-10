#!/usr/bin/env python3
"""ida_pclntab_finder.py — Locate Go `pclntab` magic headers in a binary.

Context
-------
When Go binaries are stripped, the `.symtab` is zeroed out but the
`.gopclntab` data itself is almost always still present — it is
critical to the Go runtime for stack traces, garbage collection root
scanning, and defer handling, so stripping it would break the binary.
The pclntab maps every function's address to its name, file, and line
range. Recovering it effectively undoes the stripping of user code.

The magic header changed between Go versions:

  * Go 1.2  → 0xfffffffb
  * Go 1.16 → 0xfffffffa
  * Go 1.18 → 0xfffffff0
  * Go 1.20 → 0xfffffff1

After the magic, the header continues with `00 00 <pc quantum>
<ptrsize>`. We scan for any of the magics followed by `\x00\x00` and
emit the candidate offset. This matches both little- and big-endian
variants and gives the analyst a single stable pivot for:

    * reading function count and first function address
    * building a name table that IDA can re-apply via `set_name`
    * triangulating the Go version

Usage as `py_eval` payload
--------------------------

```python
# -- BEGIN IDA WRAPPER --
import struct, ida_bytes, idaapi

MAGICS = [0xfffffffb, 0xfffffffa, 0xfffffff0, 0xfffffff1]

def ida_find_pclntab():
    info = idaapi.get_inf_structure()
    min_ea = info.min_ea
    max_ea = info.max_ea
    size = max_ea - min_ea
    # Limit to 64 MiB for safety; raise if larger binary.
    if size > 64 * 1024 * 1024:
        size = 64 * 1024 * 1024
    buf = ida_bytes.get_bytes(min_ea, size) or b""
    hits = []
    for magic in MAGICS:
        for endian in ("<I", ">I"):
            magic_b = struct.pack(endian, magic)
            off = 0
            while True:
                idx = buf.find(magic_b, off)
                if idx < 0:
                    break
                # Header continues with 00 00 pc_q ptr_size
                tail = buf[idx + 4 : idx + 8]
                if len(tail) == 4 and tail[:2] == b"\x00\x00":
                    pc_q, ptr_sz = tail[2], tail[3]
                    hits.append({
                        "ea": hex(min_ea + idx),
                        "magic": hex(magic),
                        "endian": endian,
                        "pc_quantum": pc_q,
                        "ptr_size": ptr_sz,
                    })
                off = idx + 1
    return hits

ida_find_pclntab()
# -- END IDA WRAPPER --
```

Standalone usage
----------------
    ida_pclntab_finder.py sample.bin
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

MAGICS = [0xFFFFFFFB, 0xFFFFFFFA, 0xFFFFFFF0, 0xFFFFFFF1]


def find_pclntab(data: bytes) -> list[dict]:
    hits: list[dict] = []
    for magic in MAGICS:
        for endian in ("<I", ">I"):
            magic_b = struct.pack(endian, magic)
            off = 0
            while True:
                idx = data.find(magic_b, off)
                if idx < 0:
                    break
                tail = data[idx + 4 : idx + 8]
                if len(tail) == 4 and tail[:2] == b"\x00\x00":
                    hits.append(
                        {
                            "offset": idx,
                            "magic": hex(magic),
                            "endian": endian,
                            "pc_quantum": tail[2],
                            "ptr_size": tail[3],
                        }
                    )
                off = idx + 1
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sample", type=Path)
    args = ap.parse_args()

    data = args.sample.read_bytes()
    hits = find_pclntab(data)
    if not hits:
        print("no pclntab candidates found", file=sys.stderr)
        return 1

    print(f"{'offset':<12} {'magic':<12} {'endian':<8} pc_q  ptrsz")
    for h in hits:
        print(f"0x{h['offset']:08x} {h['magic']:<12} {h['endian']:<8} "
              f"{h['pc_quantum']:<5} {h['ptr_size']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
