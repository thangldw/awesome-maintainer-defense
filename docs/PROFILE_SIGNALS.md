# PR quality profile contract

This document is the reviewable contract for the PR-quality workflows shipped in the Maintainer Defense Kit. The workflow files configure every active check explicitly so an upstream default cannot silently change the baseline.

## Active checks

The pinned [`peakoss/anti-slop`](https://github.com/peakoss/anti-slop/tree/57858eead489d08b255fab2af45a506c2ca6eab2) Action evaluates these six submission properties. A PR is flagged only when at least four fail.

| Check | Shipped value | Why it is used |
| --- | --- | --- |
| Changed files | At most 50 | Very broad changes are harder to review safely; splitting is normally reversible. |
| Changed lines | At most 10,000 | Bounds review scope without inferring who authored the contribution. |
| Maintainers may edit | Required | Allows a maintainer to help repair the PR branch when GitHub supports it. |
| PR description | Required | Requires a minimum reproducibility and intent record. |
| Commit-message length | At most 500 characters | Bounds unusually large commit messages while leaving normal explanations intact. |
| Final newline | Required | Checks basic repository hygiene. |

The repository validator locks all six values and the four-failure threshold.

## Profile effects

- `observe` writes results only to the workflow job summary. It never fails a check or changes a pull request; on public repositories, workflow summaries and logs are publicly visible.
- `balanced` evaluates the same signals and fails the named `PR quality gate` check when the threshold is reached. It does not comment, label, close, lock, merge, or check out contributor code.
- `hardened` adds pinned dependency-review and workflow static-analysis jobs to `balanced`; its PR-quality behavior is otherwise identical.

A failing `balanced` or `hardened` check blocks merging only if a repository owner separately makes that check required in a native GitHub ruleset.

## Explicitly disabled inputs

The baseline does not use source-branch names, usernames, account age, fork rate, public-profile state, profile completeness, repository or global merge history, commit-author identity, description length, emoji count, code-reference count, changed-path deny lists, or added-comment count as quality evidence. The optional label bypass is also disabled.

Draft pull requests remain exempt so contributors can iterate before requesting review. The workflow explicitly exempts `OWNER`, `MEMBER`, and `COLLABORATOR` associations plus `actions-user`, `autofix-ci[bot]`, `dependabot[bot]`, `renovate[bot]`, and `github-actions[bot]`. No user, label, or milestone exemption is enabled. Review this list before treating the result as a security boundary.

## Tuning and evidence

Start with `observe`. Record the observation period, totals, false positives, appeals, and any threshold change in the installed adoption record. Do not lower the failure threshold or make the check required without human review and repository-specific evidence. Sanitized field reports can be submitted through the [field-report issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=field-report.yml).

This is a triage contract, not an AI-authorship detector or a security certification. See the [assurance case](KIT_ASSURANCE.md) for the tested boundary.
