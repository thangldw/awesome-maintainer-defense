---
name: audit-repository-workflows
description: Audit a local repository for governance gaps, GitHub Actions trust-boundary risks, and unsafe moderation automation. Use for repository security reviews, pull-request workflow audits, pull_request_target or workflow_run analysis, token-permission checks, policy coverage, and requests for a reviewable remediation patch.
---

# Audit repository workflows

Use the bundled dependency-free auditor. Lead with evidence and distinguish a finding from proof of authorship, intent, compromise, or exploitability.

## Workflow

1. Resolve the exact repository directory. Do not scan outside the user's stated scope.
2. Read `references/commands.md` and run the read-only audit first.
3. Summarize critical and high findings, the workflow/event path that triggers each finding, and the documented safe remediation.
4. Generate a patch only when the user requests a fix or patch. The `fix` command emits unified diff text and never edits the target repository.
5. Review every proposed patch before recommending application. Call out changes that need repository-owner judgment.

## Guardrails

- Never install a defense profile, edit repository settings, commit, push, merge, close issues, or change permissions without a separate explicit request.
- Do not label a contributor, account, pull request, or commit as malicious based on heuristic findings.
- Treat exit code `2` from `--fail-on` as a policy threshold result, not an auditor crash.
- Keep SARIF or JSON output private when it contains sensitive workflow paths or security details.
- If the target is not a Git repository, explain the reduced provenance context rather than inventing repository identity.

## Output

Return: audit scope, finding counts, prioritized findings, evidence locations, remediation options, limitations, and whether a patch was generated.
