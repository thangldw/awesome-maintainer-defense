# Balanced maintainer-defense starter kit

This is the label-only component used by the balanced Maintainer Defense Kit profile. Prefer the [installer](../maintainer-defense-kit) so conflicts, provenance, verification, and rollback are recorded.

## Behavior

- Pull requests are checked against deterministic submission-quality signals. The baseline explicitly disables username, account-age, profile-completeness, global-history, emoji, and similar proxy heuristics.
- A pull request with several quality-risk signals receives `needs-human-review`; it is **not** commented on, closed, or locked.
- Only `opened` and `reopened` events are checked, preventing repeated comments or labels after every edit and synchronize event.
- The workflow never checks out or executes code from the pull request.
- Bug reports must include a version, environment, reproduction steps, and expected behavior.

## Before enabling

1. Read the pinned Action's documentation and license.
2. Test on a non-critical repository or fork.
3. Create the `needs-human-review` label. The upstream Action only logs a warning when a configured label is missing; it cannot make that failure visible to contributors.
4. Adjust thresholds using real submissions and record false positives.
5. Publish an appeal path and contribution policy.

Automated scores are triage hints, not proof that a contributor used AI or acted maliciously.
