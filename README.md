# Awesome Maintainer Defense

> A curated defense stack, policies, and ready-to-use workflows for open-source maintainers.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Quality](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml/badge.svg)](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Open source should stay open without requiring maintainers to absorb unlimited spam, harassment, unsafe workflows, low-effort automated contributions, or security-report noise. This list collects practical defenses while preserving human review and legitimate first-time contributions.

This project is **anti-abuse, not anti-AI**. It favors transparent signals, reversible actions, least privilege, and a documented appeal path over unreliable claims that a tool can perfectly identify AI-generated content.

## Start here

| Situation | First move | Then consider |
| --- | --- | --- |
| Normal project, limited time | Copy the [balanced starter kit](kits/balanced) | Add structured issue forms and lifecycle automation |
| Sudden PR or issue flood | Disable automatic merges and enable interaction limits | Review [Repo Lockdown](https://github.com/dessant/repo-lockdown) before activating it |
| Repeated low-quality PRs | Label for human review before auto-closing | Add Anti Slop in report-only mode and publish a contribution policy |
| Harassment or coordinated abuse | Preserve evidence and limit interactions | Use Niubi Guard in dry-run mode before applying actions |
| Suspicious workflow change | Do not run untrusted code with write tokens | Run zizmor, pin Actions, and restrict `GITHUB_TOKEN` permissions |

The [balanced starter kit](kits/balanced) is deliberately review-first: it labels suspicious submissions but does not automatically close them.

## Principles

1. **Quality, not authorship.** Evaluate reproducibility, scope, tests, and contributor responsiveness—not writing style.
2. **Review before enforcement.** Start in report-only or dry-run mode and measure false positives.
3. **Least privilege.** Give workflows the smallest token permissions and never expose secrets to untrusted pull-request code.
4. **Reversible by default.** Prefer labels and queues before closing, locking, or blocking.
5. **Publish the rules.** Contributors should know the policy, evidence standard, and appeal path.
6. **Protect maintainer attention.** A project may reject unsolicited work that creates more review cost than value.

## Resources

⭐ marks a strong starting point, not a paid placement. The catalog is generated from [`catalog.json`](catalog.json).

<!-- catalog:start -->

### Abuse Detection & Moderation

Detect, label, quarantine, or respond to spam, harassment, and low-quality automated contributions.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard) ⭐ | tool | Apache-2.0 | Repository abuse detection and response system for spam, harassment, and coordinated attacks. |
| [Anti Slop](https://github.com/peakoss/anti-slop) ⭐ | github-action | AGPL-3.0 | Configurable GitHub Action that detects and can close low-quality or AI-slop pull requests. |
| [GitHub AI Moderator](https://github.com/github/ai-moderator) ⭐ | github-action | MIT | AI-powered Action from GitHub that detects and labels spam in repository conversations. |
| [AI Community Moderator](https://github.com/benbalter/ai-community-moderator) | github-action | MIT | Moderates community interactions against a project's contributing guide and code of conduct. |
| [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler) | github-action | MIT | Issue-intake Action that retrieves an AI assessment and applies configurable labels. |

### Contributor Trust & Admission

Use explicit vouches or contribution history to control access without closing a project to everyone.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Fossier](https://github.com/PThorpe92/fossier) | tool | MIT | Vouch-compatible workflow and CLI for reducing unsolicited pull-request spam. |
| [Vouch](https://github.com/mitchellh/vouch) ⭐ | tool | MIT | Community trust management based on explicit vouches before a participant can contribute. |
| [Good Egg](https://github.com/2ndSetAI/good-egg) ⭐ | github-action | MIT | Scores pull-request authors using their contribution history across GitHub. |

### Intake & Triage

Reduce review load with structured intake, labels, lifecycle automation, and emergency lockdowns.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Labeler](https://github.com/actions/labeler) | github-action | MIT | Official Action for labeling pull requests from changed files and branch patterns. |
| [Stale](https://github.com/actions/stale) | github-action | MIT | Official Action for marking and optionally closing inactive issues and pull requests. |
| [Lock Threads](https://github.com/dessant/lock-threads) | github-action | MIT | Locks closed issues, pull requests, and discussions after a configurable period. |
| [Repo Lockdown](https://github.com/dessant/repo-lockdown) ⭐ | github-action | MIT | Emergency Action that immediately closes and locks new issues or pull requests. |

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
| [PRevent](https://github.com/apiiro/PRevent) | github-action | MIT | Detects suspicious pull-request changes that may indicate malicious code. |

### Policies & Playbooks

Set expectations before problems arrive and respond consistently when they do.

| Resource | Type | License | Why it matters |
| --- | --- | --- | --- |
| [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies) ⭐ | awesome-list | CC0-1.0 | Comparative catalog of how open-source projects govern AI-generated contributions. |
| [Agentic OSS Policy](https://github.com/guenp/agentic-oss-policy) | templates | Unspecified | Policy templates for protecting projects from autonomous agent abuse. |
| [OpenSSF AI-Slop Best Practices](https://github.com/ossf/wg-vulnerability-disclosures/issues/178) ⭐ | working-group | N/A | Open working-group effort to develop current practices for low-quality AI security reports and contributions. |

<!-- catalog:end -->

## Ready-to-use defenses

- [Balanced starter kit](kits/balanced) — PR template, issue form, and review-first PR quality workflow.
- [AI contribution policy](policies/AI_CONTRIBUTIONS.md) — allows responsible assistance while keeping humans accountable.
- [Unsolicited pull-request policy](policies/UNSOLICITED_PULL_REQUESTS.md) — asks contributors to align before large changes.
- [Low-quality PR response](responses/low-quality-pr.md) — concise closure text without debating whether AI was used.
- [Reproduction-needed response](responses/reproduction-needed.md) — requests the minimum evidence needed to investigate.

These templates are starting points, not legal advice. Test workflows in a non-critical repository and pin third-party Actions to full commit SHAs before production use.

## What belongs here

A resource should materially reduce maintainer exposure to abuse, review overload, unsafe contribution paths, or supply-chain risk. It must have public documentation, a clear maintainer use case, and no deceptive claims. Open-source resources are preferred; a proprietary service must offer a meaningfully useful free tier and disclose data handling.

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a resource. Entries are reviewed for relevance and safety, not accepted in exchange for stars, backlinks, or payment.

## Project status

This catalog is young and intentionally conservative. A listing is not a security endorsement. Verify licenses, permissions, data flows, maintenance status, and false-positive behavior for your own threat model.

## License

This project is available under the [MIT License](LICENSE).
