# Audit log

This log records material corrections to the catalog. Routine wording and link maintenance may remain in Git history.

## 2026-07-14 — Maintainer Defense Kit assurance audit

- Found that the earlier triage workflow could create repeated failure comments on `edited` and `synchronize` events; removed public comments.
- Confirmed from upstream source that a missing configured label only produces a warning; removed automated labeling rather than accepting a silent failure mode.
- Zizmor then rejected the remaining `pull_request_target` trust boundary. Replaced it with a read-only `pull_request` status gate instead of suppressing the finding.
- Disabled upstream username, account-age, fork-rate, public-profile, profile-completeness, global-history, emoji, and commit-author proxy heuristics so the baseline follows the project's quality-not-authorship principle.
- Removed undeclared default labels from the issue form because GitHub does not apply labels that do not already exist.
- Added an installer with dry-run default, conflict refusal, ownership and SHA-256 manifest, verification, modified-file-safe uninstall, repository-bound paths, symlink rejection, and atomic manifest creation.
- Tested all nine profile/language combinations plus conflicts, modified files, pre-existing files, malicious manifest paths, and symlink traversal.
- Resolved four upstream Action tags to their recorded immutable SHAs, confirmed GitHub reports all four commits as verified, and added scheduled drift verification.
- Added an explicit assurance case, production acceptance gate, native-control precedence, and complete deployable English, Vietnamese, and Japanese kit assets.

## 2026-07-14 — Full evidence audit

- Audited every entry against its official repository, README, action documentation, and detected license.
- Added `audits.json` with deployment, defaults, maximum effects, data boundaries, access, limitations, repository snapshots, and evidence links.
- Corrected PRevent from `github-action` to `github-app`; upstream documents a self-hosted GitHub App deployment.
- Renamed the OpenSSF AI-slop entry to **Best-Practices Work Item** and stated that it is not a finalized standard.
- Removed Agentic OSS Policy because the repository had no detected license; without a license, reusable policy text does not meet this project's inclusion bar.
- Recorded that Niubi Guard's repository API returned `NOASSERTION` while its checked license file contained Apache License 2.0 text.
- Corrected Issue Metrics: the Action generates a Markdown file; publishing it as an issue requires a separate Action and write permission.
- Downgraded GitHub AI Moderator, Good Egg, and the unfinished OpenSSF work item from featured status. Model-based authorship inference is not proof, history scoring needs bias evaluation, and an open work item is not an adoption-ready standard.
- Added OpenSSF Allstar, Safe Settings, Repository Settings App, Issue Metrics, OSV-Scanner, and Gitleaks to cover governance, measurement, vulnerability, and secret defenses.
- Added a 180-day audit-expiry check, complete audit/catalog ID matching, full-SHA Action pin enforcement, and weekly evidence-link checks.

## Reporting an audit error

Open an issue with the resource ID, the claim that is wrong, and a canonical upstream source. Security-sensitive problems should use private vulnerability reporting.
