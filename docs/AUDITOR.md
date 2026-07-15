# Repository auditor

The dependency-free repository auditor checks local GitHub governance, workflow trust boundaries, and moderation automation. It is designed to complement—not replace—specialized GitHub Actions analyzers such as zizmor.

## Commands

From a source checkout:

```bash
python3 scripts/install_kit.py audit .
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

`fix` never edits the target, changes GitHub settings, commits, pushes, or opens a pull request. It emits a unified diff for human review. `--dry-run` is accepted for clarity but is redundant because patch-only behavior is unconditional.

## Rule families

| Family | Scope |
| --- | --- |
| `MD-GOV` | SECURITY, CODEOWNERS, issue forms, dependency updates, and documented branch-protection expectations |
| `MD-WF` | Token boundaries, immutable Action pins, privileged events, untrusted checkout/execution, secrets, and persisted credentials |
| `MD-MOD` | Destructive moderation, identity/history proxies, and appeal paths |

Every finding includes a source location, severity, confidence, threat scenario, recommendation, stable fingerprint, and patch metadata. JSON output follows [`auditor.schema.json`](../auditor.schema.json). SARIF output follows SARIF 2.1.0 and can be uploaded by a separately reviewed GitHub Code Scanning workflow.

## Offline boundary

The auditor does not make network or GitHub API calls. It cannot prove the actual state of rulesets, branch protections, default token settings, labels, private vulnerability reporting, or organization policy. It checks only repository files and reports undocumented expectations separately. Do not interpret a clean local audit as a certification.

## Evidence and testing

The labeled corpus in [`tests/fixtures/auditor/corpus.json`](../tests/fixtures/auditor/corpus.json) covers safe and unsafe governance, workflow, and moderation configurations. Tests also mutate token permissions, Action pins, and checkout credential persistence, then require the corresponding rule to detect each mutation.

Corpus accuracy is a regression measurement over the published cases, not a claim about all GitHub repositories. New rules should add positive, negative, and non-applicable examples before their behavior is advertised.

Published per-rule precision, recall, exact-case agreement, mutation score, and their interpretation boundary are in [`AUDITOR_EVALUATION.md`](AUDITOR_EVALUATION.md).

The first public-repository smoke test, pinned source revisions, corrections it produced, and why it does not claim real-world precision are documented in [`AUDITOR_PILOT.md`](AUDITOR_PILOT.md).
