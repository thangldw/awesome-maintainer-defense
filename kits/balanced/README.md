# Balanced maintainer-defense starter kit

> Deployable asset. Start from the [documentation hub](../../docs/README.md).

This is the read-only status-gate component used by the balanced Maintainer Defense Kit profile. Prefer the [installer](../maintainer-defense-kit) so conflicts, provenance, verification, and rollback are recorded.

## Behavior

- Pull requests are checked against deterministic submission-quality signals. The baseline explicitly disables username, account-age, profile-completeness, global-history, emoji, and similar proxy heuristics.
- A pull request with several quality-risk signals receives a failed `PR quality gate` check; it is **not** commented on, labeled, closed, or locked.
- New commits and edited descriptions are rechecked, allowing a contributor to clear the gate with better evidence.
- The workflow never checks out or executes code from the pull request.
- Bug reports must include a version, environment, reproduction steps, and expected behavior.

## Before enabling

1. Read the pinned Action's documentation and license.
2. Test on a non-critical repository or fork.
3. Adjust thresholds using real submissions and record false positives.
4. Publish an appeal path and contribution policy.
5. Only after observation, optionally make `PR quality gate` a required check in a native GitHub ruleset.

Automated scores are triage hints, not proof that a contributor used AI or acted maliciously.
