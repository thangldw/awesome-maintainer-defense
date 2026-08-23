# Pilot evidence registry

Each dated directory is an immutable, reproducible evidence unit for one pinned auditor revision and one pinned target revision.

Required inputs are `metadata.json`, `raw-report.json`, `effective-report.json`, and `labels.json`. The builder produces canonical `pilot.json` and `README.md`; missing labels remain `unresolved` and are never inferred. Raw and effective reports stay separate so suppressions remain auditable.

Historical pilots are rebuilt with their recorded source code and do not claim equality with the current runtime. A pilot for the current package version must additionally match current runtime paths before release.

Owner-directed dogfood must be labeled non-independent and non-representative. Aggregate precision is permitted only when an external maintainer authorized it and every finding has an independent, non-unresolved label. Finding-only bundles cannot establish recall.

`fixtures/minimal-input.json` demonstrates the schema and is not field evidence. Participation authority, disclosure choices, and publication limits are defined in the [pilot program](../docs/AUDITOR_PILOT_PROGRAM.md).
