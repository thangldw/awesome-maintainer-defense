# Roadmap

> Outcomes we want to prove, not a backlog of features.

| Horizon | Outcome | Evidence that it is complete |
| --- | --- | --- |
| Release gate | A maintainer can install and verify one identical release through familiar channels. | PyPI, GitHub, Homebrew, and the ChatGPT/Codex bundle resolve to `1.1.0` artifacts covered by one checksum manifest. |
| Now | Maintainers can decide whether each finding is useful and correct. | At least five consent-based pilots include independent labels, false-positive review, and remediation feedback. |
| Next | Common safe configurations produce fewer ambiguous findings. | Pilot corrections become regression cases and per-rule field results are published with their applicability limits. |
| Later | Field evidence is independently reproducible across diverse repositories. | Repeated pilot runs preserve pinned source/target revisions, full labels, limitations, and non-invented metrics. |

The project will not add automatic blocking, closing, or repository changes to make the roadmap look larger. Read-only auditing and reviewable patches remain the product boundary.
