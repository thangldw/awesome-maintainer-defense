# Pilot evidence

Each dated directory is a reproducible evidence bundle built from a pinned auditor commit and target commit. Keep metadata, raw report, effective report, optional independent labels, generated `pilot.json`, and generated `README.md` together.

The builder never infers review labels. Missing labels stay `unresolved`; expired or governed suppressions remain visible through the raw/effective split. Aggregate precision is allowed only for an explicitly authorized, completely independently labeled sample. Recall is not derived from finding-only bundles.

`fixtures/minimal-input.json` is a format example, not field evidence. The initial repository dogfood pilot is owner-directed and must state that it is neither independent nor representative.
