# Repository auditor

> Product reference for commands, rule families, output contracts, fixes, and offline limits. Return to the [documentation hub](README.md).

The dependency-free repository auditor checks local GitHub governance, workflow trust boundaries, and moderation automation. It is designed to complement—not replace—specialized GitHub Actions analyzers such as zizmor.

Its contract is: **find risky GitHub settings and automated jobs without changing your repository**. The default human output leads with severity counts and then shows the source evidence, risk, safe remediation, and stable rule link for every finding.

## Commands

From a source checkout:

```bash
python3 scripts/install_kit.py audit .
python3 scripts/install_kit.py audit . --format summary
python3 scripts/install_kit.py audit . --format json
python3 scripts/install_kit.py audit . --format sarif > maintainer-defense.sarif
python3 scripts/install_kit.py audit . --fail-on high
python3 scripts/install_kit.py fix . --output recommended.patch
python3 scripts/install_kit.py fix . --safe-only
```

The standalone artifact accepts the same `audit` and `fix` subcommands. The original installer interface remains supported, both with legacy flags and through `install`:

```bash
python3 maintainer-defense.py --target . --profile observe
python3 maintainer-defense.py install --target . --profile observe
```

The v1.1 release provides the verified standalone artifact, a wheel for `pipx`, and a Homebrew formula. Distribution commands and checksums are documented in the repository README.

`fix` never edits the target, changes GitHub settings, commits, pushes, or opens a pull request. It emits a unified diff for human review. `--dry-run` is accepted for clarity but is redundant because patch-only behavior is unconditional.

## Rule families

| Family | Scope |
| --- | --- |
| `MD-GOV` | SECURITY, CODEOWNERS, issue forms, dependency updates, and documented branch-protection expectations |
| `MD-WF` | Token boundaries, immutable Action pins, privileged events, untrusted checkout/execution, secrets, and persisted credentials |
| `MD-MOD` | Destructive moderation, identity/history proxies, and appeal paths |

Every finding includes a stable rule ID, source location, severity, confidence, threat scenario, recommendation, stable fingerprint, and patch metadata. The [rule reference](AUDITOR_RULES.md) adds detection evidence, false-positive guidance, safe remediation, and OpenSSF/CWE mappings where the mapping is useful. JSON output follows [`auditor.schema.json`](../auditor.schema.json). SARIF output follows SARIF 2.1.0 and links each result to its rule documentation.

## GitHub Action and Security tab

The copyable [`auditor-sarif.yml`](examples/auditor-sarif.yml) workflow scans on `push`, a weekly schedule, or manual dispatch and uploads SARIF to GitHub code scanning. The auditor itself is read-only: it neither executes repository code nor changes repository contents or settings. The upload step does require `security-events: write`; that permission writes analysis results to the Security tab, not source code. Code scanning is available for public repositories on GitHub.com and for eligible private or internal repositories with GitHub Code Security enabled. Review both prerequisites and the upload boundary before adoption.

## Offline boundary

The auditor does not make network or GitHub API calls. It cannot prove the actual state of rulesets, branch protections, default token settings, labels, private vulnerability reporting, or organization policy. It checks only repository files and reports undocumented expectations separately. Do not interpret a clean local audit as a certification.

## Evidence and testing

The labeled corpus in [`tests/fixtures/auditor/corpus.json`](../tests/fixtures/auditor/corpus.json) covers safe and unsafe governance, workflow, and moderation configurations. Tests also mutate token permissions, Action pins, and checkout credential persistence, then require the corresponding rule to detect each mutation.

Corpus accuracy is a regression measurement over the published cases, not a claim about all GitHub repositories. New rules should add positive, negative, and non-applicable examples before their behavior is advertised.

Published per-rule precision, recall, exact-case agreement, mutation score, and their interpretation boundary are in [`AUDITOR_EVALUATION.md`](AUDITOR_EVALUATION.md).

The first public-repository smoke test, pinned source revisions, corrections it produced, and why it does not claim real-world precision are documented in [`AUDITOR_PILOT.md`](AUDITOR_PILOT.md).

Independent OSS maintainers can join the consent-based next phase through the [`AUDITOR_PILOT_PROGRAM.md`](AUDITOR_PILOT_PROGRAM.md) protocol.
