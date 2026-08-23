# Documentation

English is the canonical product contract. Vietnamese and Japanese cover the essential adoption and safety journey; runtime kit assets remain structurally aligned across all three languages.

## Start and operate

| Goal | Document |
| --- | --- |
| Build, verify, and run the first audit | [Getting started](GETTING_STARTED.md) |
| Use every auditor command and output | [Auditor CLI](AUDITOR.md) |
| Review a finding by stable rule ID | [Auditor rules](AUDITOR_RULES.md) |
| Govern suppressions and expiry | [Configuration](CONFIGURATION.md) |
| Triage, authorize, roll out, and roll back controls | [Playbook](PLAYBOOK.md) |

## Decide whether to adopt

| Question | Document |
| --- | --- |
| What inputs and authority cross trust boundaries? | [Threat model](THREAT_MODEL.md) |
| Which claims have automated evidence? | [Kit assurance](KIT_ASSURANCE.md) |
| What does the labeled corpus measure? | [Auditor evaluation](AUDITOR_EVALUATION.md) |
| How can a maintainer authorize a pilot? | [Pilot program](AUDITOR_PILOT_PROGRAM.md) |
| Which artifacts and channels are release-authoritative? | [Distribution](DISTRIBUTION.md) |

## Browse and extend

- [Evidence-reviewed catalog](CATALOG.md)
- [Pilot evidence](../pilots/README.md)
- [Deployable kit](../kits/maintainer-defense-kit/README.md)
- [Contribution contract](../CONTRIBUTING.md)

Localized essentials: [Tiếng Việt](vi/README.md) · [日本語](ja/README.md).

## Architecture diagrams

- [Trust boundaries](diagrams/trust-boundaries.html): the local read-only audit path and the live GitHub state it cannot inspect.
- [Audit to action](diagrams/audit-to-action.html): the evidence, governance, and output contract at each stage, with owner authorization as the decision gate.
- [Consent to evidence](diagrams/consent-to-evidence.html): the disclosure-controlled path from maintainer consent to a reproducible evidence bundle.

Documentation claims must distinguish local tested behavior from live GitHub state and field effectiveness. Generated pages are rebuilt from structured sources; edit their source data rather than the generated Markdown.
