# Balanced profile

The balanced profile turns deterministic pull-request quality signals into one read-only status check. It does not check out pull-request code, comment, label, close, lock, merge, or change settings.

## Security boundary

The workflow runs on `pull_request`, grants read-only access, pins the third-party Action to a reviewed full commit SHA, and disables identity/history proxies. A controlled failed result becomes the `PR quality gate` check so contributors can recover by updating the pull request.

## Adoption gate

1. Install `observe` first and collect representative flagged and unflagged samples.
2. Record the signal window, false positives, appeals, threshold decision, owner, and rollback trigger.
3. Review the pinned Action source and license.
4. Test failure and recovery in a non-critical repository.
5. Enable `balanced`; make the check required in a native ruleset only after measured owner approval.

The status check is a triage input, not proof of AI use, intent, or contribution quality. Use the [installer](../maintainer-defense-kit/README.md) for conflict-safe preview, verification, and uninstall.
