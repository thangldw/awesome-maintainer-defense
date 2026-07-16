# Changelog

> Release history for published versions.

All notable changes are documented here. Dates use ISO 8601.

## [1.1] - 2026-07-17

### Auditor-first product contract

- Repositioned the README around Maintainer Defense Kit as the CLI/auditor/policy product and moved the Awesome badge to the community catalog.
- Added real default CLI output from the published `pwn-request` corpus case and a regression test that keeps the README block byte-for-byte aligned with the implementation.
- Made human output lead with severity counts and label evidence, risk, safe remediation, and the stable rule reference.
- Added a complete rule reference with false-positive review guidance and conservative OpenSSF/CWE mappings.
- Added SARIF `helpUri` links and a pinned, checksum-verified GitHub code scanning workflow example with an explicit `security-events: write` boundary.
- Added a machine-readable rule registry that owns canonical titles, severities, help anchors, and standards mappings, with drift checks across implementation, corpus, and documentation.
- Added compact `--format summary` output, dedicated auditor false-positive intake, and a consent-based OSS maintainer pilot protocol.
- Added a tested universal wheel with `pipx` entry points and a checksum-locked Homebrew formula.
- Added a real CLI-result screenshot, plain-language product description, focused comparison, outcome roadmap, and three bounded newcomer issues.

## [1.0] - 2026-07-15

### Real-repository pilot corrections

- Audited ten public repositories at pinned commits and published the applicability boundary instead of inferring real-world precision from synthetic fixtures.
- Correctly parse quoted `uses:` values so full-SHA pins are not reported as mutable references.
- Report privileged-event checkout only when the checked-out revision is attacker-influenced; a reviewed base-branch checkout is not treated as a pwn-request path.
- Scope persisted-checkout-credential checks to the checkout job and step rather than permissions or options elsewhere in a multi-job workflow.
- Added regression fixtures derived from all three pilot corrections, bringing the labeled synthetic corpus to 52 cases.

### Repository auditor

- Added dependency-free `audit` and patch-only `fix` commands while preserving the v1 installer interface.
- Added human, stable JSON v1, and SARIF 2.1.0 output with source locations, severity, confidence, threat scenarios, recommendations, fingerprints, and patch metadata.
- Added governance, workflow trust-boundary, and moderation-safety rule families.
- Added a labeled 52-case corpus plus permission, Action-pin, and persisted-token mutation tests.
- Added CODEOWNERS coverage and monthly Dependabot updates for GitHub Actions.

### Profile contract and support boundary

- Made all six active PR-quality checks and the four-failure threshold explicit in the shipped workflows, rather than inheriting behavior from upstream defaults.
- Disabled source-branch-name and label-bypass heuristics, plus repository-history proxies, so the baseline stays focused on submission properties.
- Added a reviewable signal contract covering checks, thresholds, profile effects, disabled inputs, exemptions, tuning, and limitations.
- Declared Python 3.10+ support and added CI coverage for Linux on Python 3.10, 3.12, and 3.14 and macOS on Python 3.12.
- Added a privacy-sanitized field-report path for collecting the evidence needed to evaluate false positives and maintainer workload.
- Removed the final undeclared issue-form label dependency and added validation to prevent silent label failures from returning.
- Clarified that English, Vietnamese, and Japanese assets are structurally complete while independent native security/legal review of Vietnamese and Japanese wording remains pending.

### Maintainer defense kit

- Added install, dry-run, manifest verification, conflict-safe writes, and guarded uninstall across `observe`, `balanced`, and `hardened` profiles.
- Shipped structurally complete deployment assets in English, Vietnamese, and Japanese.
- Added a dependency-free standalone release CLI with 25 gzip-compressed embedded assets and a published SHA-256 checksum.
- Added an honest 35.5-second demo generated from the real standalone CLI: dry-run → install `observe` → verify → uninstall.

### What the audit changed

- **Removed `pull_request_target`.** The first label-only correction still crossed a privileged trust boundary. Zizmor rejected it, so the shipped design uses the unprivileged `pull_request` event, read-only permissions, no checkout of contributor code, and a named status gate.
- **Removed proxy heuristics.** Username, account age, fork rate, profile state, global merge history, emoji, code-reference style, and commit-author identity are disabled. The baseline evaluates submission quality signals, not presumed authorship or intent.
- **Removed silent label failure.** Upstream source showed that a missing label could reduce enforcement to a warning. Automated comments and labeling were removed from the shipped workflows; the neutral label specification is optional and explicitly manual.
- **Removed undeclared issue labels.** GitHub documents that missing issue-form labels are not applied. The forms no longer imply a queue that may not exist.
- **Hardened local changes.** The installer rejects path traversal and symlink destinations, refuses to overwrite conflicting files, verifies cryptographic digests, and never removes modified installer-owned files.

### Assurance boundary

The engineering guarantees above are covered by static validation and end-to-end tests. Moderation effectiveness, false-positive rates, and maintainer time saved still require field evidence; v1.0 does not present them as proven outcomes. See [`docs/KIT_ASSURANCE.md`](docs/KIT_ASSURANCE.md) and [`docs/AUDIT_LOG.md`](docs/AUDIT_LOG.md).

[1.0]: https://github.com/thangldw/awesome-maintainer-defense/releases/tag/v1.0
[1.1]: https://github.com/thangldw/awesome-maintainer-defense/releases/tag/v1.1
