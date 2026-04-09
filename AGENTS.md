# Repository guidance

This repository contains reusable reverse-engineering skills.

## Global rules

- Prioritize truth over convenience.
- Explicitly separate:
  - Facts
  - Inferences
  - Hypotheses
- Never imply a script, tool, or MCP action ran unless it actually ran.
- Prefer compact, analyst-grade outputs over long generic prose.
- When uncertain, say what is unknown and what evidence would reduce uncertainty.
- Use workflow skills before tool-specific micro-optimizations.

## Structure

- `skills/`
  Agent-agnostic skills intended to work across open skills ecosystems.

- `codex/overlays/`
  Codex-only overlays such as `agents/openai.yaml`.

- `mcp/`
  MCP tool setup notes, wrappers, and server-specific documentation.

## Reporting expectations

Outputs should usually include:
1. Executive summary
2. Facts
3. Inferences
4. Unknowns
5. Recommended next actions
