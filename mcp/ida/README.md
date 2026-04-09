# IDA MCP integration

This directory documents the expected MCP tooling for IDA-based workflows.

## Intended use

The reverse-engineering skills in this repository may assume availability of an IDA-oriented MCP tool capable of:
- listing functions
- reading strings
- reading xrefs
- exporting disassembly or pseudocode
- running analysis-side helper scripts

## AI-assisted cadence

Skills under `skills/reverse-golang-malware/references/ai-assisted-field-manual.md` describe how to combine **human pivot selection** with **MCP-backed breadth** (survey, string-gap checks, large-handler decompilation). The same MCP dependency applies.

## Go-focused workflow

For stripped Go samples, a practical MCP sequence is:

1. list user-package functions under `main` and any recovered non-stdlib package prefixes
2. decompile `main.main`, init functions, and large user handlers
3. retrieve xrefs to `runtime.newproc`, `runtime.newproc1`, `runtime.makechan`, `runtime.selectgo`, and `runtime.newobject`
4. list strings and xrefs mentioning URLs, config paths, shell execution, TLS, DNS, and persistence paths
5. export pseudocode for top candidates so local helper scripts can score goroutine hotspots

The repository's Go skills include helper scripts that can be used after these exports:
- `skills/reverse-golang-symbol-recovery/scripts/extract_buildinfo.py`
- `skills/reverse-golang-symbol-recovery/scripts/go_inventory.py`
- `skills/reverse-golang-malware/scripts/goroutine_hotspots.py`

## Important rule

Skills may depend on this tool conceptually, but must never claim it was executed unless it actually ran.

## Claude Code

Configure the MCP server in Claude Code using your normal Claude MCP setup.

## Codex

Declare the dependency through the Codex overlay in:
`codex/overlays/<skill>/agents/openai.yaml`
