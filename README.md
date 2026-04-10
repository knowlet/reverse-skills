# reverse-skills

Reusable reverse engineering and malware analysis skills for open agent ecosystems.

This repository is designed to work well with:
- Claude Code
- Codex
- other agents supported by the open skills ecosystem

## Install

Install the whole repository as a skill source:

```bash
npx skills add knowlet/reverse-skills
```

Install a specific skill:

```bash
npx skills add knowlet/reverse-skills --skill reverse-malware-triage
npx skills add knowlet/reverse-skills --skill reverse-ida-mcp-driver
npx skills add knowlet/reverse-skills --skill reverse-rust-malware
npx skills add knowlet/reverse-skills --skill reverse-golang-symbol-recovery
npx skills add knowlet/reverse-skills --skill reverse-golang-malware
npx skills add knowlet/reverse-skills --skill reverse-protocol-reconstruction
npx skills add knowlet/reverse-skills --skill reverse-operator-attribution
npx skills add knowlet/reverse-skills --skill reverse-botnet-dismantling
npx skills add knowlet/reverse-skills --skill reverse-reporting
```

## Skills

- `reverse-malware-triage`
  Fast binary triage, capability inventory, IOC extraction, and next
  pivots. Now ships `scripts/quick_triage.sh`, `scripts/entropy.py`,
  and `scripts/string_clusters.py` for one-shot identity + packer +
  signature + clustered-string snapshots.

- `reverse-ida-mcp-driver`
  Drive `ida-pro-mcp` efficiently: structured "survey this binary"
  prompts, dispatcher-location heuristics, handler fan-out discipline,
  cost-budgeted tool sequencing, and `py_eval`-ready scripts for
  `.rodata` byte-scanning, panic-path extraction, and Go pclntab
  discovery. Use whenever an IDA MCP server is connected.

- `reverse-rust-malware`
  Workflow for stripped/static Rust samples: string recovery via a
  byte-by-byte `.rodata` scanner, panic-path module-tree
  reconstruction, fingerprint mining (users, crates, rustc versions,
  typos), memory-dump peer extraction, and dispatcher discovery.

- `reverse-golang-symbol-recovery`
  Recover package names, build metadata, types, and source-layout
  clues from stripped Go binaries. Includes a `pclntab_finder.py` that
  locates the magic header across Go 1.2 / 1.16 / 1.18 / 1.20 even when
  the section name is stripped, and a GoResolver fallback pointer for
  Garble-obfuscated samples.

- `reverse-golang-malware`
  Workflow for stripped/packed Go samples: isolate user logic, map
  goroutines, extract artifacts, and assess behavior.

- `reverse-protocol-reconstruction`
  Recover command flow, field candidates, encode/decode boundaries,
  and protocol behavior.

- `reverse-operator-attribution`
  Pivot from malware artifacts to operator or developer hypotheses and
  prioritized investigative actions.

- `reverse-botnet-dismantling`
  Turn reconstructed control-plane evidence into ranked disruption,
  containment, and monitoring options.

- `reverse-reporting`
  Turn analysis into an operator-ready or analyst-ready report with
  confidence labels.

## Design principles

- Separate facts, inferences, and hypotheses.
- Never claim a tool was executed unless it was actually executed.
- Prefer concrete command sequences and exact MCP tool names over generic "capability" language.
- Prefer workflow skills over giant monolithic prompts.
- Keep core skills agent-agnostic.
- Put Codex-specific metadata under `codex/overlays/`.
- Keep only verified MCP integrations under `mcp/`.

## Claude Code and Codex

Core skills live in `skills/<name>/SKILL.md`.

For Codex-specific metadata and MCP dependency declarations, see:
- `codex/overlays/<skill>/agents/openai.yaml`

For concrete IDA integration, see:
- `mcp/ida/README.md`

This repo standardizes on `mrexodia/ida-pro-mcp` for IDA-backed workflows and expects skills to call out actual tool names such as `decompile`, `xrefs_to`, `find_regex`, `export_funcs`, `rename`, and `set_type` when MCP-driven analysis is part of the workflow.

## Recommended usage order

1. `reverse-malware-triage` (optionally wrap with `scripts/quick_triage.sh`)
2. `reverse-ida-mcp-driver` for the structured first-pass survey when
   IDA Pro is available
3. `reverse-golang-symbol-recovery` when a Go sample is noisy or stripped
4. `reverse-rust-malware` or `reverse-golang-malware` or another family-specific skill
5. `reverse-protocol-reconstruction`
6. `reverse-operator-attribution`
7. `reverse-botnet-dismantling`
8. `reverse-reporting`
