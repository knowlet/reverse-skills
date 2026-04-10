---
name: reverse-ida-mcp-driver
description: Use this skill whenever an `ida-pro-mcp` server is connected and you need to drive IDA Pro efficiently for reverse engineering — structured "survey this binary" first passes, progressive deepening from big-picture to dispatcher-level detail, ready-to-paste `py_eval` helpers for `.rodata` string recovery, panic-path extraction, and pclntab discovery, and disciplined rules for when to `decompile`, `xrefs_to`, `find_regex`, `rename`, and `set_type`. Trigger on any task involving IDA MCP, IDA Pro workflows, stripped binary analysis when the disassembler is connected, or when an analyst asks Claude to "look at this IDB", "survey this binary", "find the dispatcher", or "recover symbols" with an IDA backend available. Complements `reverse-malware-triage`, `reverse-rust-malware`, `reverse-golang-symbol-recovery`, and `reverse-golang-malware`.
---

# Reverse IDA MCP Driver

Use this skill when `ida-pro-mcp` is connected and the agent is expected
to drive IDA Pro, not describe it abstractly. It captures a
reproducible, efficient analyst methodology for AI-assisted RE against
stripped native binaries. It is designed for workflows where a human
would otherwise click for hours, and optimized for the realistic cost
model: MCP calls and decompilations are not free, so we batch, we
prioritize, and we stop when the evidence is sufficient.

## Golden rules

1. **Never claim an MCP tool ran unless it actually ran.** Log the tool
   name, the arguments you passed, and the outcome. If an MCP call fails
   or times out, say so and fall back to CLI tooling rather than making
   up results.
2. **Survey before you rename.** The first pass produces a structured
   inventory: function count, entrypoints, top-N largest non-runtime
   functions, language/toolchain, packer hints, and candidate
   dispatcher. Renaming before that is how agents fabricate confident
   but wrong call graphs.
3. **Progressive deepening.** Big picture → dispatcher → handlers →
   types → field semantics. Do not jump straight to `set_type` on a
   struct you have only seen once.
4. **Prefer `find_regex` and `xrefs_to` to read-everything.** Exporting
   every function wastes tokens. A good analyst pulls the narrow
   function that explains the wide phenomenon.
5. **Use `py_eval` for things IDA cannot do by default.** Byte-level
   `.rodata` scanning, panic-path harvesting, pclntab discovery, and
   memory-dump correlation belong in `py_eval`, not in 100 `decompile`
   calls.
6. **Facts / Inferences / Hypotheses** must stay separated in the
   final analyst output. Decompiler pseudocode is an inference, not a
   fact. A string is a fact. The meaning of that string is a hypothesis
   until verified.

## Expected tool inventory

This skill expects `mrexodia/ida-pro-mcp` to be connected. The tool names
below are the exact names this repo targets. If a different IDA MCP
server is connected, map these to the equivalent tools and note the
mapping in the run log.

Core tools:
- `list_funcs`, `lookup_funcs`
- `decompile`, `disasm`
- `xrefs_to`, `callees`, `callgraph`
- `find_regex`, `find`
- `analyze_funcs`, `export_funcs`
- `rename`, `set_comments`, `set_type`, `infer_types`
- `py_eval`

Resources:
- `ida://idb/metadata`, `ida://idb/segments`, `ida://idb/entrypoints`
- `ida://xrefs/from/{addr}`, `ida://types`, `ida://structs`

See `../../mcp/ida/README.md` for install and configuration facts.

## Phase 1: "survey this binary" structured first pass

This is the prompt and tool sequence that turns a cold IDB into a
one-page triage report in under a minute of wall time. It is deliberate
about which tools run and in what order.

**Paste this as the opening prompt** after connecting to IDA:

> Survey this binary. Produce a one-page report with these sections:
> Executive summary, Identity (format, arch, stripped, language guess),
> Entrypoints, Top-10 largest non-runtime functions, Candidate
> dispatcher(s) with cyclomatic complexity, Networking/crypto hints,
> Panic or source path hints, Strings count (IDA view vs `.rodata`
> byte-scan). Separate facts from inferences. Do not rename anything.
> Use: `ida://idb/metadata`, `list_funcs`, `ida://idb/entrypoints`,
> `find_regex` for URLs/IPs/crypto markers, and `py_eval` for the
> byte-scan. Report the exact tools you called and how many results
> each returned.

Under the hood this produces the following MCP call sequence:

1. `ida://idb/metadata` — format, arch, processor, bitness, entry.
2. `ida://idb/entrypoints` — list entry symbols and addresses.
3. `list_funcs` — with a filter that excludes `runtime.`, `std::`,
   `core::`, `alloc::`, `tokio::`, `reqwest::`, `serde::` prefixes. If
   the IDB is stripped, use a size filter instead (>256 bytes).
4. `py_eval` with the `.rodata` scanner in
   `scripts/ida_rodata_scanner.py` (see below). Compare the count
   against IDA's native string window.
5. `find_regex` with the alternation bundle in
   `references/regex-bundles.md` — a single call covers URLs, IPs,
   domains, crypto markers, and shell paths.
6. `find_regex` for `\.rs:\d+|\.go:\d+|\.c:\d+` to pull source-path
   tail artefacts; for Rust also scan for
   `panicked at |called \`(Option|Result)::unwrap|thread '`.
7. For each of the top-10 largest user functions, do **not** decompile
   yet. Just record size, name (if present), and xref count via
   `xrefs_to`. This keeps the first pass cheap.
8. Report.

The first pass must not call `decompile` more than twice. If it does,
you are over-committing to hypotheses that haven't been scored.

See `references/survey-prompts.md` for concrete variants (Rust-biased,
Go-biased, Windows PE, IoT ELF, and unknown-format).

## Phase 2: locate the dispatcher

After the survey, the next objective is a *dispatcher*: the function
where an incoming command, message, or enum variant is routed. In
malware this is almost always a switch/if-chain with high cyclomatic
complexity that calls a wide fan-out of sibling functions.

Heuristics that actually work:

- **Big functions that call many siblings** — sort `list_funcs` by size
  descending, then use `callees` on each to rank by out-degree. The
  dispatcher is typically in the top 3.
- **Command words → xref → callsite** — the output of
  `find_regex` for command names (e.g. `NodeConnect`, `FileReq`,
  `ShellBack`) goes through `xrefs_to`. The function that touches *all*
  of them is the dispatcher.
- **Panic/anyhow bread crumbs** — Rust handlers often panic with
  "unknown command" or "invalid variant" near the fall-through arm. A
  `find_regex` for those phrases lands directly on the dispatcher.
- **serde/bincode hooks** — for Rust, `xrefs_to` the deserializer
  entry functions; for Go, `xrefs_to` `runtime.selectgo`,
  `runtime.chanrecv`, and `encoding/json.Unmarshal`.

Once the dispatcher is identified, decompile it **once** and read the
pseudocode carefully. Prefer a short targeted `set_comments` over a
rename. Rename only after the structure is clearly understood.

## Phase 3: progressive deepening to handlers

The dispatcher gives you a list of handler addresses. For each handler:

1. `decompile` — record the function's purpose in one sentence and the
   evidence supporting it.
2. `xrefs_to` on strings, globals, and types the handler touches.
3. `callees` — note which runtime/library calls it performs. That is
   the "capability fingerprint" of the handler.
4. Only after steps 1–3 for *all* handlers, begin `rename`.

The mistake to avoid: renaming the first handler you decompiled. You
will propagate a wrong guess through xrefs and contaminate later
analysis. Rename in one consolidated pass at the end of Phase 3.

## Phase 4: types and structs

Only after handlers are stable do you touch types. Use:

- `infer_types` for quick wins on parameters you already understand.
- `set_type` only with evidence — either a matching decompiled shape or
  an observed serde/bincode layout.
- `export_funcs` for a handler family when you want to diff across
  samples or feed into a separate capability tool.

## Phase 5: handoff

When the survey and dispatcher analysis are stable, hand off to the
language- or topic-specific skill:

- Rust → `reverse-rust-malware`
- Go → `reverse-golang-malware` or `reverse-golang-symbol-recovery`
- Protocol recovery → `reverse-protocol-reconstruction`
- Operator attribution → `reverse-operator-attribution`
- Botnet containment → `reverse-botnet-dismantling`
- Final report → `reverse-reporting`

## Cost discipline

Every MCP call has a latency + context cost. Budget your first pass:

- ≤ 2 `decompile` calls in Phase 1
- ≤ 10 `decompile` calls in Phase 2 (dispatcher + shortlist)
- `find_regex` and `xrefs_to` are cheap — use them liberally
- `py_eval` once per capability you can't get from built-in tools

If a phase blows the budget, stop and summarize what you learned rather
than continuing on momentum.

## `py_eval` helpers

This skill ships `py_eval`-ready scripts in `scripts/`. Each script is
plain Python, doesn't import IDA-specific modules when run standalone,
and gets a thin IDA wrapper at the top when pasted into `py_eval`.

- `scripts/ida_rodata_scanner.py` — the byte-by-byte `.rodata` scanner
  from the HackMD workflow. Recovers strings IDA misses.
- `scripts/ida_panic_paths.py` — pulls panic/source paths from
  user-selected segments and prints a de-duplicated workspace tree.
- `scripts/ida_pclntab_finder.py` — locates Go pclntab magic headers
  and emits the segment definition needed to undo stripping.

See each file for the IDA wrapper comment block.

## Prompt templates

See `references/survey-prompts.md` for ready-to-paste prompts:

- cold-start survey (no language guess yet)
- Rust-biased survey (panic-path and crate-version focus)
- Go-biased survey (pclntab, moduledata, goroutine focus)
- Dispatcher-locator prompt
- Handler fan-out prompt
- Type-recovery prompt

## Required response structure

When producing analyst output from this skill, use:

# IDA MCP Analyst Report

## Run log
- MCP tool: `list_funcs` — 3,182 functions
- MCP tool: `find_regex` (URLs+IPs+crypto) — 87 hits
- MCP tool: `py_eval` (rodata scanner) — 701 strings
- ...

## Executive summary
[2-5 sentences, evidence-grounded]

## Identity
- Format, arch, bitness
- Stripped, static/dynamic
- Language guess with confidence

## Facts
-
-

## Inferences
-
-

## Hypotheses
-
-

## Top user functions
| address | size | xrefs | notes |
|---------|------|-------|-------|

## Dispatcher candidate(s)
- address, complexity, supporting evidence

## Recommended next actions
1.
2.
3.
