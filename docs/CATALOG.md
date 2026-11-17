# Evidence-reviewed catalog

> Generated from `catalog.json` and `audits.json`. Edit the structured sources, not this file.

## Reading the evidence

Official project sources were last reviewed on **2026-08-03**. The snapshot is not an endorsement, certification, or promise of future maintenance. Access, data boundaries, and repository snapshots are recorded in `audits.json`.

Impact records the maximum documented automation effect: `low` is normally read-only; `medium` can publish, fail checks, comment, label, or modify local files; `high` can close, lock, delete, block, limit interactions, or change settings. Configuration may reduce the actual effect.

## Abuse Detection & Moderation

Detect, label, quarantine, or respond to spam, harassment, and low-quality automated contributions.

### [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard)

Repository abuse detection and response system for spam, harassment, and coordinated attacks.

- `tool` · `Apache-2.0` · featured · impact `high` (delete comments, close issues, lock issues, block users, set interaction limits)
- **Default:** Dry-run; strong actions are opt-in
- **Limitation:** AI classification is probabilistic. Review evidence and planned actions in dry-run before apply mode. GitHub does not detect the license automatically, but the repository LICENSE file contains Apache-2.0 text.
- **Evidence:** [source 1](https://github.com/Albert-Weasker/niubi_guard#what-it-does) · [source 2](https://github.com/Albert-Weasker/niubi_guard#ai-detection) · [source 3](https://github.com/Albert-Weasker/niubi_guard/blob/main/LICENSE)

### [Anti Slop](https://github.com/peakoss/anti-slop)

Configurable GitHub Action that detects and can close low-quality or AI-slop pull requests.

- `github-action` · `AGPL-3.0` · featured · impact `high` (label, comment, close PR, lock PR)
- **Default:** Enforcement; the documented quick start closes a PR after the failure threshold
- **Limitation:** Heuristics include account and contribution-history signals, so legitimate newcomers can be flagged. Set close-pr and lock-pr to false during evaluation.
- **Evidence:** [source 1](https://github.com/peakoss/anti-slop#quick-start) · [source 2](https://github.com/peakoss/anti-slop#recommended-permissions)

### [GitHub AI Moderator](https://github.com/github/ai-moderator)

Model-powered Action that labels spam, link spam, and content it infers to be AI-generated.

- `github-action` · `MIT` · impact `medium` (label, minimize comment)
- **Default:** Applies moderation output unless dry-run is enabled
- **Limitation:** Repository content is sent to a model endpoint and model judgments can be wrong. Its built-in AI-authorship prompt is not proof of authorship; disable it for enforcement. GitHub Models paid usage may apply after free limits.
- **Evidence:** [source 1](https://github.com/github/ai-moderator#usage) · [source 2](https://github.com/github/ai-moderator#inputs)

### [AI Community Moderator](https://github.com/benbalter/ai-community-moderator)

Moderates community interactions against a project's contributing guide and code of conduct.

- `github-action` · `MIT` · impact `high` (comment, hide content, lock discussion, limit interactions)
- **Default:** Model-driven moderation using project guidelines
- **Limitation:** A language model interprets community standards; ambiguous or multilingual content needs human review and an appeal path.
- **Evidence:** [source 1](https://github.com/benbalter/ai-community-moderator#features) · [source 2](https://github.com/benbalter/ai-community-moderator#permissions)

### [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler)

Issue-intake Action that retrieves an AI assessment and applies configurable labels.

- `github-action` · `MIT` · impact `medium` (comment, label)
- **Default:** Posts a structured assessment and applies configured labels
- **Limitation:** The assessment is model-generated, not factual proof. Prompt changes and model changes can alter classification behavior.
- **Evidence:** [source 1](https://github.com/github/ai-assessment-comment-labeler#overview) · [source 2](https://github.com/github/ai-assessment-comment-labeler#required-permissions)

## Contributor Trust & Admission

Use explicit vouches or contribution history to control access without closing a project to everyone.

### [Fossier](https://github.com/PThorpe92/fossier)

Vouch-compatible workflow and CLI for reducing unsolicited pull-request spam.

- `tool` · `MIT` · impact `high` (label, comment, close PR)
- **Default:** Allows, reviews, or denies based on trust tier and a multi-signal score
- **Limitation:** History-based scoring and optional AI co-author rejection can exclude legitimate contributors. Low-confidence cases are forced to review, but maintainers should still test thresholds.
- **Evidence:** [source 1](https://github.com/PThorpe92/fossier#how-it-works) · [source 2](https://github.com/PThorpe92/fossier#github-action)

### [Vouch](https://github.com/mitchellh/vouch)

Community trust management based on explicit vouches before a participant can contribute.

- `tool` · `MIT` · featured · impact `high` (fail check, close issue, lock issue, close PR)
- **Default:** Explicit admission based on project-defined vouches and denouncements
- **Limitation:** Explicit trust can protect attention but can also create a closed or biased contributor network. Define transparent nomination and appeal rules.
- **Evidence:** [source 1](https://github.com/mitchellh/vouch#who-is-vouched) · [source 2](https://github.com/mitchellh/vouch#github-actions)

### [Good Egg](https://github.com/2ndSetAI/good-egg)

Scores pull-request authors using their contribution history across GitHub.

- `github-action` · `MIT` · impact `medium` (comment, create check, fail check)
- **Default:** Posts a trust-score comment; fail-on-low is false by default
- **Limitation:** Past merge history is an imperfect proxy for trust and can disadvantage new or private contributors. The Action installs a version-ranged package from PyPI at runtime.
- **Evidence:** [source 1](https://github.com/2ndSetAI/good-egg#github-action) · [source 2](https://github.com/2ndSetAI/good-egg#scoring-models)

## Intake & Triage

Reduce review load with structured intake, labels, lifecycle automation, and emergency lockdowns.

### [Labeler](https://github.com/actions/labeler)

Official Action for labeling pull requests from changed files and branch patterns.

- `github-action` · `MIT` · impact `medium` (add label, remove label)
- **Default:** Adds or removes labels according to repository configuration
- **Limitation:** Using pull_request_target is dangerous if the same workflow checks out or executes untrusted PR code. Labeling rules can misroute contributions.
- **Evidence:** [source 1](https://github.com/actions/labeler#recommended-permissions) · [source 2](https://github.com/actions/labeler#notes-regarding-pull_request_target-event)

### [Stale](https://github.com/actions/stale)

Official Action for marking and optionally closing inactive issues and pull requests.

- `github-action` · `MIT` · impact `high` (label, comment, close issue, close PR, delete branch)
- **Default:** Marks inactivity and closes after the configured grace period
- **Limitation:** Inactivity does not mean low value. Exempt security, roadmap, accessibility, and confirmed-bug labels before enabling closure.
- **Evidence:** [source 1](https://github.com/actions/stale#recommended-permissions) · [source 2](https://github.com/actions/stale#all-options)

### [Lock Threads](https://github.com/dessant/lock-threads)

Locks closed issues, pull requests, and discussions after a configurable period.

- `github-action` · `MIT` · impact `high` (lock issue, lock PR, lock discussion)
- **Default:** Locks closed threads after configured inactivity
- **Limitation:** Locking prevents late corrections and support follow-up. Exclusions and a clear path to open a new issue are important.
- **Evidence:** [source 1](https://github.com/dessant/lock-threads#usage)

### [Repo Lockdown](https://github.com/dessant/repo-lockdown)

Emergency Action that immediately closes and locks new issues or pull requests.

- `github-action` · `MIT` · featured · impact `high` (label, comment, close, lock)
- **Default:** Immediately closes and locks configured new issues or pull requests
- **Limitation:** This is a blunt emergency control intended for repositories that do not accept submissions or for temporary incidents, not routine triage.
- **Evidence:** [source 1](https://github.com/dessant/repo-lockdown#usage)

### [Issue Metrics](https://github.com/github-community-projects/issue-metrics)

Measures issue, pull-request, and discussion response times and generates a Markdown report.

- `github-action` · `MIT` · impact `medium` (write report file in the workflow workspace)
- **Default:** Reads repository activity and writes a Markdown report file
- **Limitation:** Response-time metrics do not measure answer quality or maintainer wellbeing. The official example uses a separate Action to publish the generated file as an issue; this tool does not publish it by itself.
- **Evidence:** [source 1](https://github.com/github-community-projects/issue-metrics#available-metrics) · [source 2](https://github.com/github-community-projects/issue-metrics#usage)

## Repository Governance & Access

Keep security policies, branch protections, and repository settings consistent across projects.

### [OpenSSF Allstar](https://github.com/ossf/allstar)

Continuously checks and enforces security policies across GitHub organizations.

- `github-app` · `Apache-2.0` · featured · impact `high` (create issue, create check, block noncompliant changes)
- **Default:** Reports policy violations as issues in the quick start
- **Limitation:** Organization-wide policy mistakes can affect many repositories. Start with opt-in scope and issue reporting before block enforcement.
- **Evidence:** [source 1](https://github.com/ossf/allstar#using-the-public-allstar-app) · [source 2](https://github.com/ossf/allstar#configuration-definitions)

### [Safe Settings](https://github.com/github-community-projects/safe-settings)

Centrally manages repository settings, branch protections, and teams with pull-request dry runs.

- `github-app` · `ISC` · featured · impact `high` (change repository settings, change branch protection, change teams, rename repository)
- **Default:** Applies default-branch settings; pull-request changes are evaluated in dry-run
- **Limitation:** Configuration errors have organization-wide blast radius. Restrict managed repositories, protect the admin repository, and require review for settings changes.
- **Evidence:** [source 1](https://github.com/github-community-projects/safe-settings#how-it-works) · [source 2](https://github.com/github-community-projects/safe-settings#restrict-repositories)

### [Repository Settings App](https://github.com/repository-settings/app)

Synchronizes repository settings from a version-controlled `.github/settings.yml` file.

- `github-app` · `ISC` · impact `high` (change repository settings, change permissions, change branch protection)
- **Default:** Synchronizes settings from `.github/settings.yml`
- **Limitation:** Anyone able to merge settings changes may gain or alter administrative access. Protect the configuration path with CODEOWNERS and required review.
- **Evidence:** [source 1](https://github.com/repository-settings/app#repository-settings-app) · [source 2](https://github.com/repository-settings/app#security-implications)

## Workflow & Supply-Chain Defense

Protect CI, dependencies, secrets, and merge paths from hostile or compromised contributions.

### [Harden-Runner](https://github.com/step-security/harden-runner)

Monitors network egress, file integrity, and processes on GitHub-hosted runners.

- `github-action` · `Apache-2.0` · featured · impact `high` (observe workflow runtime, block network egress)
- **Default:** Audit network, file, and process activity
- **Limitation:** The community and enterprise tiers differ, and monitoring data is presented through an external service. Review data handling and supported runner type before adoption.
- **Evidence:** [source 1](https://github.com/step-security/harden-runner#community-free) · [source 2](https://github.com/step-security/harden-runner#how-it-works)

### [OpenSSF Scorecard](https://github.com/ossf/scorecard)

Automated security-health checks for open-source projects and their dependencies.

- `tool` · `Apache-2.0` · featured · impact `low` (produce score, produce SARIF when configured)
- **Default:** Read-only heuristic assessment
- **Limitation:** Scorecard documents that checks are heuristics with false positives and negatives. Weekly public results omit some checks and can be stale.
- **Evidence:** [source 1](https://github.com/ossf/scorecard#scorecard-checks) · [source 2](https://github.com/ossf/scorecard#public-data)

### [zizmor](https://github.com/zizmorcore/zizmor)

Static analysis for security and correctness problems in GitHub Actions workflows.

- `tool` · `MIT` · featured · impact `low` (report findings, fail check when configured)
- **Default:** Read-only static analysis
- **Limitation:** Static analysis cannot prove a workflow is safe and may miss runtime or third-party Action behavior. Review findings in context.
- **Evidence:** [source 1](https://github.com/zizmorcore/zizmor) · [source 2](https://docs.zizmor.sh/audits/)

### [pinact](https://github.com/suzuki-shunsuke/pinact)

Pins GitHub Actions and reusable workflows to immutable commit hashes.

- `tool` · `MIT` · impact `medium` (rewrite Action references, fail verification)
- **Default:** Modifies files when pinning; supports a non-modifying verification mode
- **Limitation:** A pinned SHA limits tag movement but does not make third-party code trustworthy. Offline mode only checks SHA syntax.
- **Evidence:** [source 1](https://github.com/suzuki-shunsuke/pinact#offline-check---no-api) · [source 2](https://github.com/suzuki-shunsuke/pinact#update-actions--update)

### [Dependency Review Action](https://github.com/actions/dependency-review-action)

Blocks pull requests that introduce vulnerable dependencies or disallowed licenses.

- `github-action` · `MIT` · featured · impact `medium` (fail check, comment summary when configured)
- **Default:** Fails when configured vulnerability or license criteria are violated
- **Limitation:** Supported for public repositories and private repositories with GitHub Advanced Security. Results depend on dependency graph coverage and advisory data.
- **Evidence:** [source 1](https://github.com/actions/dependency-review-action#dependency-review-action) · [source 2](https://github.com/actions/dependency-review-action#configuration-options)

### [TruffleHog](https://github.com/trufflesecurity/trufflehog)

Finds and verifies leaked credentials before they become a maintainer incident.

- `tool` · `AGPL-3.0` · impact `low` (report secret, make credential-verification requests)
- **Default:** Scans and can verify discovered credentials
- **Limitation:** Verification can send authentication requests to third-party services. Redact output, scope scans carefully, and treat findings as sensitive incident data.
- **Evidence:** [source 1](https://github.com/trufflesecurity/trufflehog#what-is-secret-verification) · [source 2](https://github.com/trufflesecurity/trufflehog#usage)

### [PRevent](https://github.com/apiiro/PRevent)

Detects suspicious pull-request changes that may indicate malicious code.

- `github-app` · `MIT` · impact `high` (report finding, block merge pending review)
- **Default:** Scans configured languages for suspicious patterns and can gate merge
- **Limitation:** Rules focus on dynamic execution and obfuscation in supported languages; passing does not prove a contribution is benign. Deployment requires operating a privileged GitHub App.
- **Evidence:** [source 1](https://github.com/apiiro/PRevent#how-it-works) · [source 2](https://github.com/apiiro/PRevent#supported-languages)

### [OSV-Scanner](https://github.com/google/osv-scanner)

Scans lockfiles, SBOMs, and source artifacts against the OSV vulnerability database.

- `tool` · `Apache-2.0` · featured · impact `medium` (fail check, modify dependency files in guided remediation)
- **Default:** Read-only vulnerability and license scan
- **Limitation:** Coverage varies by ecosystem. Guided remediation can execute package-manager behavior from untrusted projects; do not run fix mode on untrusted code.
- **Evidence:** [source 1](https://github.com/google/osv-scanner#offline-mode) · [source 2](https://github.com/google/osv-scanner#guided-remediation)

### [Gitleaks](https://github.com/gitleaks/gitleaks)

Detects secrets in Git history, directories, files, and standard input.

- `tool` · `MIT` · featured · impact `low` (report finding, fail check)
- **Default:** Read-only pattern-based secret detection
- **Limitation:** Pattern detection has false positives and false negatives. Keep output redacted and rotate any real credential rather than merely deleting it from the latest commit.
- **Evidence:** [source 1](https://github.com/gitleaks/gitleaks#readme) · [source 2](https://github.com/gitleaks/gitleaks#commands)

## Policies & Playbooks

Set expectations before problems arrive and respond consistently when they do.

### [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies)

Comparative catalog of how open-source projects govern AI-generated contributions.

- `awesome-list` · `CC0-1.0` · featured · impact `low` (none)
- **Default:** Documentation only
- **Limitation:** Policies differ by project and can change after collection. Confirm each linked source and seek legal advice for copyright, labor, or privacy questions.
- **Evidence:** [source 1](https://github.com/melissawm/open-source-ai-contribution-policies)

### [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)

Open work item developing practices for low-quality AI security reports and contributions; not a finalized standard.

- `working-group` · `N/A` · impact `low` (none)
- **Default:** Discussion and planned deliverables only
- **Limitation:** This is an open work item, not a finished best-practices document, standard, or OpenSSF certification.
- **Evidence:** [source 1](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)
