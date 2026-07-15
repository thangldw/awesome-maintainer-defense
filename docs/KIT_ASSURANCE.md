# Maintainer Defense Kit assurance case

> Acceptance contract separating tested engineering guarantees from unproven field effectiveness. Return to the [documentation hub](README.md).

**Status:** engineering-verified baseline; not security-certified and not yet field-validated across representative public repositories.

This document defines exactly what the kit currently guarantees, how those claims are tested, and what remains unproven. “Defense” means reducing review cost and unsafe automation paths—not identifying whether a human or AI authored a contribution.

## Assurance claims

| Claim | Mechanism | Verification |
| --- | --- | --- |
| Safe adoption default | `observe` uses `pull_request`, read-only token permissions, no checkout, and disables comments, labels, close, and lock | Installer matrix test plus workflow validation |
| Reversible installation | Dry-run by default; conflict preflight; no overwrite; file hashes and ownership in a manifest; uninstall refuses modified owned files | Conflict, modified-file, pre-existing-file, verify, and uninstall tests |
| Repository boundary | Fixed relative destinations, manifest path validation, symlink rejection, and atomic manifest replacement | Malicious manifest and symlink tests |
| Limited contributor-visible effect | `balanced` and `hardened` can fail only a named status check; they do not comment, label, close, lock, merge, or execute PR code | Static workflow inspection and profile tests |
| Reduced proxy bias | Baseline explicitly disables username, account-age, fork-rate, public-profile, profile-completeness, global-merge-history, emoji, code-reference, and commit-author identity heuristics | Static workflow inspection |
| Immutable dependencies | Every Action reference is a full commit SHA with a matching `pins.json` record | Repository validator |
| Upstream provenance is monitored | Each documented tag resolved to the recorded SHA and each commit was reported verified by GitHub on 2026-07-15 | `scripts/verify_pins.py`, run on the weekly evidence workflow |
| Deployable translations | Every profile installs structurally complete English, Vietnamese, or Japanese intake templates, policies, playbook, and adoption record; independent native review of Vietnamese and Japanese wording remains pending | 3 profiles × 3 languages end-to-end matrix |
| Workflow regression detection | Workflow safety invariants, zizmor, and install tests run in CI | Quality and Workflow security workflows |
| Runtime support | The installer supports Python 3.10+ and is tested on Linux with Python 3.10, 3.12, and 3.14 and on macOS with Python 3.12 | Quality workflow matrix |

## Corrected findings from the second audit

The earlier balanced workflow was not strong enough to support an assurance claim:

1. It ran on `edited` and `synchronize` and configured a failure comment. The upstream Action calls `createComment` for each failed run, so normal PR updates could repeatedly notify contributors.
2. It assumed `needs-human-review` already existed. The upstream Action catches the failure-actions exception and logs a warning, meaning the intended queue could silently disappear. [Pinned upstream implementation](https://github.com/peakoss/anti-slop/blob/57858eead489d08b255fab2af45a506c2ca6eab2/src/actions.ts#L71-L113)
3. The first installer design needed explicit defenses against a malicious manifest and symlink traversal.
4. The issue form requested default labels that might not exist; GitHub documents that missing labels are simply not applied.
5. [Upstream defaults](https://github.com/peakoss/anti-slop/blob/57858eead489d08b255fab2af45a506c2ca6eab2/action.yaml) included identity, history, and style proxies that were not justified by this project's quality-first principles; the shipped profiles now explicitly disable them.
6. The first label-only correction still used `pull_request_target`. Zizmor correctly rejected that privileged trigger as fundamentally dangerous, so the final design uses a read-only `pull_request` status gate instead of suppressing the finding.

All shipped PR-quality workflows now use read-only permissions and avoid public comments and labels. `balanced` converts the pinned Action's controlled `result` output into a failing status check; enforcement remains an explicit native-ruleset decision. The default profile only writes a job summary.

## What is not guaranteed

- No detector can reliably prove AI authorship, intent, or contributor quality. Signals are triage inputs only.
- The repository does not yet contain a representative, privacy-reviewed field dataset measuring precision, recall, false-positive rate, maintainer time saved, or contributor drop-off.
- A verified upstream commit is not a full audit of third-party Action code. Maintainers must still review licenses, source, network behavior, and updates.
- GitHub settings, branch rules, label existence, private vulnerability reporting, and organizational policy are outside the local installer's control.
- Vietnamese and Japanese text has automated structural coverage but has not been independently reviewed by native-speaking security or legal professionals.
- The kit is not a compliance control, legal opinion, SLA, warranty, or incident-response service.

## Production acceptance gate

Treat the kit as production-ready for a specific repository only after all of the following are true:

1. Native GitHub controls in [`NATIVE_CONTROLS.md`](NATIVE_CONTROLS.md) are reviewed first.
2. `observe` runs for a documented period with no contributor-visible action.
3. The adoption record contains an owner, review SLA, appeal path, emergency disable owner, and baseline metrics.
4. Test PRs prove the status gate can both fail and recover; only then consider making it required in a native ruleset.
5. False positives and review time are reviewed by a human before thresholds or profiles change.
6. Installation verification, repository CI, and workflow security analysis pass.

Until field evidence exists, the honest answer is: the kit's **installation, permissions, reversibility, pinning, and localization are tested**; its real-world moderation effectiveness is **not yet guaranteed**.

The exact checks, thresholds, disabled proxies, and profile effects are recorded in [`PROFILE_SIGNALS.md`](PROFILE_SIGNALS.md). Maintainers may contribute privacy-sanitized aggregate results through the [field-report issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=field-report.yml); raw PR data and contributor identities are neither requested nor needed.
