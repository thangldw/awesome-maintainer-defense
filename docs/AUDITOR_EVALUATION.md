# Auditor corpus evaluation

> Evidence record for deterministic rule behavior. Start from the [documentation hub](README.md).

## Result

**Corpus:** 52 labeled synthetic repository fixtures.

**Exact-case agreement:** 52/52.

**Micro precision:** 1.000.

**Micro recall:** 1.000.

| Rule | TP | FP | FN | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| `MD-GOV-001` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-GOV-002` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-GOV-003` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-GOV-004` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-GOV-005` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-GOV-006` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-MOD-001` | 6 | 0 | 0 | 1.000 | 1.000 |
| `MD-MOD-002` | 7 | 0 | 0 | 1.000 | 1.000 |
| `MD-MOD-003` | 4 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-001` | 2 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-002` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-003` | 3 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-004` | 2 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-005` | 4 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-006` | 3 | 0 | 0 | 1.000 | 1.000 |

## Mutation score

The test suite applies four explicit mutations: remove the top-level permission boundary, grant `write-all`, replace a full Action SHA with a tag, and persist a write-capable checkout token. All four mutations are detected: **4/4 (1.000)**.

## Interpretation boundary

These measurements describe only the published synthetic corpus. Cases are small, deterministic, and designed around known rule behavior; they are regression evidence, not an estimate of effectiveness on arbitrary public repositories. They do not measure YAML parser completeness, GitHub settings that are absent from a checkout, prevalence-weighted accuracy, or maintainer outcomes. A real-world benchmark requires independently labeled repositories and applicability review.

Regenerate this document with `python3 scripts/evaluate_auditor.py`.
