---
name: reverse-protocol-reconstruction
description: Use this skill to reconstruct command flow, transport assumptions, message boundaries, field candidates, and encode/decode behavior from reverse-engineering evidence.
---

# Reverse Protocol Reconstruction

Use this skill when the analysis already has some strings, handler candidates, or decompiled code and the next goal is to reconstruct the wire protocol or command model.

## Minimum evidence package

Before reconstructing fields, gather at least:
- command strings, JSON keys, or opcode constants
- one decode or parse function
- one dispatch or handler function
- one encode or send function, if present
- transport clues from imports, strings, or telemetry

If `ida-pro-mcp` is connected, the minimum MCP pass is:
- `find_regex` for command words, verbs, framing strings, and JSON tags
- `xrefs_to` on those strings or constants
- `decompile` the decode, dispatch, and encode candidates
- `callgraph` from the receive path or top dispatcher
- `export_funcs` when local diffing or field extraction is needed

## Objectives

Produce:
1. a command map,
2. likely encode/decode boundaries,
3. message and field candidates,
4. protocol-flow hypotheses,
5. validation steps.

## Workflow

### Phase 1: gather protocol clues
Look for:
- command strings
- packet builders
- serializers / deserializers
- message enums
- length-prefix or framing logic
- crypto wrapping
- transport wrappers

### Phase 2: identify boundaries
Try to isolate:
- receive path
- decode path
- dispatch path
- handler path
- encode path
- send path

Do not infer a full protocol from only one function. Prefer at least one path on each side of dispatch.

### Phase 3: command and message map
For each command or message candidate, record:
- evidence
- likely direction
- likely arguments or fields
- confidence level

Useful CLI pivots:

```bash
strings -a -n 4 sample.bin | rg -i 'json|msgpack|protobuf|grpc|http|ws|opcode|cmd|type|action|version|nonce|iv'
```

### Phase 4: defensive interpretation
Summarize:
- likely operator actions supported
- likely network visibility
- best validation points in PCAP, sandbox, or telemetry

If protocol evidence now supports operator pivots, hand off to `reverse-operator-attribution`.

If the recovered control plane is mature enough for containment or takedown planning, hand off to `reverse-botnet-dismantling`.

## Output format

# Protocol Reconstruction Summary

## Executive Summary
[2-5 sentences]

## Facts
- 
- 

## Inferences
- 
- 

## Message / Command Candidates
- 
- 

## Flow Hypothesis
1.
2.
3.

## Gaps
- 
- 

## Validation Plan
1.
2.
3.
