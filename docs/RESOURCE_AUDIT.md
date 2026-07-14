# Resource audit

Verified against official project sources on **2026-07-14**.
Repository activity is a point-in-time snapshot, not an endorsement or a guarantee of future maintenance.

## How to read this audit

- **Low impact:** read-only analysis or documentation in normal use.
- **Medium impact:** can label, comment, fail checks, publish reports, or modify local files.
- **High impact:** can close, lock, delete, block, limit interactions, or change repository settings.
- Impact is maximum documented capability, not a security score. Actual behavior depends on configuration.
- Data boundaries identify where repository content, metadata, or credentials may travel. Verify current privacy terms yourself.

## Abuse Detection & Moderation

### [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard)

- **Deployment:** Hosted service, CLI, web UI, Docker, or self-hosted source
- **Default mode:** Dry-run; strong actions are opt-in
- **Maximum automation impact:** HIGH — delete comments, close issues, lock issues, block users, set interaction limits
- **Data boundaries:** GitHub API, project-configured OpenAI-compatible model, optional hosted service
- **Access:** GitHub token; optional model endpoint and API key
- **Important limitation:** AI classification is probabilistic. Review evidence and planned actions in dry-run before apply mode. GitHub does not detect the license automatically, but the repository LICENSE file contains Apache-2.0 text.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-09T11:54:36Z`, GitHub license detection=`NOASSERTION`
- **Evidence:** [source 1](https://github.com/Albert-Weasker/niubi_guard#what-it-does) · [source 2](https://github.com/Albert-Weasker/niubi_guard#ai-detection) · [source 3](https://github.com/Albert-Weasker/niubi_guard/blob/main/LICENSE)

### [Anti Slop](https://github.com/peakoss/anti-slop)

- **Deployment:** GitHub Action
- **Default mode:** Enforcement; the documented quick start closes a PR after the failure threshold
- **Maximum automation impact:** HIGH — label, comment, close PR, lock PR
- **Data boundaries:** GitHub API
- **Access:** Recommended: contents read, issues read, pull requests write
- **Important limitation:** Heuristics include account and contribution-history signals, so legitimate newcomers can be flagged. Set close-pr and lock-pr to false during evaluation.
- **Repository snapshot:** archived=`false`, last source push=`2026-04-15T16:37:26Z`, GitHub license detection=`AGPL-3.0`
- **Evidence:** [source 1](https://github.com/peakoss/anti-slop#quick-start) · [source 2](https://github.com/peakoss/anti-slop#recommended-permissions)

### [GitHub AI Moderator](https://github.com/github/ai-moderator)

- **Deployment:** GitHub Action
- **Default mode:** Applies moderation output unless dry-run is enabled
- **Maximum automation impact:** MEDIUM — label, minimize comment
- **Data boundaries:** GitHub API, GitHub Models
- **Access:** GitHub token plus models read and write access needed for configured moderation actions
- **Important limitation:** Repository content is sent to a model endpoint and model judgments can be wrong. Its built-in AI-authorship prompt is not proof of authorship; disable it for enforcement. GitHub Models paid usage may apply after free limits.
- **Repository snapshot:** archived=`false`, last source push=`2026-06-02T05:54:42Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github/ai-moderator#usage) · [source 2](https://github.com/github/ai-moderator#inputs)

### [AI Community Moderator](https://github.com/benbalter/ai-community-moderator)

- **Deployment:** GitHub Action
- **Default mode:** Model-driven moderation using project guidelines
- **Maximum automation impact:** HIGH — comment, hide content, lock discussion, limit interactions
- **Data boundaries:** GitHub API, GitHub Models
- **Access:** GitHub token, models read, and write permissions for enabled actions
- **Important limitation:** A language model interprets community standards; ambiguous or multilingual content needs human review and an appeal path.
- **Repository snapshot:** archived=`false`, last source push=`2025-11-20T02:13:17Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/benbalter/ai-community-moderator#features) · [source 2](https://github.com/benbalter/ai-community-moderator#permissions)

### [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler)

- **Deployment:** GitHub Action
- **Default mode:** Posts a structured assessment and applies configured labels
- **Maximum automation impact:** MEDIUM — comment, label
- **Data boundaries:** GitHub API, GitHub Models or a compatible endpoint
- **Access:** GitHub token, models read, issues write, and contents read for prompt files
- **Important limitation:** The assessment is model-generated, not factual proof. Prompt changes and model changes can alter classification behavior.
- **Repository snapshot:** archived=`false`, last source push=`2025-10-16T13:20:30Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github/ai-assessment-comment-labeler#overview) · [source 2](https://github.com/github/ai-assessment-comment-labeler#required-permissions)

## Contributor Trust & Admission

### [Fossier](https://github.com/PThorpe92/fossier)

- **Deployment:** GitHub Action and CLI
- **Default mode:** Allows, reviews, or denies based on trust tier and a multi-signal score
- **Maximum automation impact:** HIGH — label, comment, close PR
- **Data boundaries:** GitHub API, optional Fossier registry
- **Access:** GitHub token with pull-request write access; optional registry API key
- **Important limitation:** History-based scoring and optional AI co-author rejection can exclude legitimate contributors. Low-confidence cases are forced to review, but maintainers should still test thresholds.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-06T16:53:54Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/PThorpe92/fossier#how-it-works) · [source 2](https://github.com/PThorpe92/fossier#github-action)

### [Vouch](https://github.com/mitchellh/vouch)

- **Deployment:** GitHub Actions and a repository trust file
- **Default mode:** Explicit admission based on project-defined vouches and denouncements
- **Maximum automation impact:** HIGH — fail check, close issue, lock issue, close PR
- **Data boundaries:** GitHub API, repository trust file
- **Access:** Depends on action; write permission is required for close or lock behavior
- **Important limitation:** Explicit trust can protect attention but can also create a closed or biased contributor network. Define transparent nomination and appeal rules.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-12T20:29:38Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/mitchellh/vouch#who-is-vouched) · [source 2](https://github.com/mitchellh/vouch#github-actions)

### [Good Egg](https://github.com/2ndSetAI/good-egg)

- **Deployment:** GitHub Action, CLI, Python package, and MCP server
- **Default mode:** Posts a trust-score comment; fail-on-low is false by default
- **Maximum automation impact:** MEDIUM — comment, create check, fail check
- **Data boundaries:** GitHub API, Python package registry during Action installation
- **Access:** GitHub token; pull-request write for comments and optional checks write
- **Important limitation:** Past merge history is an imperfect proxy for trust and can disadvantage new or private contributors. The Action installs a version-ranged package from PyPI at runtime.
- **Repository snapshot:** archived=`false`, last source push=`2026-04-12T17:55:02Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/2ndSetAI/good-egg#github-action) · [source 2](https://github.com/2ndSetAI/good-egg#scoring-models)

## Intake & Triage

### [Labeler](https://github.com/actions/labeler)

- **Deployment:** GitHub Action
- **Default mode:** Adds or removes labels according to repository configuration
- **Maximum automation impact:** MEDIUM — add label, remove label
- **Data boundaries:** GitHub API
- **Access:** Contents read and pull requests write
- **Important limitation:** Using pull_request_target is dangerous if the same workflow checks out or executes untrusted PR code. Labeling rules can misroute contributions.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-12T04:12:15Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/labeler#recommended-permissions) · [source 2](https://github.com/actions/labeler#notes-regarding-pull_request_target-event)

### [Stale](https://github.com/actions/stale)

- **Deployment:** GitHub Action
- **Default mode:** Marks inactivity and closes after the configured grace period
- **Maximum automation impact:** HIGH — label, comment, close issue, close PR, delete branch
- **Data boundaries:** GitHub API
- **Access:** Issues and pull requests write; contents write only when deleting branches
- **Important limitation:** Inactivity does not mean low value. Exempt security, roadmap, accessibility, and confirmed-bug labels before enabling closure.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-12T04:10:47Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/stale#recommended-permissions) · [source 2](https://github.com/actions/stale#all-options)

### [Lock Threads](https://github.com/dessant/lock-threads)

- **Deployment:** GitHub Action
- **Default mode:** Locks closed threads after configured inactivity
- **Maximum automation impact:** HIGH — lock issue, lock PR, lock discussion
- **Data boundaries:** GitHub API
- **Access:** Write permission for each enabled issue, pull-request, or discussion scope
- **Important limitation:** Locking prevents late corrections and support follow-up. Exclusions and a clear path to open a new issue are important.
- **Repository snapshot:** archived=`false`, last source push=`2026-06-26T18:23:49Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/dessant/lock-threads#usage)

### [Repo Lockdown](https://github.com/dessant/repo-lockdown)

- **Deployment:** GitHub Action
- **Default mode:** Immediately closes and locks configured new issues or pull requests
- **Maximum automation impact:** HIGH — label, comment, close, lock
- **Data boundaries:** GitHub API
- **Access:** Issues and/or pull requests write
- **Important limitation:** This is a blunt emergency control intended for repositories that do not accept submissions or for temporary incidents, not routine triage.
- **Repository snapshot:** archived=`false`, last source push=`2026-06-26T18:23:39Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/dessant/repo-lockdown#usage)

### [Issue Metrics](https://github.com/github-community-projects/issue-metrics)

- **Deployment:** GitHub Action or containerized tool
- **Default mode:** Reads repository activity and writes a Markdown report file
- **Maximum automation impact:** MEDIUM — write report file in the workflow workspace
- **Data boundaries:** GitHub API, workflow workspace
- **Access:** Issues, pull requests, or discussions read according to the search query; publishing requires a separate step and permission
- **Important limitation:** Response-time metrics do not measure answer quality or maintainer wellbeing. The official example uses a separate Action to publish the generated file as an issue; this tool does not publish it by itself.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-09T18:00:50Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/github-community-projects/issue-metrics#available-metrics) · [source 2](https://github.com/github-community-projects/issue-metrics#usage)

## Repository Governance & Access

### [OpenSSF Allstar](https://github.com/ossf/allstar)

- **Deployment:** OpenSSF-operated or self-hosted GitHub App
- **Default mode:** Reports policy violations as issues in the quick start
- **Maximum automation impact:** HIGH — create issue, create check, block noncompliant changes
- **Data boundaries:** GitHub API, OpenSSF-operated service when using the public app
- **Access:** Read access to most repository settings and contents; issues and checks write for reporting and block mode
- **Important limitation:** Organization-wide policy mistakes can affect many repositories. Start with opt-in scope and issue reporting before block enforcement.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-13T13:34:11Z`, GitHub license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/allstar#using-the-public-allstar-app) · [source 2](https://github.com/ossf/allstar#configuration-definitions)

### [Safe Settings](https://github.com/github-community-projects/safe-settings)

- **Deployment:** GitHub App
- **Default mode:** Applies default-branch settings; pull-request changes are evaluated in dry-run
- **Maximum automation impact:** HIGH — change repository settings, change branch protection, change teams, rename repository
- **Data boundaries:** GitHub API, central admin repository
- **Access:** Broad organization and repository administration permissions
- **Important limitation:** Configuration errors have organization-wide blast radius. Restrict managed repositories, protect the admin repository, and require review for settings changes.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-10T15:30:03Z`, GitHub license detection=`ISC`
- **Evidence:** [source 1](https://github.com/github-community-projects/safe-settings#how-it-works) · [source 2](https://github.com/github-community-projects/safe-settings#restrict-repositories)

### [Repository Settings App](https://github.com/repository-settings/app)

- **Deployment:** GitHub App
- **Default mode:** Synchronizes settings from `.github/settings.yml`
- **Maximum automation impact:** HIGH — change repository settings, change permissions, change branch protection
- **Data boundaries:** GitHub API, repository configuration file
- **Access:** Repository administration permissions
- **Important limitation:** Anyone able to merge settings changes may gain or alter administrative access. Protect the configuration path with CODEOWNERS and required review.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-14T09:00:37Z`, GitHub license detection=`ISC`
- **Evidence:** [source 1](https://github.com/repository-settings/app#repository-settings-app) · [source 2](https://github.com/repository-settings/app#security-implications)

## Workflow & Supply-Chain Defense

### [Harden-Runner](https://github.com/step-security/harden-runner)

- **Deployment:** GitHub Action plus StepSecurity service; self-hosted runner support depends on tier
- **Default mode:** Audit network, file, and process activity
- **Maximum automation impact:** HIGH — observe workflow runtime, block network egress
- **Data boundaries:** runner telemetry, StepSecurity service
- **Access:** Runs first in a CI job and observes process, file, and network activity
- **Important limitation:** The community and enterprise tiers differ, and monitoring data is presented through an external service. Review data handling and supported runner type before adoption.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-07T09:27:49Z`, GitHub license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/step-security/harden-runner#community-free) · [source 2](https://github.com/step-security/harden-runner#how-it-works)

### [OpenSSF Scorecard](https://github.com/ossf/scorecard)

- **Deployment:** CLI, GitHub Action, REST API, and public dataset
- **Default mode:** Read-only heuristic assessment
- **Maximum automation impact:** LOW — produce score, produce SARIF when configured
- **Data boundaries:** GitHub API, optional Scorecard API and public dataset
- **Access:** Repository metadata read; additional permissions when uploading SARIF
- **Important limitation:** Scorecard documents that checks are heuristics with false positives and negatives. Weekly public results omit some checks and can be stale.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-13T08:23:11Z`, GitHub license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/scorecard#scorecard-checks) · [source 2](https://github.com/ossf/scorecard#public-data)

### [zizmor](https://github.com/zizmorcore/zizmor)

- **Deployment:** Local CLI, package, or CI check
- **Default mode:** Read-only static analysis
- **Maximum automation impact:** LOW — report findings, fail check when configured
- **Data boundaries:** local files, optional GitHub API for online audits
- **Access:** Read access to workflow files; optional GitHub token
- **Important limitation:** Static analysis cannot prove a workflow is safe and may miss runtime or third-party Action behavior. Review findings in context.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-14T08:41:24Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/zizmorcore/zizmor) · [source 2](https://docs.zizmor.sh/audits/)

### [pinact](https://github.com/suzuki-shunsuke/pinact)

- **Deployment:** Local CLI or CI check
- **Default mode:** Modifies files when pinning; supports a non-modifying verification mode
- **Maximum automation impact:** MEDIUM — rewrite Action references, fail verification
- **Data boundaries:** local files, GitHub API unless offline mode is used
- **Access:** Filesystem write for fixes; optional GitHub token for release and tag lookup
- **Important limitation:** A pinned SHA limits tag movement but does not make third-party code trustworthy. Offline mode only checks SHA syntax.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-14T02:46:48Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/suzuki-shunsuke/pinact#offline-check---no-api) · [source 2](https://github.com/suzuki-shunsuke/pinact#update-actions--update)

### [Dependency Review Action](https://github.com/actions/dependency-review-action)

- **Deployment:** GitHub Action
- **Default mode:** Fails when configured vulnerability or license criteria are violated
- **Maximum automation impact:** MEDIUM — fail check, comment summary when configured
- **Data boundaries:** GitHub Dependency Graph API
- **Access:** Contents read and pull requests read; optional pull requests write for comments
- **Important limitation:** Supported for public repositories and private repositories with GitHub Advanced Security. Results depend on dependency graph coverage and advisory data.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-09T01:43:34Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/actions/dependency-review-action#dependency-review-action) · [source 2](https://github.com/actions/dependency-review-action#configuration-options)

### [TruffleHog](https://github.com/trufflesecurity/trufflehog)

- **Deployment:** CLI, container, and CI integrations
- **Default mode:** Scans and can verify discovered credentials
- **Maximum automation impact:** LOW — report secret, make credential-verification requests
- **Data boundaries:** scanned source, credential providers during verification
- **Access:** Read access to scan targets; network access for verification
- **Important limitation:** Verification can send authentication requests to third-party services. Redact output, scope scans carefully, and treat findings as sensitive incident data.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-14T12:39:26Z`, GitHub license detection=`AGPL-3.0`
- **Evidence:** [source 1](https://github.com/trufflesecurity/trufflehog#what-is-secret-verification) · [source 2](https://github.com/trufflesecurity/trufflehog#usage)

### [PRevent](https://github.com/apiiro/PRevent)

- **Deployment:** Self-hosted GitHub App
- **Default mode:** Scans configured languages for suspicious patterns and can gate merge
- **Maximum automation impact:** HIGH — report finding, block merge pending review
- **Data boundaries:** GitHub API, self-hosted scanner, configured secret manager
- **Access:** GitHub App private key, webhook secret, repository contents, and checks or status permissions
- **Important limitation:** Rules focus on dynamic execution and obfuscation in supported languages; passing does not prove a contribution is benign. Deployment requires operating a privileged GitHub App.
- **Repository snapshot:** archived=`false`, last source push=`2026-01-08T08:10:14Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/apiiro/PRevent#how-it-works) · [source 2](https://github.com/apiiro/PRevent#supported-languages)

### [OSV-Scanner](https://github.com/google/osv-scanner)

- **Deployment:** CLI, container, and CI integrations
- **Default mode:** Read-only vulnerability and license scan
- **Maximum automation impact:** MEDIUM — fail check, modify dependency files in guided remediation
- **Data boundaries:** OSV API and deps.dev, offline database option
- **Access:** Read access to dependency artifacts; filesystem and package-manager access for fix mode
- **Important limitation:** Coverage varies by ecosystem. Guided remediation can execute package-manager behavior from untrusted projects; do not run fix mode on untrusted code.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-14T04:42:24Z`, GitHub license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/google/osv-scanner#offline-mode) · [source 2](https://github.com/google/osv-scanner#guided-remediation)

### [Gitleaks](https://github.com/gitleaks/gitleaks)

- **Deployment:** CLI, pre-commit hook, and CI integrations
- **Default mode:** Read-only pattern-based secret detection
- **Maximum automation impact:** LOW — report finding, fail check
- **Data boundaries:** local scan target
- **Access:** Read access to files or Git history
- **Important limitation:** Pattern detection has false positives and false negatives. Keep output redacted and rotate any real credential rather than merely deleting it from the latest commit.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-08T04:13:10Z`, GitHub license detection=`MIT`
- **Evidence:** [source 1](https://github.com/gitleaks/gitleaks#readme) · [source 2](https://github.com/gitleaks/gitleaks#commands)

## Policies & Playbooks

### [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies)

- **Deployment:** Reference catalog
- **Default mode:** Documentation only
- **Maximum automation impact:** LOW — none
- **Data boundaries:** none
- **Access:** None
- **Important limitation:** Policies differ by project and can change after collection. Confirm each linked source and seek legal advice for copyright, labor, or privacy questions.
- **Repository snapshot:** archived=`false`, last source push=`2026-07-09T17:58:53Z`, GitHub license detection=`CC0-1.0`
- **Evidence:** [source 1](https://github.com/melissawm/open-source-ai-contribution-policies)

### [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)

- **Deployment:** Open working-group issue
- **Default mode:** Discussion and planned deliverables only
- **Maximum automation impact:** LOW — none
- **Data boundaries:** public GitHub discussion
- **Access:** None
- **Important limitation:** This is an open work item, not a finished best-practices document, standard, or OpenSSF certification.
- **Repository snapshot:** archived=`false`, last source push=`2026-02-04T16:32:52Z`, GitHub license detection=`Apache-2.0`
- **Evidence:** [source 1](https://github.com/ossf/wg-vulnerability-disclosures/issues/178)
