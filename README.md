# Awesome Maintainer Defense

> Audit the repository. Install only what you understand. Keep every enforcement decision reversible.

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Quality](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml/badge.svg)](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project gives open-source maintainers one coherent defense system:

- an offline repository auditor for governance, GitHub Actions, and moderation risk;
- a reversible kit with `observe`, `balanced`, and `hardened` profiles;
- an evidence-reviewed catalog of native controls and third-party tools;
- deployable policies, issue forms, response templates, and operating playbooks.

It is **anti-abuse, not anti-AI**. Findings are review inputs, never proof of authorship or intent.

## Audit first

Download the dependency-free v1.0 CLI and verify its checksum. Python 3.10+ is required; no network access or GitHub token is used during an audit.

```bash
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.0/maintainer-defense-kit.py
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.0/maintainer-defense-kit.py.sha256

sha256sum -c maintainer-defense-kit.py.sha256
# macOS: shasum -a 256 -c maintainer-defense-kit.py.sha256

python3 maintainer-defense-kit.py audit .
python3 maintainer-defense-kit.py audit . --format sarif > maintainer-defense.sarif
python3 maintainer-defense-kit.py fix . --output recommended.patch
```

`fix` emits a unified diff. It never edits files, changes GitHub settings, commits, or pushes. See the [auditor reference](docs/AUDITOR.md), [synthetic evaluation](docs/AUDITOR_EVALUATION.md), and [public-repository pilot](docs/AUDITOR_PILOT.md).

## Install a defense profile

Preview is the default. Add `--apply` only after reviewing every destination and diff.

```bash
python3 maintainer-defense-kit.py --target . --profile observe --language en --repo OWNER/REPOSITORY
python3 maintainer-defense-kit.py --target . --profile observe --language en --repo OWNER/REPOSITORY --apply
python3 maintainer-defense-kit.py --target . --verify
```

The installer refuses conflicting files, records ownership and hashes in a manifest, and will not uninstall modified installer-owned files.

![35-second terminal demo: dry-run, install observe, verify, then uninstall](assets/demo.gif)

## Choose the next move

| Repository state | Recommended move |
| --- | --- |
| No baseline yet | Review [native controls](docs/NATIVE_CONTROLS.md), then run the auditor |
| Normal contribution load | Install `observe`; collect data without contributor-visible action |
| Measured review overload | Consider `balanced`; keep human review and an appeal path |
| Supply-chain exposure | Add `hardened`; review pins, token permissions, and dependency policy |
| Active abuse incident | Use the [incident playbook](docs/PLAYBOOK.md); time-bound every restriction |

The [documentation hub](docs/README.md) maps product reference, operations, evidence, and deployable assets.

## Resources

The catalog is generated from [`catalog.json`](catalog.json). ⭐ marks a practical starting point, not a ranking, endorsement, or paid placement.

<!-- catalog:start -->

### Abuse Detection & Moderation

Detect, label, quarantine, or respond to spam, harassment, and low-quality automated contributions.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard) ⭐ | tool | Apache-2.0 | Repository abuse detection and response system for spam, harassment, and coordinated attacks. |
| [Anti Slop](https://github.com/peakoss/anti-slop) ⭐ | github-action | AGPL-3.0 | Configurable GitHub Action that detects and can close low-quality or AI-slop pull requests. |
| [GitHub AI Moderator](https://github.com/github/ai-moderator) | github-action | MIT | Model-powered Action that labels spam, link spam, and content it infers to be AI-generated. |
| [AI Community Moderator](https://github.com/benbalter/ai-community-moderator) | github-action | MIT | Moderates community interactions against a project's contributing guide and code of conduct. |
| [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler) | github-action | MIT | Issue-intake Action that retrieves an AI assessment and applies configurable labels. |

### Contributor Trust & Admission

Use explicit vouches or contribution history to control access without closing a project to everyone.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Fossier](https://github.com/PThorpe92/fossier) | tool | MIT | Vouch-compatible workflow and CLI for reducing unsolicited pull-request spam. |
| [Vouch](https://github.com/mitchellh/vouch) ⭐ | tool | MIT | Community trust management based on explicit vouches before a participant can contribute. |
| [Good Egg](https://github.com/2ndSetAI/good-egg) | github-action | MIT | Scores pull-request authors using their contribution history across GitHub. |

### Intake & Triage

Reduce review load with structured intake, labels, lifecycle automation, and emergency lockdowns.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Labeler](https://github.com/actions/labeler) | github-action | MIT | Official Action for labeling pull requests from changed files and branch patterns. |
| [Stale](https://github.com/actions/stale) | github-action | MIT | Official Action for marking and optionally closing inactive issues and pull requests. |
| [Lock Threads](https://github.com/dessant/lock-threads) | github-action | MIT | Locks closed issues, pull requests, and discussions after a configurable period. |
| [Repo Lockdown](https://github.com/dessant/repo-lockdown) ⭐ | github-action | MIT | Emergency Action that immediately closes and locks new issues or pull requests. |
| [Issue Metrics](https://github.com/github-community-projects/issue-metrics) | github-action | MIT | Measures issue, pull-request, and discussion response times and generates a Markdown report. |

### Repository Governance & Access

Keep security policies, branch protections, and repository settings consistent across projects.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [OpenSSF Allstar](https://github.com/ossf/allstar) ⭐ | github-app | Apache-2.0 | Continuously checks and enforces security policies across GitHub organizations. |
| [Safe Settings](https://github.com/github-community-projects/safe-settings) ⭐ | github-app | ISC | Centrally manages repository settings, branch protections, and teams with pull-request dry runs. |
| [Repository Settings App](https://github.com/repository-settings/app) | github-app | ISC | Synchronizes repository settings from a version-controlled `.github/settings.yml` file. |

### Workflow & Supply-Chain Defense

Protect CI, dependencies, secrets, and merge paths from hostile or compromised contributions.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Harden-Runner](https://github.com/step-security/harden-runner) ⭐ | github-action | Apache-2.0 | Monitors network egress, file integrity, and processes on GitHub-hosted runners. |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) ⭐ | tool | Apache-2.0 | Automated security-health checks for open-source projects and their dependencies. |
| [zizmor](https://github.com/zizmorcore/zizmor) ⭐ | tool | MIT | Static analysis for security and correctness problems in GitHub Actions workflows. |
| [pinact](https://github.com/suzuki-shunsuke/pinact) | tool | MIT | Pins GitHub Actions and reusable workflows to immutable commit hashes. |
| [Dependency Review Action](https://github.com/actions/dependency-review-action) ⭐ | github-action | MIT | Blocks pull requests that introduce vulnerable dependencies or disallowed licenses. |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | tool | AGPL-3.0 | Finds and verifies leaked credentials before they become a maintainer incident. |
| [PRevent](https://github.com/apiiro/PRevent) | github-app | MIT | Detects suspicious pull-request changes that may indicate malicious code. |
| [OSV-Scanner](https://github.com/google/osv-scanner) ⭐ | tool | Apache-2.0 | Scans lockfiles, SBOMs, and source artifacts against the OSV vulnerability database. |
| [Gitleaks](https://github.com/gitleaks/gitleaks) ⭐ | tool | MIT | Detects secrets in Git history, directories, files, and standard input. |

### Policies & Playbooks

Set expectations before problems arrive and respond consistently when they do.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies) ⭐ | awesome-list | CC0-1.0 | Comparative catalog of how open-source projects govern AI-generated contributions. |
| [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178) | working-group | N/A | Open work item developing practices for low-quality AI security reports and contributions; not a finalized standard. |

<!-- catalog:end -->

## Safety contract

- Evaluate submission quality and repository risk, not presumed authorship.
- Run untrusted code only with read-only authority and no secrets.
- Start with observation; require evidence before enforcement.
- Prefer queues and status checks over automatic closing or locking.
- Publish the rule, owner, review date, rollback, and appeal path.
- Treat every scanner result and catalog listing as evidence to review—not certification.

The kit's installation, pinning, permissions, and rollback behavior are tested. Moderation effectiveness is not yet field-proven. Read the [assurance case](docs/KIT_ASSURANCE.md) before production use.

## Contribute

Use [CONTRIBUTING.md](CONTRIBUTING.md) for catalog evidence requirements and safety review. Listings cannot be purchased, and inclusion is not a security endorsement.

MIT licensed. Templates are starting points, not legal advice.
