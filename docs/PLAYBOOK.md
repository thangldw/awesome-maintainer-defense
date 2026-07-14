# Maintainer-defense playbook

## Level 0 — Baseline

Use this before there is an incident.

- Publish contribution, AI-assistance, unsolicited-PR, code-of-conduct, and security-report policies.
- Require structured bug evidence: version, environment, minimal reproduction, actual result, expected result.
- Protect `.github/`, release workflows, package manifests, and ownership files with CODEOWNERS and required review. GitHub recommends protecting the CODEOWNERS file itself; see [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
- Use branch rulesets for required reviews, status checks, deletion protection, and force-push protection. See [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- Set explicit `GITHUB_TOKEN` permissions per job and pin third-party Actions to reviewed commit SHAs.
- Enable private vulnerability reporting and document what evidence a security report must contain.
- Decide who can activate incident controls and where the decision is logged.

## Level 1 — Observe

Use when review volume is rising but the queue is still manageable.

- Measure submissions, time to first response, close reasons, reopened items, and reviewer hours.
- Run new moderation or trust tools in dry-run/report-only mode for at least two representative review cycles.
- Sample both flagged and unflagged submissions; otherwise false negatives remain invisible.
- Record false positives by contributor type, language, repository area, and reason.
- Do not call a person malicious or claim AI use based only on a score.

Exit criteria: the team can state what problem exists, its weekly cost, which signals help, and the tolerated false-positive rate.

## Level 2 — Review-first enforcement

Use when measured signals are useful enough to route work.

- Apply a private or neutral label such as `needs-human-review`.
- Keep automatic closing, locking, blocking, and public accusations disabled.
- Exempt maintainers, approved bots, known contributors, security reporters, and time-sensitive release automation only where the exemption is justified.
- Require a human decision for every high-impact action.
- Publish a short appeal path based on new evidence, not debate about authorship.

The [balanced starter kit](../kits/balanced) implements this level for PR quality triage.

## Level 3 — Incident mode

Use for a live flood, coordinated harassment, or credible compromise—not as a permanent default.

1. Assign an incident owner and start a timestamped decision log.
2. Preserve URLs, screenshots, webhook delivery IDs, workflow run IDs, and relevant audit logs. Do not copy secrets into the log.
3. Pause risky automation and releases if integrity is uncertain.
4. Temporarily limit interactions to existing users, contributors, or collaborators. GitHub interaction limits expire after a chosen duration; see [limiting repository interactions](https://docs.github.com/en/communities/moderating-comments-and-conversations/limiting-interactions-in-your-repository).
5. Close or lock only the clearly affected submission classes. Prefer temporary controls with an explicit expiry.
6. Block accounts or report abuse when behavior violates platform rules; do not use technical disagreement alone as grounds for abuse reporting. See [reporting abuse or spam](https://docs.github.com/en/communities/maintaining-your-safety-on-github/reporting-abuse-or-spam).
7. Rotate exposed credentials, invalidate artifacts, and review workflow history when compromise is possible.
8. Communicate a brief status without amplifying harassment or publishing sensitive evidence.

## Level 4 — Recovery

- Remove temporary interaction limits and lockdown workflows on schedule.
- Reopen legitimate items caught by broad controls.
- Notify affected contributors when a false positive caused a visible action.
- Compare reviewer load, missed valid reports, false positives, and time to recovery against the baseline.
- Convert only proven incident controls into long-term policy.
- Write a blameless retrospective that separates attacker behavior, platform limits, configuration mistakes, and maintainer capacity.

## Adoption record

For every automated defense, record:

| Field | Example |
| --- | --- |
| Owner | `@maintainer-team` |
| Problem | `40 unsolicited PRs/week, 6 reviewer-hours` |
| Mode | `dry-run`, `review-first`, or `enforcing` |
| Permissions | `contents: read`, `pull-requests: write` |
| Data boundary | GitHub API, GitHub Models, vendor service, local only |
| High-impact actions | close, lock, block, delete, settings changes |
| False-positive budget | `< 2% of sampled legitimate PRs` |
| Review date | ISO date, no more than 90 days away |
| Rollback | exact workflow/config change that disables enforcement |

Controls without an owner, review date, and rollback path should not remain in enforcement mode.
