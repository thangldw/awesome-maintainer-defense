# Documentation Reset 1.1.1 Design

## Decision

Awesome Maintainer Defense will replace its existing documentation system with a security-product-first documentation set. English is canonical. Vietnamese and Japanese provide complete essential journeys without duplicating deep reference material. Old Markdown, historical narrative files, generated prose, documentation diagrams, screenshots, and demonstrations are removed from `main`; Git history and immutable release tags remain the recovery path.

The reset is a public-content change to the Python distribution, Maintainer Defense Kit, and existing ChatGPT plugin bundle. It therefore ships as version 1.1.1 through the existing GitHub, PyPI, and ChatGPT release paths. It must not create a new plugin listing.

## Goals

- Make the auditor and Maintainer Defense Kit the primary product story.
- Give a maintainer one unambiguous path from installation to audit, interpretation, patch review, and evidence publication.
- Replace every retained Markdown file with newly authored content.
- Remove obsolete, duplicated, historical, and generated Markdown that no longer belongs in the active information architecture.
- Replace documentation visuals with three accessible, self-contained HTML diagrams generated under the Diagram Design contract.
- Preserve runtime paths that are embedded into standalone, wheel, sdist, and plugin artifacts.
- Preserve evidence JSON, schemas, source registries, Git history, and tagged releases.
- Keep English, Vietnamese, and Japanese commands, effects, safety boundaries, and consent language semantically aligned.

## Non-goals

- Changing auditor rules, severities, report schemas, suppression behavior, or patch-only remediation behavior.
- Rebranding or replacing the published plugin icon.
- Translating every deep reference page into Vietnamese and Japanese.
- Migrating old prose into an archive directory on `main`.
- Claiming independent field accuracy before an authorized external maintainer completes a pilot.
- Retaining compatibility stubs at deleted Markdown paths. Stable root legal/support URLs and auditor help paths are retained instead.

## Destructive Migration Boundary

The following classes are deleted from `main`:

- old release notes, changelog prose, roadmap prose, design specs, and implementation plans;
- duplicated auditor, assurance, maturity, native-control, profile-signal, submission, and visual-style pages whose responsibilities move into the new canonical set;
- old documentation screenshots, result illustrations, animated demonstrations, and social-preview files;
- old generated Markdown before it is rebuilt by the new generators.

The following classes are preserved:

- Git history and tags, including `v1.1.0`;
- release artifacts already published for earlier versions;
- evidence JSON under `pilots/`, catalog/audit registries, schemas, labeled corpus fixtures, and workflow pin metadata;
- executable source, workflows, tests, and package configuration except where paths, validation, generators, or version metadata must change;
- `assets/plugin-icon.png` and `assets/plugin-icon.svg`, because they are the identity assets of the existing published listing rather than documentation illustrations.

Deletion is recoverable from Git. The implementation must use an isolated worktree and one scoped branch.

## Information Architecture

### Root entry points

- `README.md`: English product landing page and shortest verified quickstart.
- `README.vi.md`: Vietnamese essential landing page.
- `README.ja.md`: Japanese essential landing page.
- `SECURITY.md`: supported versions, private reporting, response expectations, and disclosure boundary.
- `SUPPORT.md`: support channels, diagnostic evidence, and response scope.
- `CONTRIBUTING.md`: contribution paths, evidence requirements, local gates, and review expectations.
- `CODE_OF_CONDUCT.md`: concise community conduct and enforcement route.
- `PRIVACY.md`: canonical data-processing statement for the local, read-only product.
- `TERMS.md`: canonical use limitations and responsibility boundary.

`CHANGELOG.md` and `ROADMAP.md` are removed. GitHub Releases is the release history; GitHub Issues is the active roadmap.

### English canonical documentation

- `docs/README.md`: documentation hub organized by user task.
- `docs/GETTING_STARTED.md`: installation, checksum verification, first audit, and result interpretation.
- `docs/AUDITOR.md`: CLI behavior, formats, exit policy, baselines, suppressions, and patch-only fixes.
- `docs/AUDITOR_RULES.md`: one registry-aligned section per implemented rule and stable help anchors.
- `docs/CONFIGURATION.md`: configuration schema, suppression governance, examples, and failure modes.
- `docs/THREAT_MODEL.md`: trust boundaries, attacker capabilities, offline limits, and residual risk.
- `docs/KIT_ASSURANCE.md`: assurance claims mapped to executable evidence and explicit limitations.
- `docs/PLAYBOOK.md`: runtime response and adoption playbook embedded by the installer.
- `docs/AUDITOR_PILOT_PROGRAM.md`: consent, pinned execution, maintainer review, disclosure, and publication contract.
- `docs/DISTRIBUTION.md`: source, standalone, pipx, Homebrew, GitHub Release, PyPI, and existing ChatGPT listing.
- `docs/CATALOG.md`: generated secondary catalog reference sourced from `catalog.json` and `audits.json`.
- `docs/AUDITOR_EVALUATION.md`: generated synthetic-corpus evaluation sourced from the labeled corpus and rule registry.

### Localized essentials

Vietnamese lives under `docs/vi/`; Japanese lives under `docs/ja/`. Each locale contains:

- `README.md`: localized documentation hub;
- `GETTING_STARTED.md`: full install and first-audit journey;
- `SAFETY.md`: read-only scope, patch-only behavior, limitations, and legal/support links;
- `PILOTS.md`: consent and evidence-publication journey;
- `PLAYBOOK.md`: fully localized runtime playbook embedded by the installer.

Deep auditor rules, configuration schema, threat model, assurance mapping, distribution internals, and generated evidence remain English canonical. Localized pages link to those references and provide enough context to use them safely.

### Runtime Markdown

All retained Markdown under these paths is newly authored while preserving its runtime contract:

- `kits/balanced/README.md`;
- `kits/workflow-hardening/README.md`;
- `kits/maintainer-defense-kit/README.md`, `README.vi.md`, and `README.ja.md`;
- `kits/maintainer-defense-kit/locales/{en,vi,ja}/adoption-record.md`;
- `kits/maintainer-defense-kit/locales/{en,vi,ja}/pull_request_template.md`;
- `policies/AI_CONTRIBUTIONS{,.vi,.ja}.md`;
- `policies/UNSOLICITED_PULL_REQUESTS{,.vi,.ja}.md`;
- `responses/low-quality-pr.md` and `responses/reproduction-needed.md`;
- `skills/audit-repository-workflows/SKILL.md`;
- `skills/audit-repository-workflows/references/commands.md`;
- `pilots/README.md` and the generated pilot report at the existing pinned pilot directory.

Documentation-like YAML and JSON copy surfaces are reviewed and rewritten when their wording points to removed pages or contradicts the new content model. Executable workflow behavior and product source data are otherwise unchanged.

### Generated Markdown

Generators own all generated prose:

- `scripts/render.py` writes `docs/CATALOG.md` instead of inserting the catalog into root READMEs.
- `scripts/render_audit.py` contributes evidence fields to the generated catalog reference rather than maintaining a separate duplicate narrative.
- `scripts/evaluate_auditor.py` writes the new `docs/AUDITOR_EVALUATION.md` format.
- `scripts/build_pilot_bundle.py` rebuilds the pinned pilot report in the new evidence format without changing evidence JSON or inventing labels.

Generated files carry an explicit generated notice and deterministic output. Validation fails when regeneration changes a committed file.

## Content Contract

Every user journey follows this order:

1. install or obtain a verified artifact;
2. run an offline audit against an explicit target;
3. interpret findings as review inputs rather than vulnerability proof;
4. generate a patch without applying it;
5. review and authorize any repository change;
6. publish evidence only under an explicit pilot disclosure choice.

Claims must distinguish:

- tested engineering behavior;
- deterministic synthetic-corpus evaluation;
- owner-directed, non-independent evidence;
- independently labeled field evidence.

The documentation must not publish precision, recall, ranking, or repository scores without the independent-label and sample-contract gates already enforced by the pilot builder.

Commands in English, Vietnamese, and Japanese entry points are byte-equivalent except for surrounding prose. Commands reference version 1.1.1 and paths that are produced by the build. Effects, network boundaries, mutation boundaries, consent requirements, and known limitations retain the same meaning across locales.

English legal and support files are canonical. Localized pages summarize the routing decision and link to the canonical files; they do not create independent localized legal contracts.

## Diagram System

The project will record its explicit selection of the shipped Diagram Design profile with a `.diagram-design` marker containing exactly `profile: default` and a valid local default profile snapshot as required by the skill.

All diagrams use the minimal-light variant, static mode, English canonical labels, `doc-wide` sizing, and mixed technical/maintainer audience. Each file is a self-contained HTML document with inline CSS and SVG; Google Fonts is the only permitted remote dependency. Vietnamese and Japanese pages provide textual equivalents.

### Trust boundaries

- Path: `docs/diagrams/trust-boundaries.html`
- Semantic pattern: secure paved road.
- Visual type: architecture.
- Budget: at most seven nodes and ten connectors.
- Focal message: repository content crosses into offline inspection, but execution and repository mutation remain outside the paved road.
- Deliberate cuts: individual rule IDs, GitHub organization settings, and distribution channels stay in prose.

### Audit to action

- Path: `docs/diagrams/audit-to-action.html`
- Semantic pattern: stage framework with semantic slots.
- Visual type: process.
- Budget: at most six stages and eight connectors.
- Focal message: evidence becomes a reviewable patch, never an automatically applied change.
- Deliberate cuts: per-format field schemas and per-rule branching stay in reference pages.

### Consent to evidence

- Path: `docs/diagrams/consent-to-evidence.html`
- Semantic pattern: none; the dominant axis is role-scoped evidence flow.
- Visual type: data flow.
- Budget: at most seven nodes and nine connectors.
- Focal message: maintainer consent and labels gate any publication; unresolved findings remain unresolved.
- Deliberate cuts: aggregate metric formulas and internal dogfood details stay in the pilot documentation.

Each SVG has a prefixed title and description, `role="img"`, resolved `aria-labelledby`, orthogonal connectors, fanned attach points, masked connector labels, a bottom legend, a four-pixel grid, and no more than two accent elements. The installed Diagram Design `self_check.py` and the relevant geometry check must pass for every file.

## Validation and Failure Handling

The documentation manifest is explicit. Validation fails closed when:

- a required new path is absent;
- a forbidden legacy path returns;
- an unlisted Markdown or documentation visual appears;
- a local Markdown link is broken;
- localized entry-point commands differ from English;
- localized safety or consent contract markers are absent;
- a quickstart path does not exist or its command does not run;
- auditor rule IDs, severities, anchors, or standards mappings differ from the registry;
- generated Markdown is stale;
- a diagram fails accessibility, single-file, geometry, connector, or token checks;
- package, standalone, wheel, sdist, or plugin bundle content omits a required rewritten runtime document;
- any old documentation screenshot, demonstration, or social-preview artifact remains.

External links are checked separately from deterministic local-link validation. A transient network failure is reported as external evidence failure, not converted into a local-content pass.

The old deep links intentionally removed from `main` may return 404. Versioned `v1.1.0` links remain available through the immutable tag. Root `SECURITY.md`, `SUPPORT.md`, `PRIVACY.md`, and `TERMS.md`, plus `docs/AUDITOR.md` and `docs/AUDITOR_RULES.md`, retain stable paths because external product contracts depend on them.

## Release Contract

The implementation bumps all public version contracts to 1.1.1, including Python package metadata, CLI version output, standalone builders, release assets, Homebrew formula, plugin manifest, submission documentation, and tests.

The release gate runs the complete existing suite plus the new documentation-manifest, localization-parity, and diagram checks. It builds the standalone artifacts, wheel, sdist, and deterministic plugin bundle once. Tag `v1.1.1` publishes through the existing GitHub Actions release workflow and PyPI Trusted Publisher. The existing ChatGPT listing is updated with the 1.1.1 bundle and verified on its public directory page. No additional listing is created.

## Acceptance Criteria

- Every retained Markdown file is newly authored or newly generated in this change.
- Every approved legacy Markdown and documentation visual is absent from `main`.
- The root landing page is security-product-first and the catalog is secondary.
- English canonical and VI/JA essential journeys pass command, effect, limitation, and consent parity tests.
- All three diagrams pass Diagram Design checks and are linked from the correct canonical and localized pages.
- The runtime installer, auditor, kit profiles, pilot builder, package, and plugin bundle retain their behavioral contracts.
- The repository passes local tests, validation, link checks, package tests, distribution tests, pilot provenance checks, metadata checks, pin checks, workflow-security checks, and GitHub CI.
- Version 1.1.1 is published on GitHub and PyPI, and the existing ChatGPT listing publicly displays 1.1.1.
