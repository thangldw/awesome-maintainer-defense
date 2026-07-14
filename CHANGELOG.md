# Changelog

All notable changes are documented here. Dates use ISO 8601.

## [1.0.0] - 2026-07-14

### Maintainer defense kit

- Added install, dry-run, manifest verification, conflict-safe writes, and guarded uninstall across `observe`, `balanced`, and `hardened` profiles.
- Shipped complete deployment assets in English, Vietnamese, and Japanese.
- Added a dependency-free standalone release CLI with 25 gzip-compressed embedded assets and a published SHA-256 checksum.
- Added an honest 35.5-second demo generated from the real standalone CLI: dry-run → install `observe` → verify → uninstall.

### What the audit changed

- **Removed `pull_request_target`.** The first label-only correction still crossed a privileged trust boundary. Zizmor rejected it, so the shipped design uses the unprivileged `pull_request` event, read-only permissions, no checkout of contributor code, and a named status gate.
- **Removed proxy heuristics.** Username, account age, fork rate, profile state, global merge history, emoji, code-reference style, and commit-author identity are disabled. The baseline evaluates submission quality signals, not presumed authorship or intent.
- **Removed silent label failure.** Upstream source showed that a missing label could reduce enforcement to a warning. Automated comments and labeling were removed from the shipped workflows; the neutral label specification is optional and explicitly manual.
- **Removed undeclared issue labels.** GitHub documents that missing issue-form labels are not applied. The forms no longer imply a queue that may not exist.
- **Hardened local changes.** The installer rejects path traversal and symlink destinations, refuses to overwrite conflicting files, verifies cryptographic digests, and never removes modified installer-owned files.

### Assurance boundary

The engineering guarantees above are covered by static validation and end-to-end tests. Moderation effectiveness, false-positive rates, and maintainer time saved still require field evidence; v1.0.0 does not present them as proven outcomes. See [`docs/KIT_ASSURANCE.md`](docs/KIT_ASSURANCE.md) and [`docs/AUDIT_LOG.md`](docs/AUDIT_LOG.md).

[1.0.0]: https://github.com/thangldw/awesome-maintainer-defense/releases/tag/v1.0.0
