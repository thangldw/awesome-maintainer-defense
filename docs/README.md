# Documentation

> One entry point for product reference, operating guidance, evidence, and deployable assets.

Start with the repository [README](../README.md). Use this page when you need to understand a decision, operate a defense, or verify a claim.

## Product reference

| Need | Canonical document |
| --- | --- |
| Run the repository auditor | [Auditor reference](AUDITOR.md) |
| Understand every PR-quality signal | [Signal contract](PROFILE_SIGNALS.md) |
| Install, verify, or remove the kit | [Kit guide](../kits/maintainer-defense-kit/README.md) |
| Know what the kit actually guarantees | [Kit assurance case](KIT_ASSURANCE.md) |

## Operate safely

1. Review [native GitHub controls](NATIVE_CONTROLS.md).
2. Use the [threat model](THREAT_MODEL.md) to identify assets and trust boundaries.
3. Choose a control level with the [maturity model](MATURITY_MODEL.md).
4. Follow the [defense playbook](PLAYBOOK.md) for baseline, observation, enforcement, incidents, and recovery.

Deployment translations:

- [Vietnamese playbook](vi/PLAYBOOK.md) and [assurance case](vi/KIT_ASSURANCE.md)
- [Japanese playbook](ja/PLAYBOOK.md) and [assurance case](ja/KIT_ASSURANCE.md)

## Verify the evidence

| Question | Evidence |
| --- | --- |
| How are catalog entries selected? | [Evaluation method](EVALUATION.md) |
| What access, effects, and limitations does each resource have? | [Resource audit](RESOURCE_AUDIT.md) |
| What did the synthetic corpus measure? | [Auditor evaluation](AUDITOR_EVALUATION.md) |
| What changed after testing public repositories? | [Auditor pilot](AUDITOR_PILOT.md) |
| What material corrections have been made? | [Audit log](AUDIT_LOG.md) |

## Deployable assets

- [AI-assisted contribution policy](../policies/AI_CONTRIBUTIONS.md)
- [Unsolicited pull-request policy](../policies/UNSOLICITED_PULL_REQUESTS.md)
- [Low-quality submission response](../responses/low-quality-pr.md)
- [Reproduction-needed response](../responses/reproduction-needed.md)
- [Balanced starter kit](../kits/balanced/README.md)
- [Workflow-hardening kit](../kits/workflow-hardening/README.md)

## Documentation rules

- Keep one canonical document for each contract.
- Link to evidence instead of repeating claims.
- Separate tested engineering behavior from field effectiveness.
- Keep English, Vietnamese, and Japanese deployment assets structurally aligned.
- Edit generated sources—not generated tables—and run `make validate` before merging.
