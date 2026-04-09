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
npx skills add knowlet/reverse-skills --skill reverse-malware-triage
npx skills add knowlet/reverse-skills --skill reverse-protocol-reconstruction
```

## Skills

- `reverse-malware-triage`
  Fast binary triage, capability inventory, IOC extraction, and next pivots.

- `reverse-rust-malware`
  Workflow for stripped/static Rust samples: string recovery, panic-path reconstruction, module tree building, dispatcher discovery.

- `reverse-protocol-reconstruction`
  Recover command flow, field candidates, encode/decode boundaries, and protocol behavior.

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
2. `reverse-rust-malware` or another family/tool-specific skill
3. `reverse-protocol-reconstruction`
4. `reverse-reporting`
