# OSS maintainer pilot program

> Consent, review, and publication contract for independently reviewed repository pilots. Return to the [auditor reference](AUDITOR.md).

## Purpose

The synthetic corpus measures deterministic regression behavior, and the first public-repository smoke test exposed parser and applicability failures. The next evidence step is maintainer-reviewed classification: whether each finding is correct, useful, actionable, and appropriately severe in the repository's real operating context.

## Participation contract

1. A maintainer or explicitly authorized representative volunteers a public repository and full commit SHA through the [pilot issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-pilot.yml).
2. The auditor runs offline against that pinned checkout. Repository code is not executed, and no repository files or settings are changed.
3. The maintainer reviews each result as true positive, false positive, not applicable, or unresolved, and records the missing external context separately.
4. No repository score or ranking is produced. Results are published only at the participant's selected disclosure level.
5. Any parser or rule correction receives a minimal regression fixture before a new evaluation is published.

## Minimum evidence

- auditor version and full source revision;
- repository revision and declared external-policy boundary;
- per-rule TP, FP, not-applicable, and unresolved counts;
- whether the recommendation was safe and practical;
- sanitized qualitative feedback on usefulness and maintainer effort;
- reviewer role and explicit publication consent.

Precision and recall will not be aggregated until the sample has independent labels, explicit applicability decisions, and enough positive and negative cases per rule to avoid presenting a misleading rate.

## Reproducible bundle

Capture the pinned metadata, raw schema-v1 report, effective post-suppression report, and optional maintainer labels, then run:

```bash
python3 scripts/build_pilot_bundle.py \
  --metadata metadata.json \
  --raw-report raw-report.json \
  --effective-report effective-report.json \
  --labels labels.json \
  --json-output pilot.json \
  --markdown-output README.md
```

The [`pilot.schema.json`](../pilot.schema.json) contract preserves unresolved labels and raw/effective evidence separately. The [pilot evidence directory](../pilots/README.md) defines the publication layout. Owner-directed dogfood must remain labeled non-independent and non-representative.
