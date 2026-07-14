# Maintainer-defense maturity model

This model describes operational readiness, not project prestige.

| Level | Name | Observable state |
| --- | --- | --- |
| 0 | Reactive | Rules are implicit; incidents are handled ad hoc; automation has broad default permissions |
| 1 | Documented | Contribution, security, conduct, and escalation policies exist; sensitive paths have owners |
| 2 | Measured | Queue load, response time, close reasons, and false positives are sampled; dry-run precedes enforcement |
| 3 | Controlled | Automation is least-privilege, pinned, reversible, owner-assigned, and periodically reviewed |
| 4 | Resilient | Incident controls have expiry and rollback; recovery includes reopening false positives and updating the threat model |

Do not skip from reactive directly to automatic blocking. Most repositories gain more from clearer intake, narrower scope, and protected workflows than from an opaque classifier.

## Minimum evidence to advance

- **0 → 1:** policy links are visible from contribution surfaces.
- **1 → 2:** at least one month or two release cycles of queue and false-positive observations.
- **2 → 3:** documented owner, permissions, data boundary, review date, rollback, and sampled accuracy for each enforcing tool.
- **3 → 4:** a completed exercise or incident showing that controls can be activated, communicated, removed, and audited.
