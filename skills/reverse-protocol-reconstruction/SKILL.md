---
name: reverse-protocol-reconstruction
description: Use this skill to reconstruct command flow, transport assumptions, message boundaries, field candidates, and encode/decode behavior from reverse-engineering evidence.
---

# Reverse Protocol Reconstruction

Use this skill when the analysis already has some strings, handler candidates, or decompiled code and the next goal is to reconstruct the wire protocol or command model.

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

### Phase 3: command and message map
For each command or message candidate, record:
- evidence
- likely direction
- likely arguments or fields
- confidence level

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
