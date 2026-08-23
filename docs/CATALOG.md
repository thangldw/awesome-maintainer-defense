# Evidence-reviewed catalog

> Generated from `catalog.json` and `audits.json`. Edit the structured sources, not this file.

## Reading the evidence

Official project sources were last reviewed on **2026-08-03**. The snapshot is not an endorsement, certification, or promise of future maintenance.

Impact records the maximum documented automation effect: `low` is normally read-only; `medium` can publish, fail checks, comment, label, or modify local files; `high` can close, lock, delete, block, limit interactions, or change settings. Configuration may reduce the actual effect.

## Abuse Detection & Moderation

Detect, label, quarantine, or respond to spam, harassment, and low-quality automated contributions.

### [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard)

Repository abuse detection and response system for spam, harassment, and coordinated attacks.

- **Classification:** `tool` · `Apache-2.0` · featured
- **Deployment/default:** Hosted service, CLI, web UI, Docker, or self-hosted source; Dry-run; strong actions are opt-in
- **Maximum impact:** `high` — delete comments, close issues, lock issues, block users, set interaction limits
- **Data boundaries:** GitHub API, project-configured OpenAI-compatible model, optional hosted service
- **Access:** GitHub token; optional model endpoint and API key
- **Limitation:** AI classification is probabilistic. Review evidence and planned actions in dry-run before apply mode. GitHub does not detect the license automatically, but the repository LICENSE file contains Apache-2.0 text.
- **Repository snapshot:** archived=`false`, last push=`2026-08-21T08:38:11Z`, license detection=`NOASSERTION`
- **Evidence:** [source 1](https://github.com/Albert-Weasker/niubi_guard#what-it-does) · [source 2](https://github.com/Albert-Weasker/niubi_guard#ai-detection) · [source 3](https://github.com/Albert-Weasker/niubi_guard/blob/main/LICENSE)

### [Anti Slop](https://github.com/peakoss/anti-slop)

Configurable GitHub Action that detects and can close low-quality or AI-slop pull requests.

- **Classification:** `github-action` · `AGPL-3.0` · featured
- **Deployment/default:** GitHub Action; Enforcement; the documented quick start closes a PR after the failure threshold
- **Maximum impact:** `high` — label, comment, close PR, lock PR
- **Data boundaries:** GitHub API
- **Access:** Recommended: contents read, issues read, pull requests write
- **Limitation:** Heuristics include account and contribution-history signals, so legitimate newcomers can be flagged. Set close-pr and lock-pr to false during evaluation.
- **Repository snapshot:** archived=`false`, last push=`2026-04-15T16:37:26Z`, license detection=`AGPL-3.0`
- **Evidence:** [source 1](https://github.com/peakoss/anti-slop#quick-start) · [source 2](https://github.com/peakoss/anti-slop#recommended-permissions)

### [GitHub AI Moderator](https://github.com/github/ai-moderator)

Model-powered Action that labels spam, link spam, and content it infers to be AI-generated.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Applies moderation output unless dry-run is enabled
- **Maximum impact:** `medium` — label, minimize comment
- **Data boundaries:** GitHub API, GitHub Models
- **Access:** GitHub token plus models read and write access needed for configured moderation actions
- **Limitation:** Repository content is sent to a model endpoint and model judgments can be wrong. Its built-in AI-authorship prompt is not proof of authorship; disable it for enforcement. GitHub Models paid usage may apply after free limits.
- **Repository snapshot:** archived=`false`, last push=`2026-08-17T18:18:19Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github/ai-moderator#usage) · [source 2](https://github.com/github/ai-moderator#inputs)

### [AI Community Moderator](https://github.com/benbalter/ai-community-moderator)

Moderates community interactions against a project's contributing guide and code of conduct.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Model-driven moderation using project guidelines
- **Maximum impact:** `high` — comment, hide content, lock discussion, limit interactions
- **Data boundaries:** GitHub API, GitHub Models
- **Access:** GitHub token, models read, and write permissions for enabled actions
- **Limitation:** A language model interprets community standards; ambiguous or multilingual content needs human review and an appeal path.
- **Repository snapshot:** archived=`false`, last push=`2025-11-20T02:13:17Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/benbalter/ai-community-moderator#features) · [source 2](https://github.com/benbalter/ai-community-moderator#permissions)

### [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler)

Issue-intake Action that retrieves an AI assessment and applies configurable labels.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Posts a structured assessment and applies configured labels
- **Maximum impact:** `medium` — comment, label
- **Data boundaries:** GitHub API, GitHub Models or a compatible endpoint
- **Access:** GitHub token, models read, issues write, and contents read for prompt files
- **Limitation:** The assessment is model-generated, not factual proof. Prompt changes and model changes can alter classification behavior.
- **Repository snapshot:** archived=`false`, last push=`2025-10-16T13:20:30Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github/ai-assessment-comment-labeler#overview) · [source 2](https://github.com/github/ai-assessment-comment-labeler#required-permissions)

## Contributor Trust & Admission

Use explicit vouches or contribution history to control access without closing a project to everyone.

### [Fossier](https://github.com/PThorpe92/fossier)

Vouch-compatible workflow and CLI for reducing unsolicited pull-request spam.

- **Classification:** `tool` · `MIT`
- **Deployment/default:** GitHub Action and CLI; Allows, reviews, or denies based on trust tier and a multi-signal score
- **Maximum impact:** `high` — label, comment, close PR
- **Data boundaries:** GitHub API, optional Fossier registry
- **Access:** GitHub token with pull-request write access; optional registry API key
- **Limitation:** History-based scoring and optional AI co-author rejection can exclude legitimate contributors. Low-confidence cases are forced to review, but maintainers should still test thresholds.
- **Repository snapshot:** archived=`false`, last push=`2026-07-06T16:53:54Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/PThorpe92/fossier#how-it-works) · [source 2](https://github.com/PThorpe92/fossier#github-action)

### [Vouch](https://github.com/mitchellh/vouch)

Community trust management based on explicit vouches before a participant can contribute.

- **Classification:** `tool` · `MIT` · featured
- **Deployment/default:** GitHub Actions and a repository trust file; Explicit admission based on project-defined vouches and denouncements
- **Maximum impact:** `high` — fail check, close issue, lock issue, close PR
- **Data boundaries:** GitHub API, repository trust file
- **Access:** Depends on action; write permission is required for close or lock behavior
- **Limitation:** Explicit trust can protect attention but can also create a closed or biased contributor network. Define transparent nomination and appeal rules.
- **Repository snapshot:** archived=`false`, last push=`2026-08-23T03:12:49Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/mitchellh/vouch#who-is-vouched) · [source 2](https://github.com/mitchellh/vouch#github-actions)

### [Good Egg](https://github.com/2ndSetAI/good-egg)

Scores pull-request authors using their contribution history across GitHub.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action, CLI, Python package, and MCP server; Posts a trust-score comment; fail-on-low is false by default
- **Maximum impact:** `medium` — comment, create check, fail check
- **Data boundaries:** GitHub API, Python package registry during Action installation
- **Access:** GitHub token; pull-request write for comments and optional checks write
- **Limitation:** Past merge history is an imperfect proxy for trust and can disadvantage new or private contributors. The Action installs a version-ranged package from PyPI at runtime.
- **Repository snapshot:** archived=`false`, last push=`2026-04-12T17:55:02Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/2ndSetAI/good-egg#github-action) · [source 2](https://github.com/2ndSetAI/good-egg#scoring-models)

## Intake & Triage

Reduce review load with structured intake, labels, lifecycle automation, and emergency lockdowns.

### [Labeler](https://github.com/actions/labeler)

Official Action for labeling pull requests from changed files and branch patterns.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Adds or removes labels according to repository configuration
- **Maximum impact:** `medium` — add label, remove label
- **Data boundaries:** GitHub API
- **Access:** Contents read and pull requests write
- **Limitation:** Using pull_request_target is dangerous if the same workflow checks out or executes untrusted PR code. Labeling rules can misroute contributions.
- **Repository snapshot:** archived=`false`, last push=`2026-08-10T05:45:33Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/labeler#recommended-permissions) · [source 2](https://github.com/actions/labeler#notes-regarding-pull_request_target-event)

### [Stale](https://github.com/actions/stale)

Official Action for marking and optionally closing inactive issues and pull requests.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Marks inactivity and closes after the configured grace period
- **Maximum impact:** `high` — label, comment, close issue, close PR, delete branch
- **Data boundaries:** GitHub API
- **Access:** Issues and pull requests write; contents write only when deleting branches
- **Limitation:** Inactivity does not mean low value. Exempt security, roadmap, accessibility, and confirmed-bug labels before enabling closure.
- **Repository snapshot:** archived=`false`, last push=`2026-08-07T11:29:42Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/stale#recommended-permissions) · [source 2](https://github.com/actions/stale#all-options)

### [Lock Threads](https://github.com/dessant/lock-threads)

Locks closed issues, pull requests, and discussions after a configurable period.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action; Locks closed threads after configured inactivity
- **Maximum impact:** `high` — lock issue, lock PR, lock discussion
- **Data boundaries:** GitHub API
- **Access:** Write permission for each enabled issue, pull-request, or discussion scope
- **Limitation:** Locking prevents late corrections and support follow-up. Exclusions and a clear path to open a new issue are important.
- **Repository snapshot:** archived=`false`, last push=`2026-06-26T18:23:49Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/dessant/lock-threads#usage)

### [Repo Lockdown](https://github.com/dessant/repo-lockdown)

Emergency Action that immediately closes and locks new issues or pull requests.

- **Classification:** `github-action` · `MIT` · featured
- **Deployment/default:** GitHub Action; Immediately closes and locks configured new issues or pull requests
- **Maximum impact:** `high` — label, comment, close, lock
- **Data boundaries:** GitHub API
- **Access:** Issues and/or pull requests write
- **Limitation:** This is a blunt emergency control intended for repositories that do not accept submissions or for temporary incidents, not routine triage.
- **Repository snapshot:** archived=`false`, last push=`2026-06-26T18:23:39Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/dessant/repo-lockdown#usage)

### [Issue Metrics](https://github.com/github-community-projects/issue-metrics)

Measures issue, pull-request, and discussion response times and generates a Markdown report.

- **Classification:** `github-action` · `MIT`
- **Deployment/default:** GitHub Action or containerized tool; Reads repository activity and writes a Markdown report file
- **Maximum impact:** `medium` — write report file in the workflow workspace
- **Data boundaries:** GitHub API, workflow workspace
- **Access:** Issues, pull requests, or discussions read according to the search query; publishing requires a separate step and permission
- **Limitation:** Response-time metrics do not measure answer quality or maintainer wellbeing. The official example uses a separate Action to publish the generated file as an issue; this tool does not publish it by itself.
- **Repository snapshot:** archived=`false`, last push=`2026-08-20T18:02:26Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github-community-projects/issue-metrics#available-metrics) · [source 2](https://github.com/github-community-projects/issue-metrics#usage)

## Repository Governance & Access

Keep security policies, branch protections, and repository settings consistent across projects.

### [OpenSSF Allstar](https://github.com/ossf/allstar)

Continuously checks and enforces security policies across GitHub organizations.

- **Classification:** `github-app` · `Apache-2.0` · featured
- **Deployment/default:** OpenSSF-operated or self-hosted GitHub App; Reports policy violations as issues in the quick start
- **Maximum impact:** `high` — create issue, create check, block noncompliant changes
- **Data boundaries:** GitHub API, OpenSSF-operated service when using the public app
- **Access:** Read access to most repository settings and contents; issues and checks write for reporting and block mode
- **Limitation:** Organization-wide policy mistakes can affect many repositories. Start with opt-in scope and issue reporting before block enforcement.
- **Repository snapshot:** archived=`false`, last push=`2026-08-19T21:27:39Z`, license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/allstar#using-the-public-allstar-app) · [source 2](https://github.com/ossf/allstar#configuration-definitions)

### [Safe Settings](https://github.com/github-community-projects/safe-settings)

Centrally manages repository settings, branch protections, and teams with pull-request dry runs.

- **Classification:** `github-app` · `ISC` · featured
- **Deployment/default:** GitHub App; Applies default-branch settings; pull-request changes are evaluated in dry-run
- **Maximum impact:** `high` — change repository settings, change branch protection, change teams, rename repository
- **Data boundaries:** GitHub API, central admin repository
- **Access:** Broad organization and repository administration permissions
- **Limitation:** Configuration errors have organization-wide blast radius. Restrict managed repositories, protect the admin repository, and require review for settings changes.
- **Repository snapshot:** archived=`false`, last push=`2026-08-20T20:44:04Z`, license detection=`ISC`
- **Evidence:** [source 1](https://github.com/github-community-projects/safe-settings#how-it-works) · [source 2](https://github.com/github-community-projects/safe-settings#restrict-repositories)

### [Repository Settings App](https://github.com/repository-settings/app)

Synchronizes repository settings from a version-controlled `.github/settings.yml` file.

- **Classification:** `github-app` · `ISC`
- **Deployment/default:** GitHub App; Synchronizes settings from `.github/settings.yml`
- **Maximum impact:** `high` — change repository settings, change permissions, change branch protection
- **Data boundaries:** GitHub API, repository configuration file
- **Access:** Repository administration permissions
- **Limitation:** Anyone able to merge settings changes may gain or alter administrative access. Protect the configuration path with CODEOWNERS and required review.
- **Repository snapshot:** archived=`false`, last push=`2026-08-22T12:31:58Z`, license detection=`ISC`
- **Evidence:** [source 1](https://github.com/repository-settings/app#repository-settings-app) · [source 2](https://github.com/repository-settings/app#security-implications)

## Workflow & Supply-Chain Defense

Protect CI, dependencies, secrets, and merge paths from hostile or compromised contributions.

### [Harden-Runner](https://github.com/step-security/harden-runner)

Monitors network egress, file integrity, and processes on GitHub-hosted runners.

- **Classification:** `github-action` · `Apache-2.0` · featured
- **Deployment/default:** GitHub Action plus StepSecurity service; self-hosted runner support depends on tier; Audit network, file, and process activity
- **Maximum impact:** `high` — observe workflow runtime, block network egress
- **Data boundaries:** runner telemetry, StepSecurity service
- **Access:** Runs first in a CI job and observes process, file, and network activity
- **Limitation:** The community and enterprise tiers differ, and monitoring data is presented through an external service. Review data handling and supported runner type before adoption.
- **Repository snapshot:** archived=`false`, last push=`2026-08-15T06:05:32Z`, license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/step-security/harden-runner#community-free) · [source 2](https://github.com/step-security/harden-runner#how-it-works)

### [OpenSSF Scorecard](https://github.com/ossf/scorecard)

Automated security-health checks for open-source projects and their dependencies.

- **Classification:** `tool` · `Apache-2.0` · featured
- **Deployment/default:** CLI, GitHub Action, REST API, and public dataset; Read-only heuristic assessment
- **Maximum impact:** `low` — produce score, produce SARIF when configured
- **Data boundaries:** GitHub API, optional Scorecard API and public dataset
- **Access:** Repository metadata read; additional permissions when uploading SARIF
- **Limitation:** Scorecard documents that checks are heuristics with false positives and negatives. Weekly public results omit some checks and can be stale.
- **Repository snapshot:** archived=`false`, last push=`2026-08-19T20:44:10Z`, license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/scorecard#scorecard-checks) · [source 2](https://github.com/ossf/scorecard#public-data)

### [zizmor](https://github.com/zizmorcore/zizmor)

Static analysis for security and correctness problems in GitHub Actions workflows.

- **Classification:** `tool` · `MIT` · featured
- **Deployment/default:** Local CLI, package, or CI check; Read-only static analysis
- **Maximum impact:** `low` — report findings, fail check when configured
- **Data boundaries:** local files, optional GitHub API for online audits
- **Access:** Read access to workflow files; optional GitHub token
- **Limitation:** Static analysis cannot prove a workflow is safe and may miss runtime or third-party Action behavior. Review findings in context.
- **Repository snapshot:** archived=`false`, last push=`2026-08-23T05:43:32Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/zizmorcore/zizmor) · [source 2](https://docs.zizmor.sh/audits/)

### [pinact](https://github.com/suzuki-shunsuke/pinact)

Pins GitHub Actions and reusable workflows to immutable commit hashes.

- **Classification:** `tool` · `MIT`
- **Deployment/default:** Local CLI or CI check; Modifies files when pinning; supports a non-modifying verification mode
- **Maximum impact:** `medium` — rewrite Action references, fail verification
- **Data boundaries:** local files, GitHub API unless offline mode is used
- **Access:** Filesystem write for fixes; optional GitHub token for release and tag lookup
- **Limitation:** A pinned SHA limits tag movement but does not make third-party code trustworthy. Offline mode only checks SHA syntax.
- **Repository snapshot:** archived=`false`, last push=`2026-08-23T02:09:51Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/suzuki-shunsuke/pinact#offline-check---no-api) · [source 2](https://github.com/suzuki-shunsuke/pinact#update-actions--update)

### [Dependency Review Action](https://github.com/actions/dependency-review-action)

Blocks pull requests that introduce vulnerable dependencies or disallowed licenses.

- **Classification:** `github-action` · `MIT` · featured
- **Deployment/default:** GitHub Action; Fails when configured vulnerability or license criteria are violated
- **Maximum impact:** `medium` — fail check, comment summary when configured
- **Data boundaries:** GitHub Dependency Graph API
- **Access:** Contents read and pull requests read; optional pull requests write for comments
- **Limitation:** Supported for public repositories and private repositories with GitHub Advanced Security. Results depend on dependency graph coverage and advisory data.
- **Repository snapshot:** archived=`false`, last push=`2026-08-11T00:33:37Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/dependency-review-action#dependency-review-action) · [source 2](https://github.com/actions/dependency-review-action#configuration-options)

### [TruffleHog](https://github.com/trufflesecurity/trufflehog)

Finds and verifies leaked credentials before they become a maintainer incident.

- **Classification:** `tool` · `AGPL-3.0`
- **Deployment/default:** CLI, container, and CI integrations; Scans and can verify discovered credentials
- **Maximum impact:** `low` — report secret, make credential-verification requests
- **Data boundaries:** scanned source, credential providers during verification
- **Access:** Read access to scan targets; network access for verification
- **Limitation:** Verification can send authentication requests to third-party services. Redact output, scope scans carefully, and treat findings as sensitive incident data.
- **Repository snapshot:** archived=`false`, last push=`2026-08-23T05:33:25Z`, license detection=`AGPL-3.0`
- **Evidence:** [source 1](https://github.com/trufflesecurity/trufflehog#what-is-secret-verification) · [source 2](https://github.com/trufflesecurity/trufflehog#usage)

### [PRevent](https://github.com/apiiro/PRevent)

Detects suspicious pull-request changes that may indicate malicious code.

- **Classification:** `github-app` · `MIT`
- **Deployment/default:** Self-hosted GitHub App; Scans configured languages for suspicious patterns and can gate merge
- **Maximum impact:** `high` — report finding, block merge pending review
- **Data boundaries:** GitHub API, self-hosted scanner, configured secret manager
- **Access:** GitHub App private key, webhook secret, repository contents, and checks or status permissions
- **Limitation:** Rules focus on dynamic execution and obfuscation in supported languages; passing does not prove a contribution is benign. Deployment requires operating a privileged GitHub App.
- **Repository snapshot:** archived=`false`, last push=`2026-01-08T08:10:14Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/apiiro/PRevent#how-it-works) · [source 2](https://github.com/apiiro/PRevent#supported-languages)

### [OSV-Scanner](https://github.com/google/osv-scanner)

Scans lockfiles, SBOMs, and source artifacts against the OSV vulnerability database.

- **Classification:** `tool` · `Apache-2.0` · featured
- **Deployment/default:** CLI, container, and CI integrations; Read-only vulnerability and license scan
- **Maximum impact:** `medium` — fail check, modify dependency files in guided remediation
- **Data boundaries:** OSV API and deps.dev, offline database option
- **Access:** Read access to dependency artifacts; filesystem and package-manager access for fix mode
- **Limitation:** Coverage varies by ecosystem. Guided remediation can execute package-manager behavior from untrusted projects; do not run fix mode on untrusted code.
- **Repository snapshot:** archived=`false`, last push=`2026-08-22T21:02:18Z`, license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/google/osv-scanner#offline-mode) · [source 2](https://github.com/google/osv-scanner#guided-remediation)

### [Gitleaks](https://github.com/gitleaks/gitleaks)

Detects secrets in Git history, directories, files, and standard input.

- **Classification:** `tool` · `MIT` · featured
- **Deployment/default:** CLI, pre-commit hook, and CI integrations; Read-only pattern-based secret detection
- **Maximum impact:** `low` — report finding, fail check
- **Data boundaries:** local scan target
- **Access:** Read access to files or Git history
- **Limitation:** Pattern detection has false positives and false negatives. Keep output redacted and rotate any real credential rather than merely deleting it from the latest commit.
- **Repository snapshot:** archived=`false`, last push=`2026-08-19T04:15:06Z`, license detection=`MIT`
- **Evidence:** [source 1](https://github.com/gitleaks/gitleaks#readme) · [source 2](https://github.com/gitleaks/gitleaks#commands)

## Policies & Playbooks

Set expectations before problems arrive and respond consistently when they do.

### [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies)

Comparative catalog of how open-source projects govern AI-generated contributions.

- **Classification:** `awesome-list` · `CC0-1.0` · featured
- **Deployment/default:** Reference catalog; Documentation only
- **Maximum impact:** `low` — none
- **Data boundaries:** none
- **Access:** None
- **Limitation:** Policies differ by project and can change after collection. Confirm each linked source and seek legal advice for copyright, labor, or privacy questions.
- **Repository snapshot:** archived=`false`, last push=`2026-08-20T21:05:24Z`, license detection=`CC0-1.0`
- **Evidence:** [source 1](https://github.com/melissawm/open-source-ai-contribution-policies)

### [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)

Open work item developing practices for low-quality AI security reports and contributions; not a finalized standard.

- **Classification:** `working-group` · `N/A`
- **Deployment/default:** Open working-group issue; Discussion and planned deliverables only
- **Maximum impact:** `low` — none
- **Data boundaries:** public GitHub discussion
- **Access:** None
- **Limitation:** This is an open work item, not a finished best-practices document, standard, or OpenSSF certification.
- **Repository snapshot:** archived=`false`, last push=`2026-02-04T16:32:52Z`, license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)
