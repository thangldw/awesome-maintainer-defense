# Synthetic auditor evaluation

> Generated from `tests/fixtures/auditor/corpus.json`. Edit fixtures and implementation, not this page.

## Measured contract

The corpus contains **57** small labeled fixtures designed to exercise known rule behavior.

- Exact fixture agreement: **57/57**
- Micro precision inside this corpus: **1.000**
- Micro recall inside this corpus: **1.000**

| Rule | TP | FP | FN | Corpus precision | Corpus recall |
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
| `MD-WF-005` | 5 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-006` | 3 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-007` | 1 | 0 | 0 | 1.000 | 1.000 |
| `MD-WF-008` | 1 | 0 | 0 | 1.000 | 1.000 |

## Failure-injection check

The suite injects four unsafe changes: remove the workflow permission boundary, add `write-all`, replace a full Action SHA with a tag, and persist credentials in a write-capable checkout. The expected result is **4/4 detected**.

## Interpretation boundary

These numbers are regression measurements for intentionally constructed fixtures. They are not prevalence-weighted field accuracy and do not measure arbitrary YAML semantics, live GitHub settings, maintainer time saved, contributor impact, or novel attack paths. Field claims require authorized, independently labeled repository pilots with explicit applicability decisions and adequate negative samples.

Regenerate with `python3 scripts/evaluate_auditor.py`.
