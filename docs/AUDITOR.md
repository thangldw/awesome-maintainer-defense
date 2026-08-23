# Auditor CLI

The auditor performs deterministic static inspection of a local checkout. It reads supported governance files, `.github` issue configuration, GitHub Actions YAML, and local Git metadata. It does not contact GitHub, resolve organization policy, inspect live rulesets, or run repository code.

## Command grammar

```text
maintainer-defense audit [TARGET]
  [--format human|summary|json|sarif]
  [--output PATH]
  [--fail-on critical|high|medium|low|note]
  [--baseline REPORT.json | --compare-ref GIT_REF]
  [--config PATH]
  [--new-only]

maintainer-defense fix [TARGET]
  [--output PATH]
  [--safe-only]
  [--dry-run]
```

`TARGET` defaults to the current directory.

## Audit behavior

- `human` is the default and includes evidence and remediation guidance.
- `summary` emits aggregate counts only.
- `json` conforms to `auditor.schema.json` and preserves fingerprints and locations.
- `sarif` emits SARIF 2.1.0 with stable help links to [Auditor rules](AUDITOR_RULES.md).
- `--output` writes atomically to the chosen local path; otherwise output goes to standard output.
- `--fail-on` returns 2 for a matching effective finding, 1 for a usage or input error, and 0 otherwise.

Severity represents the plausible authority or impact of the detected pattern, not exploitability proof.

## New-finding comparison

Exactly one comparison source is required with `--new-only`:

```bash
maintainer-defense audit . --baseline previous.json --new-only --format json
maintainer-defense audit . --compare-ref origin/main --new-only --fail-on high
```

`--baseline` accepts a schema-v1 JSON report. `--compare-ref` archives and audits a local Git revision in a temporary directory; it does not check out the revision or execute it. A finding is new when its 24-character fingerprint is absent from the comparison.

## Suppressions

The auditor discovers only `TARGET/.maintainer-defense.json` by default. `--config PATH` selects another file explicitly. Suppressions are applied before comparison and threshold evaluation. Invalid, duplicate, unknown, or unmatched active selectors fail closed. See [Configuration](CONFIGURATION.md).

## Patch generation

`fix` writes a unified diff to standard output or `--output`. It never changes repository files, Git state, GitHub settings, branches, or pull requests. `--safe-only` omits proposals that require contextual review. `--dry-run` is a compatibility flag; all fixes are patch-only.

## Installer compatibility

The same artifact exposes the defense-kit installer:

```bash
maintainer-defense install --target . --profile observe --language en
maintainer-defense install --target . --profile observe --language en --apply
maintainer-defense install --target . --verify
maintainer-defense install --target . --uninstall
```

Preview is the default. Install, verify, and uninstall behavior is documented by the [deployable kit](../kits/maintainer-defense-kit/README.md).
