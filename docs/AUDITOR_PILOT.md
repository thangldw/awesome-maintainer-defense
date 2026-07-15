# Public-repository auditor pilot

> Evidence record from public-repository smoke testing. It documents corrections and applicability—not population accuracy. Return to the [documentation hub](README.md).

**Run date:** 2026-07-15.

**Scope:** ten public repositories, shallow-cloned at the exact commits below.

**Purpose:** find parser and applicability failures before promoting the auditor beyond release-candidate status.

This is a smoke test, not a representative benchmark. Repository selection was purposive, the project author performed the review, and the repositories differ in organization-level policy and feature settings that an offline checkout cannot see. Consequently, this document does **not** publish real-world precision or recall.

## Results after corrections

| Repository | Commit | Findings | Rule distribution |
| --- | --- | ---: | --- |
| `actions/checkout` | `62661c4e71a304b2823ed026347b8d34c3eac541` | 34 | GOV-001×1, GOV-003×1, GOV-004×1, GOV-006×1, WF-001×7, WF-003×21, WF-006×2 |
| `astral-sh/ruff` | `bf3f5f6d6ec4f04301376a1dfd9a804aa0887b9b` | 11 | GOV-001×1, GOV-003×1, GOV-005×1, GOV-006×1, WF-001×4, WF-006×3 |
| `cli/cli` | `c14cbaa24a75272958161751240fd538a68e6c04` | 17 | GOV-003×1, GOV-004×1, GOV-006×1, WF-001×6, WF-006×8 |
| `ossf/scorecard` | `64febf8c5229a2a65d09c6b543677b28a51abb09` | 6 | GOV-003×1, GOV-004×1, WF-001×1, WF-003×1, WF-006×2 |
| `pallets/flask` | `36e4a824f340fdee7ed50937ba8e7f6bc7d17f81` | 5 | GOV-001×1, GOV-002×1, GOV-004×1, GOV-005×1, GOV-006×1 |
| `psf/requests` | `f361ead047be5cb873174218582f7d8b9fcd9f49` | 2 | GOV-004×1, GOV-006×1 |
| `pypa/pip` | `b834bb8c1bfa386d4ecca749626ee283f38366fa` | 5 | GOV-002×1, GOV-006×1, WF-001×2, WF-006×1 |
| `pytest-dev/pytest` | `67a174fcee355334c53588be2eeba8df702477e9` | 6 | GOV-002×1, GOV-004×1, GOV-006×1, WF-001×1, WF-006×2 |
| `sindresorhus/ky` | `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f` | 7 | GOV-002×1, GOV-004×1, GOV-005×1, GOV-006×1, WF-001×1, WF-003×2 |
| `zizmorcore/zizmor` | `886da1de13fb0e2655378bef38d0a8eacffbe89e` | 2 | GOV-001×1, GOV-002×1 |

The corrected run produced 95 policy findings: 77 medium, 10 low, eight notes, and no high or critical findings. Counts are deliberately not converted into repository scores or rankings.

## Corrections caused by the pilot

Manual source review identified three concrete implementation failures:

1. Seven full-SHA Action pins in `psf/requests` were quoted YAML scalars. The first parser included the quote in the ref and incorrectly reported all seven as mutable. Quoted pins now have a negative regression fixture.
2. Two `ossf/scorecard` workflows used privileged events but checked out trusted base content. The first rule reported any privileged-event checkout; it now requires an attacker-influenced revision before emitting `MD-WF-004`.
3. The first persisted-credential check combined permissions and checkout options across the entire workflow. Multi-job workflows could therefore borrow write authority or `persist-credentials: false` from unrelated jobs or steps. Evaluation is now job- and step-scoped.

## Applicability boundary

- Missing local SECURITY, CODEOWNERS, or issue-form files may be intentional or inherited from an organization-wide `.github` repository.
- A checkout with write permission may intentionally need authenticated Git operations. `MD-WF-006` asks for explicit review; it does not prove exploitability.
- A missing top-level permissions boundary can coexist with complete job-level permissions. `MD-WF-001` represents a future-job inheritance guard, not a claim that the current jobs are overprivileged.
- Mutable Action tags are a deliberate policy finding even when the repository owner accepts that update model.

An independently labeled, prevalence-aware sample is still required before publishing real-world precision or recall. The synthetic corpus remains the regression contract; this pilot exists to expose where that contract failed to model real repositories.
