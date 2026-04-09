---
name: reverse-operator-attribution
description: Use this skill when reverse-engineering, sandbox, or threat-intel evidence exposes build paths, usernames, typo fingerprints, version windows, cloud relays, wallets, contracts, peer infrastructure, or other operator traces and the goal is to pivot from malware artifacts to a defensible developer or operator attribution model with prioritized investigative actions.
---

# Reverse Operator Attribution

Use this skill after basic malware analysis exists and the next question is who likely built, operated, funded, or hosted the capability.

## Guardrails

- Separate facts, inferences, hypotheses, and unknowns.
- Prefer uniqueness over volume.
- Treat language, culture, timezone, and geography as weak signals until corroborated.
- Distinguish developer, builder, operator, relay owner, and victim. They may not be the same entity.
- Mark any action that requires provider cooperation, legal process, or law-enforcement support.

## Inputs

Prioritize:
- build paths, usernames, hostnames, temp paths
- compiler versions, crate or package tuples, protocol versions
- unique typos, literals, banners, comments, error strings
- public keys, wallet addresses, contract addresses
- peer IPs, relay hosts, VPS or cloud metadata
- update URLs, repositories, certificates, package names
- dynamic artifacts such as PCAP, memory dumps, process arguments, sandbox notes

If three or more pivot classes are present, read `references/pivot-priority.md`.

If a deliverable is needed, use `assets/attribution-template.md`.

## Workflow

### Phase 1: normalize pivots

Group the evidence into:
- source or build environment leakage
- versioning and time-window clues
- language and style fingerprints
- infrastructure and hosting pivots
- crypto and finance pivots
- operator behavior or deployment habits

### Phase 2: score pivots

Rank each pivot by:
1. uniqueness
2. external verifiability
3. resistance to spoofing
4. investigative value

Prefer:
- unique typo or literal with low public collisions
- wallet or contract reuse
- stable relay or cloud-account pivots
- uncommon version tuples or path conventions

De-prioritize:
- country guesses from peer distribution alone
- generic usernames
- non-unique library strings

### Phase 3: build an attribution graph

Map each path as:

`artifact -> pivot -> external entity -> implication -> confidence`

Track competing explanations such as:
- copied code
- rented infrastructure
- reused wallets
- deliberate false flags
- shared build hosts

### Phase 4: stress-test every major claim

For every meaningful attribution claim, ask:
- What is the direct evidence?
- What alternative explanation remains plausible?
- What evidence would weaken or collapse this claim?
- What outside source could confirm it?

### Phase 5: recommend the shortest next actions

Common next actions:
- search code and malware corpora for unique typo, path, and version tuples
- cluster samples by shared literals, keys, wallets, or update paths
- trace wallet and contract relationships
- pivot on cloud relay ownership, passive DNS, WHOIS, ASN, or hosting reuse
- prepare provider or exchange escalation packages

## Output format

# Attribution Summary

## Executive Summary
[2-5 sentences]

## Facts
- 
- 

## Inferences
- 
- 

## Hypotheses
- 
- 

## Unknowns
- 
- 

## High-Value Pivots
- Pivot | Evidence | Why it matters | Confidence

## Attribution Graph
- Artifact | Pivot | External entity | Implication | Confidence

## Recommended Next Actions
1.
2.
3.
