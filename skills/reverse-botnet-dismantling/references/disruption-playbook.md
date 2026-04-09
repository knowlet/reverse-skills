# Botnet Disruption Playbook

Use this reference when the task has moved beyond description and needs ranked operational options.

## Model first

Before suggesting action, identify:
- bootstrap and rejoin path
- command-auth mechanism
- update mechanism
- peer discovery and routing behavior
- recovery path after sinkholing or node loss

## Route families

| Route family | Typical effect | Typical prerequisite | Common failure mode |
| --- | --- | --- | --- |
| Key or credential seizure | true operator-level disruption | access to signing key, admin wallet, or operator host | legal or operational infeasibility |
| Bootstrap denial | reduces rejoin and expansion | stable bootstrap target, contract, relay, or seed list | operator rotates or re-seeds |
| Sinkhole or peer blocking | contains and observes | routable infrastructure and coordination | partial coverage only |
| Update interception | blocks or delays refresh | weak update validation or trusted network position | signed updates still win |
| Crypto or implementation weakness | creates selective exploit path | confirmed weakness and safe exploit plan | weakness is irrelevant to live path |
| Routing-table reset or rejoin isolation | temporary attrition | volatile peer cache or recoverable state | nodes rejoin through alternate path |
| Endpoint cleanup at scale | victim reduction | detection coverage and response capacity | reinfection or missed segments |

## Scoring guidance

- High value: materially reduces operator control or network recovery.
- Medium value: degrades availability or visibility but does not break command authority.
- Low value: useful only as support for another route.

When command authority depends on asymmetric signing, key seizure may be the only true network-wide takedown path. Everything else is containment, attrition, or intelligence gain unless the bootstrap path is also severed.

## Four-phase plan

1. Intelligence collection
2. Preparation and coordination
3. Synchronized execution
4. Sustainment and monitoring

## Monitoring stack

- hunt new samples and historical variants
- refresh peer or seed inventories
- watch wallets, contracts, and funding flows
- alert on update-path movement
- maintain network detections for rejoin attempts
