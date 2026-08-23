# Threat model

## Security objective

Protect maintainer decision capacity, repository integrity, release authority, credentials, private reports, and contributor appeal rights. The product reduces detectable governance and automation risks; it does not establish that a repository or person is trustworthy.

## Inputs and trust boundaries

| Boundary | Untrusted or external input | Protected side |
| --- | --- | --- |
| Public contribution → repository | Pull-request revisions, issue text, comments, links, artifacts | Maintainer queue and repository content |
| Repository → privileged workflow | Event payloads, checked-out refs, generated scripts | `GITHUB_TOKEN`, secrets, OIDC, release authority |
| Workflow → dependency/service | Actions, packages, APIs, hosted models | Source, metadata, credentials, execution environment |
| Classifier → enforcement | Heuristic or probabilistic result | Close, lock, block, label, and public accusation decisions |
| Local checkout → auditor | Governance files, workflow YAML, local Git metadata | Local report and generated patch |

The auditor crosses only the final boundary. It reads files but does not execute repository code, follow links, call remote APIs, or mutate the checkout.

## Attacker capabilities considered

- Submit crafted patches, metadata, comments, issue bodies, and workflow artifacts.
- Influence a fork revision or mutable dependency reference.
- Trigger public workflow events and attempt to reach tokens, secrets, OIDC, caches, or release jobs.
- Flood intake, hide valid work in noise, or exploit destructive moderation and appeal gaps.
- Compromise a contributor, bot, Action, package, or maintainer account.

## Required invariants

- Untrusted contributor code is never executed in a job holding secrets or write authority.
- Workflow permissions default to empty and are granted per job.
- Third-party Actions resolve to reviewed full commit SHAs.
- Cross-workflow artifacts remain untrusted unless verified and parsed without execution or rebuilt from trusted source.
- Generated remediation remains a patch until a human owner reviews and applies it.
- Destructive moderation is not a default and always has an owner, expiry, rollback, and appeal path.
- Identity and history characteristics are not treated as proof of contribution quality or malicious intent.

## Excluded state

A local audit cannot observe live rulesets, branch protection, organization policy, secret values, installed GitHub Apps, repository role eligibility, label existence, private vulnerability settings, external service behavior, or changes after the checkout revision. [MD-GOV-006](AUDITOR_RULES.md#md-gov-006) therefore records local expectations rather than asserting live configuration.

## Residual risk

Static matching may miss dynamically constructed paths, reusable-workflow behavior, custom scripts, and novel source-to-sink flows. It can also flag patterns made safe by external controls. Third-party provenance does not prove dependency safety. Human review, platform settings verification, specialized analyzers, and incident procedures remain necessary.
