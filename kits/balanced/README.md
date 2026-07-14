# Balanced maintainer-defense starter kit

This kit raises the quality bar without automatically rejecting first-time contributors. Copy the contents of this directory into the root of your repository, create the `needs-human-review` label, and edit the templates for your project.

## Behavior

- Pull requests are checked against deterministic quality and contributor-history signals.
- A suspicious pull request receives `needs-human-review`; it is **not** closed or locked.
- The workflow never checks out or executes code from the pull request.
- Bug reports must include a version, environment, reproduction steps, and expected behavior.

## Before enabling

1. Read the pinned Action's documentation and license.
2. Test on a non-critical repository or fork.
3. Create the `needs-human-review` label.
4. Adjust thresholds using real submissions and record false positives.
5. Publish an appeal path and contribution policy.

Automated scores are triage hints, not proof that a contributor used AI or acted maliciously.
