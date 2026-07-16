# Auditor rule reference

> Stable IDs, evidence, review guidance, and safe remediation for every repository auditor rule. Return to the [auditor reference](AUDITOR.md).

Rule IDs are part of the auditor's public output contract. An ID is never reassigned to a different condition. Material semantic changes require a new ID; detection refinements and false-positive fixes retain the ID and are recorded in the changelog.

## Severity model

| Severity | Meaning |
| --- | --- |
| `critical` | Untrusted input can plausibly reach secrets or repository-changing authority. Isolate the trust boundary before relying on the workflow. |
| `high` | The configuration creates direct write, destructive, or attacker-influenced execution risk. Review promptly. |
| `medium` | A defense boundary is absent or weak, but exploitation depends on additional context. |
| `low` | The gap primarily increases triage or maintenance risk. |
| `note` | The checkout cannot prove an external setting; verify it separately. |

Mappings below are cross-references, not claims that every finding is a vulnerability. OpenSSF mappings refer to the closest [Scorecard check](https://github.com/ossf/scorecard/blob/main/docs/checks.md); CWE is included only when a software-weakness category is a useful fit.

## Governance rules

### MD-GOV-001

**Missing repository security policy · medium**

- **Evidence:** none of `SECURITY.md`, `.github/SECURITY.md`, or `docs/SECURITY.md` exists.
- **Review before accepting:** an organization-wide policy, private vulnerability reporting setting, or external disclosure page may exist outside the checkout. Confirm that it is discoverable from the repository.
- **Safe remediation:** add a local `SECURITY.md` with supported versions, a private reporting route, response expectations, and a warning not to disclose secrets publicly. This is a documentation-only change.
- **Mapping:** OpenSSF Scorecard [`Security-Policy`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#security-policy). No CWE mapping.

### MD-GOV-002

**Missing CODEOWNERS boundary · medium**

- **Evidence:** no CODEOWNERS file exists in `.github/`, the repository root, or `docs/`.
- **Review before accepting:** small or single-maintainer repositories may not have a second eligible reviewer; rulesets may also assign review outside CODEOWNERS.
- **Safe remediation:** add real owners for workflows, issue templates, security policy, and CODEOWNERS itself, then separately configure rulesets if owner review must be enforced. Do not add placeholder or inactive accounts.
- **Mapping:** related to OpenSSF Scorecard [`Code-Review`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#code-review) and [`Branch-Protection`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection). No CWE mapping.

### MD-GOV-003

**CODEOWNERS does not explicitly cover `.github/` · medium**

- **Evidence:** a CODEOWNERS file exists, but no explicit rule covers `.github/`.
- **Review before accepting:** a broad `*` rule may already assign an owner. The finding asks for an explicit control-plane boundary because broad rules are easier to weaken unintentionally.
- **Safe remediation:** add a specific `/.github/` rule naming the responsible team. Verify that the owner is eligible and that branch rules actually require its review before relying on it.
- **Mapping:** related to OpenSSF Scorecard [`Code-Review`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#code-review). No CWE mapping.

### MD-GOV-004

**Missing structured issue form · low**

- **Evidence:** `.github/ISSUE_TEMPLATE/` has no YAML issue form other than `config.yml`.
- **Review before accepting:** the project may intentionally use Discussions, an external tracker, or free-form issues. Those routes can be valid when their evidence requirements are clear.
- **Safe remediation:** add a non-destructive issue form requesting reproduction steps, expected behavior, and relevant versions; direct vulnerabilities to the private security route. Avoid undeclared labels that silently fail.
- **Mapping:** no direct OpenSSF or CWE mapping.

### MD-GOV-005

**Missing machine-readable dependency update policy · low**

- **Evidence:** no supported Dependabot or Renovate configuration is found in the locations the auditor recognizes.
- **Review before accepting:** another update service or a documented manual cadence may be in use; the offline auditor cannot observe it.
- **Safe remediation:** configure Dependabot or Renovate for the repository's real ecosystems, including `github-actions` when applicable. Start with pull requests and human review rather than automatic merging.
- **Mapping:** OpenSSF Scorecard [`Dependency-Update-Tool`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dependency-update-tool). No CWE mapping.

### MD-GOV-006

**Branch-protection expectations not documented locally · note**

- **Evidence:** no recognized branch-protection or ruleset expectation appears in repository Markdown or supported settings files.
- **Review before accepting:** actual GitHub rulesets, organization policy, and inherited settings are outside an offline checkout and may already be correct.
- **Safe remediation:** document expected reviews, checks, force-push restrictions, bypass owners, and an emergency change process. Verify actual settings separately with read-only API access; documentation alone does not enforce them.
- **Mapping:** OpenSSF Scorecard [`Branch-Protection`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection). No CWE mapping.

## Workflow rules

### MD-WF-001

**Missing top-level token boundary · medium**

- **Evidence:** a workflow has no top-level `permissions` declaration.
- **Review before accepting:** every current job may already declare least privilege. The residual risk is that a future job inherits repository defaults.
- **Safe remediation:** add `permissions: {}` at workflow level, then grant only required permissions per job. The generated patch is review-required because an omitted permission can break CI.
- **Mapping:** OpenSSF Scorecard [`Token-Permissions`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions); [CWE-269](https://cwe.mitre.org/data/definitions/269.html) as a broad privilege-management cross-reference.

### MD-WF-002

**Workflow grants `write-all` · high**

- **Evidence:** a workflow or job explicitly declares `permissions: write-all`.
- **Review before accepting:** no normal workflow needs every available token permission. A release job may need several writes, but they should still be enumerated.
- **Safe remediation:** replace `write-all` with an empty default and explicitly grant the minimum job-level writes. Review and test the resulting patch before adoption.
- **Mapping:** OpenSSF Scorecard [`Token-Permissions`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions); [CWE-269](https://cwe.mitre.org/data/definitions/269.html).

### MD-WF-003

**GitHub Action is not pinned to a full commit SHA · medium**

- **Evidence:** `uses:` references an external Action or reusable workflow by a tag, branch, or other mutable ref instead of 40 hexadecimal characters.
- **Review before accepting:** local actions and Docker references are outside this rule's intended scope. A mutable tag may be an accepted update policy, but it still permits code to change without a workflow diff.
- **Safe remediation:** resolve the reviewed release to its full commit SHA, keep the human-readable tag in a comment, verify upstream provenance, and automate reviewed pin updates. The auditor does not guess a SHA.
- **Mapping:** OpenSSF Scorecard [`Pinned-Dependencies`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#pinned-dependencies); [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

### MD-WF-004

**Privileged event checks out attacker-influenced code · high**

- **Evidence:** `pull_request_target`, `workflow_run`, or `issue_comment` is combined with `actions/checkout` and an attacker-influenced pull-request ref.
- **Review before accepting:** a privileged event that checks out only the trusted base revision should not trigger. Inspect data flow when expressions or helper scripts obscure which revision is fetched.
- **Safe remediation:** separate metadata handling from code execution. Run contributor code only under `pull_request` with read-only permissions, no secrets, and no persisted credentials; never execute a fork head in the privileged job.
- **Mapping:** OpenSSF Scorecard [`Dangerous-Workflow`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow); [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

### MD-WF-005

**Untrusted input reaches secrets or write authority · critical**

- **Evidence:** a privileged-event workflow references attacker-influenced pull-request content while secrets, inherited secrets, or write permissions are present.
- **Review before accepting:** the rule is intentionally conservative and does not prove that every referenced value is executed. Trace the value into commands, reusable workflows, and actions before declaring exploitability.
- **Safe remediation:** remove secrets and writes from the untrusted path, isolate contributor-code execution in a read-only `pull_request` workflow, and pass only validated artifacts or metadata into any later privileged stage.
- **Mapping:** OpenSSF Scorecard [`Dangerous-Workflow`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow); [CWE-829](https://cwe.mitre.org/data/definitions/829.html). A more specific CWE requires source-to-sink validation.

### MD-WF-006

**Checkout may persist a write-capable token · medium**

- **Evidence:** an `actions/checkout` step is in a write-capable permission scope and its own step block does not set `persist-credentials: false`.
- **Review before accepting:** authenticated Git operations may be an intentional, reviewed part of a release job. The finding does not prove that a later step can be influenced by an attacker.
- **Safe remediation:** set `persist-credentials: false` unless authenticated Git is required. If it is required, isolate the push into a narrow job, minimize permissions, and ensure untrusted code cannot run before credential use.
- **Mapping:** related to OpenSSF Scorecard [`Token-Permissions`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions). No CWE is assigned without evidence that credentials are exposed.

## Moderation rules

### MD-MOD-001

**Destructive moderation enabled · high**

- **Evidence:** recognized configuration enables automatic closing, locking, or deletion.
- **Review before accepting:** deliberate incident lockdowns may justify a temporary destructive control when an owner, expiry, rollback, and appeal route are explicit.
- **Safe remediation:** switch to report-only mode, require human review, measure false positives, and publish an appeal path before enabling enforcement. The generated patch disables the recognized destructive option and is marked safe.
- **Mapping:** no direct OpenSSF or CWE mapping; this is an operational safety rule.

### MD-MOD-002

**Identity or history proxy used for contributor risk · medium**

- **Evidence:** recognized automation enables username, account-age, fork-activity, public-profile, profile-completeness, global-history, or commit-author identity heuristics.
- **Review before accepting:** a signal may be useful for rate limiting during a measured abuse incident, but it is not evidence that a contribution is unsafe or low quality.
- **Safe remediation:** disable the proxy and evaluate reproducibility, scope, tests, policy compliance, and contributor responsiveness. The generated patch changes only the recognized option and is marked safe.
- **Mapping:** no direct OpenSSF or CWE mapping; this is a fairness and moderation-safety rule.

### MD-MOD-003

**No discoverable appeal path for destructive moderation · medium**

- **Evidence:** destructive moderation is enabled and repository policy text contains no recognized appeal or reopening language.
- **Review before accepting:** an appeal channel may exist in a website, organization policy, or support system not present in the checkout. Confirm that affected contributors can actually discover it.
- **Safe remediation:** document the appeal channel, human owner, response expectation, reopening process, and emergency disable path before enabling destructive behavior.
- **Mapping:** no direct OpenSSF or CWE mapping; this is an operational recovery rule.

## Reporting a false positive

Include the rule ID, minimal workflow or policy excerpt, expected result, actual result, and why the documented review guidance does not cover the case. Remove secrets and personal data before using the dedicated [auditor false-positive form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-false-positive.yml).
