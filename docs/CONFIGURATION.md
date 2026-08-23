# Auditor configuration

Suppressions are governed exceptions, not rule disable switches. Store them in `.maintainer-defense.json` at the audited repository root, or select a file with `--config`.

```json
{
  "schema_version": 1,
  "suppressions": [
    {
      "rule_id": "MD-WF-003",
      "path": ".github/workflows/release.yml",
      "reason": "Reviewed migration tracked in issue 42",
      "owner": "@release-maintainers",
      "expires_on": "2026-10-31"
    }
  ]
}
```

## Selectors

Every entry requires `rule_id`, `reason`, `owner`, `expires_on`, and at least one selector:

- `fingerprint`: exactly 24 lowercase hexadecimal characters; narrowest and stable across unrelated line shifts.
- `path`: normalized repository-relative POSIX path with no backslash, absolute prefix, or `..` segment.

When both are present, both must match the same finding. Duplicate combinations are rejected.

## Lifecycle

`expires_on` uses `YYYY-MM-DD`. An expired entry no longer suppresses and produces a warning on standard error. Active entries that match no finding fail the audit because a stale or mistyped exception must not disappear silently. Owners should remove resolved entries or renew them through normal review with current evidence.

## Fail-closed errors

The auditor exits 1 for malformed JSON, unknown or extra fields, unsupported schema versions, unknown rule IDs, empty reasons or owners, invalid dates, invalid paths or fingerprints, duplicate selectors, and unmatched active suppressions.

Suppressed findings are excluded before `--new-only`, summaries, SARIF/JSON output, and `--fail-on` evaluation. The number suppressed and the configuration path are reported on standard error.

The machine-readable contract is [`maintainer-defense-config.schema.json`](../maintainer-defense-config.schema.json).
