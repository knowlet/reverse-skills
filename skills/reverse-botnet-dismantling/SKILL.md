---
name: reverse-botnet-dismantling
description: Use this skill when reverse-engineering, sandbox, or threat-intel work has already reconstructed a malware or botnet control plane and the goal is to turn that evidence into ranked disruption, containment, sinkhole, monitoring, and coordination options without overstating what is actually feasible.
---

# Reverse Botnet Dismantling

Use this skill after the protocol, infrastructure, or operator model is clear enough to ask what can actually be disrupted, contained, or monitored.

## Guardrails

- Separate facts, inferences, hypotheses, and unknowns.
- Distinguish true takedown paths from containment or attrition paths.
- State legal, provider, operational, and synchronization prerequisites.
- Do not promise network-wide disruption unless the command-auth and bootstrap assumptions support it.
- Treat endpoint cleanup, sinkholing, detection rollout, and operator seizure as different actions with different outcomes.

## Inputs

Prioritize:
- bootstrap or rejoin mechanism
- command-auth model and key material
- peer discovery and routing-table behavior
- update and recovery path
- persistence and re-seeding behavior
- relay or cloud infrastructure
- on-chain or payment infrastructure
- existing detections, IOCs, and partner constraints

If three or more disruption routes are in scope, read `references/disruption-playbook.md`.

If a deliverable is needed, use `assets/dismantling-template.md`.

## Workflow

### Phase 1: model the control plane

Document:
- how nodes join or rejoin the network
- how commands are authenticated
- how peers are learned and refreshed
- how updates are delivered and verified
- how the operator restores the network after losses

### Phase 2: enumerate route families

Consider:
- key or credential seizure
- bootstrap denial or poisoning
- peer blocking or sinkholing
- update interception or replacement
- crypto or implementation weakness exploitation
- routing-table reset or rejoin isolation
- endpoint eradication at scale
- provider, CERT, exchange, or law-enforcement action

### Phase 3: score each route

Score each route on:
1. prerequisite access
2. operational complexity
3. time to effect
4. scale
5. detectability
6. collateral risk
7. operator recovery potential

### Phase 4: assemble a phased plan

Split the plan into:
- intelligence collection
- preparation
- synchronized execution
- sustainment and monitoring

### Phase 5: define continuous monitoring

Recommend the lightest monitoring stack that still catches operator movement:
- sample hunting
- retro hunting
- network detections
- peer refresh tracking
- wallet or contract watch
- update-path monitoring

## Output format

# Dismantling Plan

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

## Control Plane Model
- Component | Evidence | Failure point | Confidence

## Ranked Disruption Routes
- Route | Effect | Prerequisites | Limits | Confidence

## Monitoring Plan
- Source | Trigger | Why it matters

## Recommended Next Actions
1.
2.
3.
