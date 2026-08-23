# Workflow-hardening profile

This profile adds dependency review and GitHub Actions static analysis to the balanced status gate.

Both workflows use `pull_request`, explicit read-only repository permissions, and full-SHA Action pins recorded in `pins.json`. They inspect the patch and workflow definitions but do not run the repository build, install dependencies, or execute pull-request code.

Before adoption, review upstream source and release notes, confirm product availability for the repository, define vulnerability and license thresholds, and test recovery after an intentional failure. Dependency Review availability depends on repository visibility and GitHub security features; zizmor reports through the job log in this profile.

A passing check covers only the configured analyzers and revision. It does not prove the change or supply chain is safe. Install through the [Maintainer Defense Kit](../maintainer-defense-kit/README.md) so preview, ownership, verification, and rollback are recorded.
