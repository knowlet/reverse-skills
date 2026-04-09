# IDA MCP integration

This directory documents the expected MCP tooling for IDA-based workflows.

## Intended use

The reverse-engineering skills in this repository may assume availability of an IDA-oriented MCP tool capable of:
- listing functions
- reading strings
- reading xrefs
- exporting disassembly or pseudocode
- running analysis-side helper scripts

## Important rule

Skills may depend on this tool conceptually, but must never claim it was executed unless it actually ran.

## Claude Code

Configure the MCP server in Claude Code using your normal Claude MCP setup.

## Codex

Declare the dependency through the Codex overlay in:
`codex/overlays/<skill>/agents/openai.yaml`
