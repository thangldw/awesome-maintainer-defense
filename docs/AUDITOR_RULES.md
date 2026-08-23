# Auditor rules

This page is the human review layer for `auditor-rules.json`. Rule IDs and anchors are stable. Evidence identifies a local pattern; reviewers must confirm applicability and external controls before changing a repository.

## Governance

### MD-GOV-001

**Repository security policy is missing · medium**

The checkout has no supported `SECURITY.md`. Confirm that a private route is not documented elsewhere, then add supported versions, response expectations, and a private disclosure path. Mapping: [OpenSSF Security-Policy](https://github.com/ossf/scorecard/blob/main/docs/checks.md#security-policy).

### MD-GOV-002

**CODEOWNERS boundary is missing · medium**

No CODEOWNERS file establishes review ownership for the repository control plane. Name real, eligible owners for workflows, issue templates, security policy, and CODEOWNERS itself; enforce review separately. Mappings: [OpenSSF Code-Review](https://github.com/ossf/scorecard/blob/main/docs/checks.md#code-review) and [Branch-Protection](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection).

### MD-GOV-003

**CODEOWNERS does not explicitly cover .github · medium**

Ownership exists but does not explicitly protect `.github`. Add a specific `/.github/` rule with active owners and verify the intended ruleset outside the checkout. Mapping: [OpenSSF Code-Review](https://github.com/ossf/scorecard/blob/main/docs/checks.md#code-review).

### MD-GOV-004

**Structured issue form is missing · low**

No YAML issue form requires reproducible evidence. Add a non-destructive form for versions, steps, expected behavior, and actual behavior; keep vulnerability intake private. No direct framework mapping is claimed.

### MD-GOV-005

**Machine-readable dependency update policy is missing · low**

The checkout contains neither supported Dependabot nor Renovate configuration. Configure the ecosystems actually used and retain human review for updates. Mapping: [OpenSSF Dependency-Update-Tool](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dependency-update-tool).

### MD-GOV-006

**Branch-protection expectations are not documented locally · note**

Local documentation does not state intended reviews, checks, bypass owners, force-push handling, and emergency procedure. Document the expectation, then compare it with live repository settings using separately authorized read-only access. Mapping: [OpenSSF Branch-Protection](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection).

## Workflows

### MD-WF-001

**Workflow has no top-level token boundary · medium**

A workflow omits a top-level `permissions` boundary, so a future job may inherit repository defaults. Set `permissions: {}` and grant only the scopes each job needs. Mappings: [OpenSSF Token-Permissions](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions) and [CWE-269](https://cwe.mitre.org/data/definitions/269.html).

### MD-WF-002

**Workflow grants write-all token permissions · high**

The workflow requests `write-all`, creating authority unrelated to most jobs. Replace it with an empty workflow default and explicit job-level grants. Mappings: [OpenSSF Token-Permissions](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions) and [CWE-269](https://cwe.mitre.org/data/definitions/269.html).

### MD-WF-003

**GitHub Action is not pinned to a full commit SHA · medium**

An Action reference uses a mutable tag or branch. Resolve the reviewed release to a full commit SHA, keep the human-readable tag in a comment, verify provenance, and automate reviewed pin updates. Mappings: [OpenSSF Pinned-Dependencies](https://github.com/ossf/scorecard/blob/main/docs/checks.md#pinned-dependencies) and [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

### MD-WF-004

**Privileged event checks out attacker-influenced code · high**

A privileged event can fetch a pull-request-controlled revision. Separate privileged metadata handling from contributor-code execution; run untrusted code only under a read-only `pull_request` path without secrets. Mappings: [OpenSSF Dangerous-Workflow](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow) and [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

### MD-WF-005

**Untrusted input can reach secrets or write authority · critical**

Attacker-controlled event data appears in a job with secrets, OIDC, or repository write authority. Trace the value to its sink, remove privilege from the untrusted path, and pass only validated data into a separate privileged stage. Mappings: [OpenSSF Dangerous-Workflow](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow) and [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

### MD-WF-006

**Checkout may persist a write-capable token · medium**

`actions/checkout` may persist credentials in a write-capable job. Set `persist-credentials: false` unless authenticated Git is required; isolate any required push in a narrow trusted job. Mapping: [OpenSSF Token-Permissions](https://github.com/ossf/scorecard/blob/main/docs/checks.md#token-permissions).

### MD-WF-007

**Untrusted event data is interpolated into a shell command · high**

An attacker-influenced expression is embedded directly in `run`. Move the expression to an environment variable or reviewed action input, then quote it for the selected shell. Mapping: [CWE-78](https://cwe.mitre.org/data/definitions/78.html).

### MD-WF-008

**Privileged workflow executes a pull-request artifact · critical**

A privileged `workflow_run` consumer executes an artifact produced by pull-request code. Treat the artifact as untrusted data: verify and parse it without execution, or rebuild from trusted source. Mappings: [OpenSSF Dangerous-Workflow](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow) and [CWE-829](https://cwe.mitre.org/data/definitions/829.html).

## Moderation

### MD-MOD-001

**Destructive moderation is enabled · high**

Recognized automation can close, lock, or delete contributor work. Use report-only mode first, require human review, measure false positives, and define appeal and rollback before enforcement. No direct framework mapping is claimed.

### MD-MOD-002

**Identity or history proxy is used for contributor risk · medium**

Automation uses identity, account age, profile, fork, or contribution-history characteristics as a risk proxy. Disable it and assess the submitted work through reproducibility, scope, tests, policy compliance, and responsiveness. No direct framework mapping is claimed.

### MD-MOD-003

**Destructive moderation has no discoverable appeal path · medium**

Destructive automation is present but the checkout contains no discoverable reconsideration route. Document a human owner, channel, response expectation, reopening process, and emergency disable path. No direct framework mapping is claimed.

Report a minimal, sanitized false-positive case through the [auditor false-positive form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-false-positive.yml).
