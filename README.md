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
npx skills add knowlet/reverse-skills --skill reverse-rust-malware
npx skills add knowlet/reverse-skills --skill reverse-golang-symbol-recovery
npx skills add knowlet/reverse-skills --skill reverse-golang-malware
npx skills add knowlet/reverse-skills --skill reverse-malware-triage
npx skills add knowlet/reverse-skills --skill reverse-protocol-reconstruction
npx skills add knowlet/reverse-skills --skill reverse-operator-attribution
npx skills add knowlet/reverse-skills --skill reverse-botnet-dismantling
```

## Skills

- `reverse-malware-triage`
  Fast binary triage, capability inventory, IOC extraction, and next pivots.

- `reverse-rust-malware`
  Workflow for stripped/static Rust samples: string recovery, panic-path reconstruction, module tree building, dispatcher discovery.

- `reverse-golang-symbol-recovery`
  Recover package names, build metadata, types, and source-layout clues from stripped Go binaries.

- `reverse-golang-malware`
  Workflow for stripped/packed Go samples: isolate user logic, map goroutines, extract artifacts, and assess behavior.

- `reverse-protocol-reconstruction`
  Recover command flow, field candidates, encode/decode boundaries, and protocol behavior.

- `reverse-operator-attribution`
  Pivot from malware artifacts to operator or developer hypotheses and prioritized investigative actions.

- `reverse-botnet-dismantling`
  Turn reconstructed control-plane evidence into ranked disruption, containment, and monitoring options.

- `reverse-reporting`
  Turn analysis into an operator-ready or analyst-ready report with confidence labels.

## Design principles

- Separate facts, inferences, and hypotheses.
- Never claim a tool was executed unless it was actually executed.
- Prefer workflow skills over giant monolithic prompts.
- Keep core skills agent-agnostic.
- Put Codex-specific metadata under `codex/overlays/`.
- Put MCP setup and tool-specific notes under `mcp/`.

## Claude Code and Codex

Core skills live in `skills/<name>/SKILL.md`.

For Codex-specific metadata and MCP dependency declarations, see:
- `codex/overlays/<skill>/agents/openai.yaml`

For MCP setup references, see:
- `mcp/`

## Recommended usage order

1. `reverse-malware-triage`
2. `reverse-golang-symbol-recovery` when a Go sample is noisy or stripped
3. `reverse-rust-malware` or `reverse-golang-malware` or another family-specific skill
4. `reverse-protocol-reconstruction`
5. `reverse-operator-attribution`
6. `reverse-botnet-dismantling`
7. `reverse-reporting`
