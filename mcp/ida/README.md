# IDA MCP integration

This repository standardizes on [`mrexodia/ida-pro-mcp`](https://github.com/mrexodia/ida-pro-mcp) for IDA-backed skills. Do not describe MCP access abstractly when the skill actually expects this server.

## Baseline install

Facts from the upstream README:
- `ida-pro-mcp` requires Python 3.11+.
- It targets IDA Pro 8.3+ and recommends 9.x.
- Installation is:

```bash
pip uninstall ida-pro-mcp
pip install https://github.com/mrexodia/ida-pro-mcp/archive/refs/heads/main.zip
ida-pro-mcp --install
```

- `ida-pro-mcp --config` prints client config JSON for supported MCP clients.

Restart both IDA and the MCP client after install. Do not claim the server is available unless it is actually configured and reachable.

## Core tools this repo expects

These are the concrete `ida-pro-mcp` tools skills in this repo may call out:

- `list_funcs`
- `lookup_funcs`
- `decompile`
- `disasm`
- `xrefs_to`
- `callees`
- `callgraph`
- `find_regex`
- `find`
- `analyze_funcs`
- `export_funcs`
- `rename`
- `set_comments`
- `set_type`
- `infer_types`
- `py_eval`

Useful resources:
- `ida://idb/metadata`
- `ida://idb/segments`
- `ida://idb/entrypoints`
- `ida://xrefs/from/{addr}`
- `ida://types`
- `ida://structs`

Debugger-only workflows additionally use `dbg_*` tools and should be treated as a separate, higher-risk phase.

## Standard analyst sequence

Use this order unless a skill says otherwise:

1. `list_funcs` or `lookup_funcs` to confirm naming quality and entrypoints.
2. `decompile` the top function(s) under review.
3. `xrefs_to` for runtime pivots, imports, strings, or globals.
4. `find_regex` or `find` for missing strings and constants.
5. `analyze_funcs` for large handlers when manual stitching is slow.
6. `rename`, `set_comments`, and `set_type` only after evidence is sufficient.
7. `export_funcs` when a local helper script or external review needs stable text.

## Go-focused sequence

For stripped Go samples:

1. `list_funcs("main")` or equivalent filter to enumerate `main.*`.
2. `decompile` `main.main`, `main.init`, and large non-runtime functions.
3. `xrefs_to`:
   - `runtime.newproc`
   - `runtime.newproc1`
   - `runtime.makechan`
   - `runtime.chansend*`
   - `runtime.chanrecv*`
   - `runtime.selectgo`
   - `runtime.newobject`
4. `find_regex` for URLs, domains, shell strings, service names, config paths.
5. `export_funcs` for the top user functions, then run:

```bash
python3 skills/reverse-golang-malware/scripts/goroutine_hotspots.py exported.txt
```

Related helper scripts:
- `skills/reverse-golang-symbol-recovery/scripts/extract_buildinfo.py`
- `skills/reverse-golang-symbol-recovery/scripts/go_inventory.py`
- `skills/reverse-golang-malware/scripts/goroutine_hotspots.py`

## Rust-focused sequence

For stripped Rust samples:

1. `find_regex` for panic strings, crate paths, and command words.
2. `list_funcs` and `lookup_funcs` around recovered crate or module names.
3. `decompile` branch-heavy handlers and allocator-adjacent logic.
4. `xrefs_to` for command words, panic paths, and network imports.
5. `callgraph` from likely dispatchers before renaming.

## Protocol-focused sequence

When reconstructing protocol flow:

1. `find_regex` for command strings, JSON keys, opcodes, and framing markers.
2. `xrefs_to` those strings or constants.
3. `decompile` decode, dispatch, and encode candidates.
4. `callgraph` from the receive path or central handler.
5. `export_funcs` relevant functions if local diffing or field extraction is needed.

## Important rule

Never imply an MCP action ran unless it actually ran.

## Claude Code and Codex

- Claude Code: add the server using your Claude MCP configuration, using the JSON emitted by `ida-pro-mcp --config` when needed.
- Codex: declare the dependency in `codex/overlays/<skill>/agents/openai.yaml`.
