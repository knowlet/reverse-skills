# Operator Pivot Priority

Use this reference when more than one attribution path exists and the analyst needs to decide what to chase first.

## Priority order

1. unique literal fingerprint
2. wallet or smart-contract reuse
3. stable relay or cloud-account pivot
4. build-path or username leakage
5. version tuple or compiler time window
6. regional or cultural hints

## Pivot classes

| Pivot class | Why it matters | Best external checks | Common trap |
| --- | --- | --- | --- |
| Unique typo or literal | Often survives refactors and may be globally rare | code search, malware corpora, web search | copy-paste reuse by third parties |
| Wallet or contract | Connects malware to funding and operational cadence | chain explorer, clustering, exchange touchpoints | assuming wallet owner equals malware author |
| Cloud relay or VPS | Can lead to account records and infrastructure reuse | ASN, passive DNS, provider logs, legal request | treating a relay as the operator without corroboration |
| Build path or username | Leaks local environment and naming habits | repo search, path conventions, cross-sample comparison | generic usernames such as `admin`, `ubuntu`, `user` |
| Version tuple | Narrows time window and dependency set | release dates, Cargo or package lock comparisons | over-precision when toolchains are backported |
| Geography or cultural clue | Can inform prioritization | node distribution, language review, number patterns | turning weak hints into identity claims |

## Confidence guidance

- High: a unique pivot is independently corroborated by a second source.
- Medium: the pivot is useful but spoofable or incomplete.
- Low: the pivot is suggestive but weak without outside confirmation.

## Escalation triggers

- Use provider escalation when the best pivot is a stable cloud relay, mailbox, or hosting account.
- Use financial escalation when the best pivot is a wallet, exchange interaction, or contract admin path.
- Use public reporting only after removing claims that rely on provider-only or sealed evidence.
