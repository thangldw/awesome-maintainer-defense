# Kit assurance

Status: engineering-verified baseline. The kit is not security-certified, and representative field accuracy is not established.

| Claim | Mechanism | Evidence | Limitation |
| --- | --- | --- | --- |
| Offline, read-only audit | Local parser; no network client; no repository-code execution | CLI and corpus tests | Live GitHub settings and external services are invisible |
| Patch-only remediation | `fix` renders a unified diff | Mutation and CLI tests | Patch correctness still depends on repository context |
| Safe install preview | Preview by default; explicit `--apply` | Installer mode tests | A maintainer must approve and review adoption |
| Conflict-safe ownership | Destination preflight, manifest hashes, symlink/path rejection | Installer conflict, verify, and uninstall tests | Manual edits to installed files intentionally block automatic removal |
| Least-privilege shipped workflows | Read-only PR event, explicit permissions, no checkout in triage profiles | Static invariants and workflow analysis | Native required-check settings remain external |
| Immutable Action references | Full commit SHA plus `pins.json` provenance records | Repository validation | Verified commits are not full source audits |
| Deterministic machine output | Schema-v1 JSON and SARIF; stable IDs and fingerprints | Contract and corpus tests | Dynamic workflow semantics may be outside parser coverage |
| Three-language deployment structure | English, Vietnamese, and Japanese assets installed by matrix | Profile × language tests | Native security/legal review is not claimed |
| Reproducible pilot bundle | Pinned source/target commits, artifact digest, raw/effective reports, labels | Pilot schema and provenance verification | Owner-directed dogfood is not independent or representative |

The current [1.1.1 owner-directed pilot](../pilots/2026-08-24-awesome-maintainer-defense/README.md) reproduced a zero-finding self-audit at its pinned release-candidate commit. This verifies artifact and evidence reproducibility only; it adds no independent field-accuracy evidence.

## Acceptance gate

Before production enforcement, a repository owner should:

1. Verify live GitHub rules, permissions, installed Apps, secrets, and private reporting separately.
2. Run the `observe` profile through representative contribution cycles.
3. Record an owner, problem baseline, data boundary, review SLA, appeal path, expiry, and rollback.
4. Sample flagged and unflagged work; test both status failure and recovery.
5. Require human approval for contributor-visible or destructive action.
6. Re-run installation verification, repository CI, and workflow security analysis after every change.

The defensible claim is limited: installation, permissions, reversibility, pinning, schemas, and deterministic regression behavior are tested. Precision, recall, maintainer time saved, contributor drop-off, and cross-project effectiveness remain unproven until independently labeled pilots provide adequate evidence.
