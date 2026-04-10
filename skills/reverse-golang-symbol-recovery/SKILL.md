---
name: reverse-golang-symbol-recovery
description: Use this skill when stripped, packed, or poorly labeled Go binaries need function names, package paths, build metadata, source layout clues, types, or interfaces recovered from build info, pclntab, moduledata, typelinks, or tool-specific metadata before deeper malware analysis. Use when triaging with binwalk/strings/go version -m/GoReSym/redress, when IDA or Ghidra shows too few strings versus strings(1), or when preparing concrete `ida-pro-mcp` rename and xref workflows for pclntab-anchored recovery.
---

# Reverse Golang Symbol Recovery

Use this skill when a Go binary is recognizable but the disassembler view is still too noisy to separate user logic from runtime and library code.

## Guardrails

- Confirm the sample is Go before applying Go-specific assumptions.
- Separate recovered metadata from inferred source structure.
- Record the recovered Go version or version range because metadata layouts change across releases.
- Treat tool output as leads to verify, not ground truth.
- Distinguish user packages from standard library, vendor, and runtime packages.

## Inputs

Prioritize:
- binary format, architecture, and stripped status
- build info, BuildID, compiler version, and module path
- `.gopclntab` or equivalent pclntab location
- `moduledata`, typelinks, and itablinks
- existing names recovered by IDA, Ghidra, Binary Ninja, or radare2
- file paths, package paths, and `main.main` / `main.init` candidates

If tool selection is unclear, read `references/tool-selection.md`.

If concrete commands or `ida-pro-mcp` actions are needed, read `references/practical-commands.md`.

For curated blogs, tools (GoReSym, Redress, AlphaGolang), and practitioner links, read `references/external-resources.md`.

If a deliverable is needed, use `assets/recovery-template.md`.

## Workflow

### Phase 1: confirm Go and version context

Start with the fastest local checks:

```bash
file sample.bin
sha256sum sample.bin
binwalk sample.bin                         # signature scan; add -Me to extract
go version -m sample.bin
go tool buildid sample.bin
python3 scripts/extract_buildinfo.py sample.bin
python3 scripts/pclntab_finder.py sample.bin   # locate pclntab even when stripped
```

Look for:
- `.gopclntab`
- `runtime.` or `type.` symbols
- Go build info or BuildID
- package paths embedded in the binary

`pclntab_finder.py` finds the pclntab magic header (`0xfffffffb` for Go
1.2, `0xfffffffa` for 1.16, `0xfffffff0` for 1.18, `0xfffffff1` for 1.20)
even when the `.symtab` and section names are stripped. It reports
offset, endian, pc quantum, and pointer size — exactly what you need to
manually define a `.gopclntab` segment in IDA and undo the stripping.
There is a `py_eval`-ready wrapper in
`../reverse-ida-mcp-driver/scripts/ida_pclntab_finder.py` for running it
inside IDA directly.

Prefer the most direct version source available. If version recovery is weak, record a range instead of guessing an exact version.

### Phase 2: recover names and package boundaries

Prefer this order:
1. native disassembler Go support if it already produced usable names
2. Go-aware metadata parsers (GoReSym, Redress)
3. version-aware scripts that rename from pclntab
4. **CFG-similarity matching (GoResolver)** when steps 1-3 recover very
   few names — that usually means the sample was obfuscated with Garble
   and metadata-based tools have nothing to chew on. See
   `references/external-resources.md` for the GoResolver entry and
   pointer to the Volexity writeup.

Recover:
- `main.main`
- `main.init` and chained init functions
- user packages
- standard library and runtime packages
- file paths if present

Common recovery sequence:

```bash
strings -a -n 8 sample.bin | rg 'go1\\.|main\\.|runtime\\.|github\\.com/|gitlab\\.com/|/src/'
GoReSym -t -d -p sample.bin > goresym.json
python3 scripts/go_inventory.py goresym.json
redress info sample.bin
redress packages sample.bin --std --vendor --filepath
redress source sample.bin
```

If `ida-pro-mcp` is connected, run:
- `list_funcs` for `main` and recovered user-package prefixes
- `lookup_funcs` plus `decompile` for `main.main` and chained init functions
- `xrefs_to` for `runtime.newobject`, `runtime.morestack`, `runtime.newproc`, and `runtime.selectgo`
- `find_regex` for module paths, source paths, config strings, and URLs
- `export_funcs` for the top user packages before bulk renaming

Do not use `rename` until build metadata, package ownership, and runtime pivots agree.

### Phase 3: recover types and interfaces

Use `moduledata`, typelinks, itablinks, and constructor sites to recover:
- structs
- interfaces
- methods
- package-owned types

Prioritize types referenced near:
- `runtime.newobject`
- network handlers
- config loaders
- crypto setup
- command dispatch

### Phase 4: rebuild the analyst view

Produce:
- a clean package inventory
- a user-code shortlist
- important functions to inspect first
- unresolved regions that still need manual work

Minimum artifact bundle:
- `file`, `sha256sum`, `go version -m`, and BuildID output
- strings hits for module paths and IOCs
- GoReSym or Redress inventory
- `ida-pro-mcp` exports only if the MCP actually ran

If author logic is now visible, hand off to `reverse-golang-malware`.

If protocol recovery becomes central, hand off to `reverse-protocol-reconstruction`.

## Output format

# Go Symbol Recovery Summary

## Executive Summary
[2-5 sentences]

## Facts
- 
- 

## Inferences
- 
- 

## Unknowns
- 
- 

## Build Metadata
- 
- 

## Recovered Packages and Functions
- 
- 

## Type and Interface Leads
- 
- 

## Recommended Next Actions
1.
2.
3.
