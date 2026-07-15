# Contributing

> Contribution contract for catalog evidence, product changes, translations, and release safety.

Contributions are welcome when they make maintainer defenses safer, more useful, or easier to verify. Read the [documentation map](docs/README.md) before adding a new concept or duplicating an existing contract.

## Add or update a catalog resource

1. Search `catalog.json` and open pull requests for duplicates.
2. Confirm the resource has public documentation and a concrete maintainer use case.
3. Review required permissions, external data sharing, destructive actions, false-positive controls, maintenance activity, and license.
4. Add one entry to `catalog.json`. Keep the description factual and under 160 characters when practical.
5. Add a matching record to `audits.json` with official evidence for deployment, default behavior, maximum effects, data boundaries, access, limitations, repository activity, and license detection.
6. Add Vietnamese and Japanese descriptions to `i18n/vi.json` and `i18n/ja.json`. Product names remain unchanged; descriptions must preserve risk qualifications.
7. Run:

   ```bash
   make render
   make validate
   make links
   make metadata
   ```

8. Complete the pull-request template and disclose your relationship to the resource.

## Evidence bar

Resources should materially reduce at least one of these burdens:

- spam, harassment, or coordinated repository abuse;
- low-quality or unsolicited contribution review;
- unsafe issue, pull-request, or security-report intake;
- malicious workflow, dependency, credential, or merge-path changes;
- inconsistent policy or incident response.

Open-source projects are preferred. A proprietary service may be considered only when it has a useful free tier, clear documentation, disclosed data handling, and no misleading detection claims. Reusable software or templates without a license do not meet the inclusion bar.

We generally reject abandoned proofs of concept, undisclosed affiliate links, generic developer tools, paywalled-only products, duplicate wrappers, and tools that present automated authorship guesses as proof of misconduct.

## Write factual descriptions

Describe what the resource does—not what its marketing page claims. Avoid words such as “best,” “revolutionary,” “perfect,” and “100% accurate.” Note when a resource can close, lock, delete, block, execute untrusted code, or send repository data to an external service.

## Edit canonical sources

The resource tables in all three README files and `docs/RESOURCE_AUDIT.md` are generated. Edit the catalog, audit, and translation data, then run `make render`. CI fails if generated content is stale, audit coverage differs, a translation is missing, or an audit is more than 180 days old.

## Audit impact labels

- `low`: read-only analysis or documentation in normal use;
- `medium`: can label, comment, fail checks, publish reports, or modify local files;
- `high`: can close, lock, delete, block, limit interactions, or change repository settings.

Use the maximum documented capability, even when the default configuration is safer. Impact is not a quality score.

## Change the auditor or kit

Product changes receive a higher safety review. Add corpus cases for auditor behavior; preserve JSON/SARIF contracts; keep installation conflict-safe; use least-privilege workflow permissions; pin Actions to full SHAs; and avoid privileged execution of untrusted code. Automatic closing, locking, or blocking remains opt-in.

Run `make test`, `make validate`, `make standalone`, and the self-audit before opening a pull request. Workflow changes must also pass zizmor in CI.

## Diagrams

Follow [`docs/VISUAL_STYLE.md`](docs/VISUAL_STYLE.md): give each diagram one clear purpose, use standard notation and consistent visual grammar, and provide language parity when the diagram affects adoption decisions.

## No pay-to-play

Listings cannot be purchased. Stars, backlinks, sponsorships, gifts, employment, or reciprocal promotion do not guarantee inclusion or featured status.
