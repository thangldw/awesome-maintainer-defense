# Contributing

Contributions are welcome when they make this collection more useful, safer, or easier to verify for maintainers.

## Add a resource

1. Search `catalog.json` and open pull requests for duplicates.
2. Confirm the resource has public documentation and a concrete maintainer use case.
3. Review required permissions, external data sharing, destructive actions, false-positive controls, maintenance activity, and license.
4. Add one entry to `catalog.json`. Keep the description factual and under 160 characters when practical.
5. Run:

   ```bash
   python3 scripts/render.py
   python3 scripts/validate.py
   ```

6. Complete the pull-request template and disclose your relationship to the resource.

## Inclusion bar

Resources should materially reduce at least one of these burdens:

- spam, harassment, or coordinated repository abuse;
- low-quality or unsolicited contribution review;
- unsafe issue, pull-request, or security-report intake;
- malicious workflow, dependency, credential, or merge-path changes;
- inconsistent policy or incident response.

Open-source projects are preferred. A proprietary service may be considered only when it has a useful free tier, clear documentation, disclosed data handling, and no misleading detection claims.

We generally reject abandoned proofs of concept, undisclosed affiliate links, generic developer tools, paywalled-only products, duplicate wrappers, and tools that present automated authorship guesses as proof of misconduct.

## Descriptions

Describe what the resource does—not what its marketing page claims. Avoid words such as “best,” “revolutionary,” “perfect,” and “100% accurate.” Note when a resource can close, lock, delete, block, execute untrusted code, or send repository data to an external service.

## Editing generated content

The resource tables in `README.md` are generated. Edit `catalog.json`, then run `python3 scripts/render.py`. CI fails if the generated section is stale.

## Changes to the starter kit

Starter-kit changes receive a higher safety review. Workflows must use least-privilege permissions, pin third-party Actions to a full commit SHA, and avoid checking out untrusted code under `pull_request_target`. Automatic closing, locking, or blocking must remain opt-in.

## No pay-to-play

Listings cannot be purchased. Stars, backlinks, sponsorships, gifts, employment, or reciprocal promotion do not guarantee inclusion or featured status.
