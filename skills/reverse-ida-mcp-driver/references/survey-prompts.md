# Survey prompt templates

Ready-to-paste opening prompts for driving `ida-pro-mcp`. Each template
is tuned for a different starting hypothesis and produces a structured
first-pass report without over-committing MCP tokens.

All prompts share a discipline: they name the exact MCP tools the agent
should call, require a *run log*, and forbid renaming in the first
pass. Without that discipline agents rapidly accumulate unverified
renames and fabricate call graphs.

---

## 1. Cold-start survey (no language guess)

Use when: you opened the IDB, the disassembler string window looks
thin, and you are not sure yet whether it is Go, Rust, Zig, C++, or a
packer stub.

```
Survey this binary using ida-pro-mcp. Do NOT rename anything.

Required sections, in this order:
  1. Run log — every MCP tool you called with argument summary + result count.
  2. Identity — format, arch, bits, entry, stripped?, static/dynamic.
  3. Toolchain guess — Go / Rust / Zig / C++ / other, with confidence and
     the specific evidence (symbols, strings, section layout, rustc vs
     go version markers, panic patterns).
  4. Top-10 largest non-runtime functions — size, xrefs_to count,
     raw name (if any).
  5. Strings coverage — count from IDA's string window vs count from
     py_eval `.rodata` byte-scan. Flag the gap if > 2x.
  6. Networking / crypto / persistence hints — only from strings or
     imports you actually saw.
  7. Next-action recommendation: which language-specific skill to hand
     off to.

Required tools to call at least once:
  - ida://idb/metadata
  - ida://idb/entrypoints
  - list_funcs
  - find_regex for  https?://|[0-9]{1,3}(\.[0-9]{1,3}){3}|ChaCha|AES|SHA-?2|Ed25519|X25519|rustls|openssl|/bin/sh|cmd\.exe
  - find_regex for  \.rs:\d+|\.go:\d+|panicked at
  - py_eval with the .rodata scanner from reverse-ida-mcp-driver/scripts/ida_rodata_scanner.py

At most 2 decompile calls. Pick them carefully.
Separate facts from inferences. Do not claim an MCP tool ran unless it
actually ran.
```

---

## 2. Rust-biased survey

Use when: the triage script or strings output already hinted at Rust
(panic markers, `.rs:N:M`, `tokio`, `serde`, `/home/*/...rust`).

```
Survey this binary as a likely Rust sample using ida-pro-mcp.

In addition to the cold-start survey requirements:

  - Use py_eval to run the .rodata byte-scanner at min=6. Report the
    total string count and the top-30 panic paths.
  - Use find_regex to pull:
      panicked at
      thread '.+?' panicked
      called `Option::unwrap|called `Result::unwrap
      registry/src/[^/]+/[a-zA-Z0-9_-]+-\d+\.\d+\.\d+
      /home/[\w.-]+/|/Users/[\w.-]+/
  - Reconstruct the workspace tree from source paths. List the
    top-level modules only.
  - Enumerate recovered crate versions (name=version). Flag any that
    look obsolete or known-vulnerable.
  - Identify the dispatcher candidate using cyclomatic complexity AND
    xrefs_to command-like strings; report both pieces of evidence.
  - Do NOT rename. Do NOT set_type. Return the run log, the workspace
    tree, the crate list, and the dispatcher candidate.

Hand off to reverse-rust-malware.
```

---

## 3. Go-biased survey

Use when: `go version -m`, strings, or `runtime.` markers indicate Go.

```
Survey this binary as a likely Go sample using ida-pro-mcp.

  - Run py_eval with scripts/ida_pclntab_finder.py. Report magic,
    endian, ptr size, pc quantum, and offset of every hit.
  - If a pclntab is found, record whether IDA already knows about it
    (check ida://idb/segments for .gopclntab).
  - list_funcs filtered for main.*, recovered user-package prefixes,
    and functions > 512 bytes that do not sit in runtime/.
  - find_regex for:
      go1\.\d+(\.\d+)?
      runtime\.newproc|runtime\.selectgo|runtime\.chansend|runtime\.chanrecv
      github\.com/|gitlab\.com/|bitbucket\.org/|gopkg\.in/
      https?://|[0-9]{1,3}(\.[0-9]{1,3}){3}
  - Identify main.main and main.init. decompile only main.main.
  - Score goroutine-heavy functions by counting xrefs_to
    runtime.newproc from each candidate.
  - Do NOT rename. Return: Go version guess, module path, candidate
    dispatcher, top-5 goroutine entry points, IOC hits.

Hand off to reverse-golang-symbol-recovery if the name quality is poor,
otherwise to reverse-golang-malware.
```

---

## 4. Dispatcher-locator prompt

Use after the survey, once you believe there is a central
command/message router but have not yet confirmed it.

```
Find the command dispatcher in this binary using ida-pro-mcp.

Rules:
  - Use find_regex to gather candidate command words. Start with the
    strings recovered from py_eval .rodata scan.
  - Use xrefs_to on each command string. Build a map of
    {command_string: [caller_eas]}.
  - The dispatcher is the function that appears as the caller for the
    largest subset of command strings. Report the exact EA + name if
    any.
  - Validate by decompiling the dispatcher ONCE. Confirm there is a
    switch/match-like structure with arms matching the command strings.
  - If two candidates tie, decompile both and report the pseudocode
    length, cyclomatic complexity, and callees for each.
  - Do NOT rename until you report back and I confirm.
```

---

## 5. Handler fan-out prompt

Use after the dispatcher is confirmed.

```
Map the handler fan-out from dispatcher <EA> using ida-pro-mcp.

  - callees(<EA>) — list every directly-called function.
  - For each handler, record:
      ea, size, outgoing calls (top 5), strings it references, xrefs_to
      from other functions.
  - For the top-3 handlers by size, decompile and write ONE sentence
    each describing purpose with the supporting evidence.
  - Do NOT rename until all handlers are covered in this phase.
  - Return a table sorted by handler size descending.
```

---

## 6. Type-recovery prompt

Use late in the workflow, once the dispatcher and handlers are
understood and you want IDA to display meaningful struct layouts.

```
Recover message struct types from the dispatcher and handlers using
ida-pro-mcp.

  - Call infer_types on the dispatcher first. Accept only inferences
    that match the handlers you already read.
  - For each handler with > 3 parameters, propose a struct shape
    consistent with the decompilation. Use set_type only when:
      (a) the shape is consistent across multiple call sites, and
      (b) the field offsets agree with serde/bincode expectations.
  - Report the before/after pseudocode for one handler to confirm the
    improvement.
  - Do NOT bulk-apply types across the whole IDB.
```
