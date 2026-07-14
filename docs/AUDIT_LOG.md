# Audit log

This log records material corrections to the catalog. Routine wording and link maintenance may remain in Git history.

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
