# Evaluation method

This project evaluates usefulness and operational risk; it does not certify that a resource is secure, unbiased, or suitable for every repository.

## Inclusion gates

A candidate must pass all of these gates:

1. **Maintainer relevance:** reduces abuse, review load, unsafe intake, governance drift, or contribution-path supply-chain risk.
2. **Public evidence:** has canonical documentation describing deployment and behavior.
3. **Identifiable owner:** names a project or organization responsible for maintenance.
4. **Reviewable terms:** publishes a license for software, or is clearly labeled as a reference/discussion rather than reusable code.
5. **Operational clarity:** required privileges, destructive actions, and external processing can be determined before installation.
6. **No deceptive certainty:** does not rely on an unsupported claim that AI authorship, malicious intent, or contributor trust can be determined perfectly.

## Evidence hierarchy

Evidence is preferred in this order:

1. action manifest, configuration schema, source code, or license file;
2. official project documentation and security policy;
3. official GitHub Marketplace or package-registry listing;
4. maintainer-authored issue or release note;
5. independent material only when it is clearly identified as secondary evidence.

Marketing copy is not sufficient for permission, privacy, or accuracy claims.

## Audit dimensions

Every catalog entry has a matching record in [`audits.json`](../audits.json):

- deployment model;
- default behavior;
- maximum documented automation impact;
- data boundaries;
- required access;
- an important limitation;
- repository activity and detected license snapshot;
- links to official evidence.

Impact is intentionally not converted into a single score. A high-impact tool may be appropriate during an incident, while a low-impact classifier may still create harmful bias when trusted blindly.

## Automation-impact labels

| Label | Meaning |
| --- | --- |
| Low | Read-only analysis or documentation in normal use |
| Medium | Can label, comment, fail checks, publish reports, or modify local files |
| High | Can close, lock, delete, block, limit interactions, or change repository settings |

The label represents maximum documented capability. Actual impact depends on configuration, event trigger, token permissions, and repository rules.

## Reliability checks

Before featuring a resource, reviewers should confirm:

- the canonical URL resolves and the repository is not archived;
- the catalog license matches GitHub detection or a reviewed license file;
- descriptions do not imply capabilities absent from official documentation;
- a dry-run, report-only, or reversible mode is documented when enforcement is possible;
- data sent to GitHub Models, a vendor backend, an identity provider, or a credential-verification endpoint is disclosed;
- restrictions on public/private repositories or paid platform features are stated;
- default behavior is distinguished from optional behavior;
- known bias and false-positive paths are documented.

Audits expire after 180 days. CI enforces complete audit coverage and matching catalog IDs.

Run `make metadata` to compare every repository snapshot with the live GitHub API. Any archive, source-push, or detected-license drift requires a human re-check of the affected resource before updating the snapshot.

## Removal and downgrade criteria

A resource may be removed or lose featured status when it becomes archived, changes ownership without clear continuity, removes its license, hides required data flows, accumulates unresolved security concerns, makes misleading accuracy claims, or no longer solves a maintainer-defense problem.

Temporary link failure is not enough for removal; the weekly checker treats most network and rate-limit errors as warnings and fails only confirmed `404` or `410` responses.

## What this audit cannot prove

- absence of vulnerabilities or malicious code;
- compliance with a specific law or organization policy;
- fairness across languages, identities, and contribution histories;
- future maintenance or service availability;
- that a passing scan makes a pull request safe.

Adopters remain responsible for reading current upstream documentation, reviewing permissions, testing in a non-critical repository, and monitoring false positives.
