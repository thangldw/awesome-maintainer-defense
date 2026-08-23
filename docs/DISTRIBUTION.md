# Distribution

Version `1.1.1` is distributed through one source repository, one PyPI project, GitHub release artifacts, and the existing ChatGPT/Codex plugin listing. A channel is verified only after its public artifact is fetched and checked.

## Release artifacts

- `maintainer-defense-kit.py` and its SHA-256 file.
- Compatibility standalone `maintainer-defense.py` and its SHA-256 file.
- Python wheel and source distribution for `maintainer-defense-kit`.
- Deterministic `awesome-maintainer-defense-openai-skills-v1.1.1.zip`.
- `SHA256SUMS.txt` covering every public release asset.

The tag, package metadata, CLI version, plugin manifests, formula URL/checksum, artifact names, and release title must all resolve to `1.1.1` before tagging.

## Publication controls

The GitHub Actions release workflow runs tests, validation, pinned-pilot verification, package builds, and distribution smoke tests from the pushed version tag. Actions use reviewed full commit SHAs. GitHub publication verifies the tag and supports idempotent asset replacement.

PyPI publication uses the `pypi` environment and OIDC Trusted Publishing; no long-lived PyPI API token is part of the workflow. `skip-existing` permits recovery after a partial run without overwriting immutable package files.

The OpenAI bundle updates the existing listing [`plugins_6a6edab2886c81918be9c9772e4ca904`](https://chatgpt.com/plugins/plugins_6a6edab2886c81918be9c9772e4ca904). Release automation must not create another listing or modify unrelated plugins. Listing metadata, Security category, support URL, skill content, prompts, scan result, attestations, review approval, and final public version are verified separately in OpenAI Platform.

## Consumer verification

Download `SHA256SUMS.txt` and verify the required artifact before execution. For PyPI, pin `maintainer-defense-kit==1.1.1` in an isolated environment and confirm `maintainer-defense --version`. For the plugin, confirm the public directory displays `1.1.1` and the expected skill before treating publication as complete.

## Recovery

If build or verification fails, do not publish the tag. If GitHub succeeds but PyPI fails, rerun the same tag workflow after fixing channel configuration; existing files remain unchanged and missing artifacts publish. If PyPI succeeds but GitHub fails, upload the exact already-built assets for the same signed/verified tag. If plugin review fails, keep the existing public version and revise only the draft update on the existing listing.

Never reuse a version for different bytes. A changed artifact requires a new version.
