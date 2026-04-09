# External Resources — Golang Reverse Engineering

Curated starting points for **stripped Go binaries**, malware-oriented symbol recovery, and tooling. Prefer primary repos and vendor blogs; verify versions against your sample’s Go toolchain.

## Official and vendor deep dives

| Resource | Notes |
| --- | --- |
| [Mandiant — Ready, Set, Go (Golang internals & symbol recovery)](https://www.mandiant.com/resources/blog/golang-internals-symbol-recovery) | pclntab, buildinfo, recovery workflow |
| [Google Cloud — Golang internals and symbol recovery](https://cloud.google.com/blog/topics/threat-intelligence/golang-internals-symbol-recovery/) | Mirror/variant of the Mandiant technical narrative |

## Open-source tools (actively used in practice)

| Tool | Role |
| --- | --- |
| [GoReSym](https://github.com/mandiant/GoReSym) | Metadata, functions, types; JSON and IDA integration paths |
| [go-re.tk / GoRE / Redress](https://go-re.tk/) | Redress CLI for packages, std/vendor/file paths |
| [AlphaGolang](https://github.com/SentineLabs/AlphaGolang) | IDA-oriented scripts for pclntab-oriented recovery |
| [binjago](https://github.com/W3ndige/binjago) | Binary Ninja helpers for stripped Go |

## Practitioner writeups

| Resource | Notes |
| --- | --- |
| [Golang Reverse Engineering Tips (Travis Mathison)](https://tdmathison.github.io/posts/Golang-Reverse-Engineering-Tips/) | IDA-focused practical notes |
| [Notes, tools, techniques for RE Go binaries (gist)](https://gist.github.com/0xdevalias/4e430914124c3fd2c51cb7ac2801acba) | Broad link collection |

## Using this list in skills

- Pair **GoReSym/Redress** output with `scripts/go_inventory.py` in this repository when JSON inventory is needed.
- When the disassembler’s Go support is weak, **recover names first**, then return to behavior analysis under `reverse-golang-malware`.
