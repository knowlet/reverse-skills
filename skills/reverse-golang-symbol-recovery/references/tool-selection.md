# Tool Selection For Go Symbol Recovery

Use this reference to choose the lightest reliable path for recovering names and structure from a Go binary.

## Selection order

1. native disassembler support
2. Go-aware metadata parsers
3. version-aware renaming scripts
4. manual pclntab and moduledata work

## Tool matrix

| Tool or path | Best use | Strength | Limitation |
| --- | --- | --- | --- |
| Native IDA Go support | newer IDA databases that already detect Go well | fast first pass and package grouping | may still miss types, paths, or packed edge cases |
| GoReSym | stripped, malformed, packed, or version-sensitive samples | version-aware recovery of metadata, paths, types, strings, user and std functions | output still needs analyst triage |
| Redress | reconstructing packages, source layout, types, and radare2 workflows | package filtering, type extraction, source-layout projection | not a replacement for manual verification |
| Ghidra `go_func.py` | renaming functions in Ghidra from pclntab | version-aware rename path for PE and ELF samples | narrower than full metadata recovery |
| Manual pclntab and moduledata parsing | damaged or adversarial binaries | works when tools partially fail | slow and error-prone |

## Practical heuristics

- If the disassembler already gave you `main.*` and clean package folders, keep that output and do not redo everything.
- If the binary is stripped, malformed after unpacking, or version detection is shaky, prefer GoReSym first.
- If you need type definitions, package grouping, or source-layout clues, Redress is a strong complement.
- If you are in Ghidra and mostly need function renaming, run a version-aware pclntab script before doing deeper manual analysis.

## What to record

- recovered Go version or version range
- build ID and module path
- package inventory split into user, vendor, std, and runtime
- recovered file paths
- top functions worth reviewing first

## Further reading

See [external-resources.md](external-resources.md) for Mandiant/Google posts, GoReSym, Redress, AlphaGolang, and curated articles.
