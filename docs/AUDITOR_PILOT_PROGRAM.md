# Auditor pilot program

The pilot program collects maintainer-reviewed evidence without ranking repositories or claiming authorship detection.

## Authority and consent

A repository maintainer or explicitly authorized representative starts a pilot through the [pilot issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-pilot.yml). They identify the public repository, pin a full target commit SHA, state their role, choose a disclosure level, and consent to the selected publication. Silence, a public URL, or an unsolicited audit is not publication consent.

## Procedure

1. Pin the auditor source revision, product version, target revision, and standalone SHA-256.
2. Run the auditor offline without executing target code or changing repository state.
3. Preserve raw and effective schema-v1 reports separately.
4. Have the authorized reviewer label each finding `true_positive`, `false_positive`, `not_applicable`, or `unresolved` and assess whether remediation is safe and practical.
5. Add a regression fixture before publishing any parser or rule correction.
6. Build and validate the reproducible bundle against `pilot.schema.json`.

The [consent-to-evidence diagram](diagrams/consent-to-evidence.html) summarizes this flow: explicit maintainer authority precedes a pinned offline audit; human labels, including unresolved findings, remain in the record; the disclosure choice limits which fields can enter the deterministic publication bundle.

## Publication gate

Publish only the fields allowed by the participant's disclosure choice. Remove credentials, personal data, private issue content, and unnecessary repository material. The bundle must state reviewer authority, whether review is independent, unresolved context, and limitations.

Owner-directed dogfood is labeled non-independent and non-representative. It can demonstrate reproducibility and product workflow, but it cannot establish field precision or external usefulness.

No repository score, leaderboard, contributor profile, or aggregate precision/recall claim is produced until independent labels and adequate positive and negative samples support that analysis.

Reproducible bundles and their required files are described in [Pilot evidence](../pilots/README.md).
