# Documentation Reset 1.1.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace every active Markdown and documentation visual with a security-product-first English canonical set, Vietnamese and Japanese essential journeys, deterministic generated evidence, three accessible diagrams, and verified 1.1.1 distributions.

**Architecture:** A checked-in documentation manifest defines the complete active surface and forbidden legacy paths. Hand-authored canonical and localized content is separated from generator-owned evidence, while runtime Markdown keeps stable installer/plugin paths. Three self-contained Diagram Design HTML files explain trust, audit, and consent flows without duplicating reference detail.

**Tech Stack:** Python 3.10+ standard library, unittest, Markdown, JSON, inline HTML/SVG/CSS, Make, GitHub Actions, PyPI Trusted Publishing, existing OpenAI skills-only plugin bundle.

**Spec:** `docs/superpowers/specs/2026-08-24-documentation-reset-design.md`

## Global Constraints

- Product positioning is security-product-first; the curated catalog is secondary.
- English is canonical; Vietnamese is the first localized priority and Japanese is the second.
- Auditor rules, severities, report schema version 1, suppression semantics, patch-only remediation, and offline/read-only boundaries do not change.
- Root `SECURITY.md`, `SUPPORT.md`, `PRIVACY.md`, `TERMS.md`, `docs/AUDITOR.md`, and `docs/AUDITOR_RULES.md` retain stable paths.
- Evidence JSON, schemas, registries, labeled corpus fixtures, Git history, and existing tags are preserved.
- Documentation illustrations are replaced; `assets/plugin-icon.png` and `assets/plugin-icon.svg` are retained byte-for-byte.
- Diagram profile is the shipped `default`; diagrams are static minimal-light, `doc-wide`, English canonical, and self-contained except for the allowed Google Fonts CSS endpoint.
- Every retained Markdown file is newly authored or regenerated in this change.
- Release version is exactly `1.1.1`; Git tag and release path are exactly `v1.1.1`.
- The existing ChatGPT listing `plugins_6a6edab2886c81918be9c9772e4ca904` is updated; no listing is created.

---

### Task 1: Documentation manifest and fail-closed validator

**Files:**
- Create: `documentation-manifest.json`
- Create: `scripts/documentation_contract.py`
- Create: `scripts/test_documentation.py`
- Modify: `Makefile`

**Interfaces:**
- Consumes: repository root and one JSON manifest containing `markdown`, `generated_markdown`, `diagrams`, `retained_images`, and `forbidden_paths`.
- Produces: `validate_documentation_contract(root: Path) -> None`, raising `DocumentationContractError` on the first contract violation; `make documentation-test` and inclusion in `make test`.

- [ ] **Step 1: Write focused failing unit tests for the contract validator**

Create temporary repositories in `scripts/test_documentation.py`. Cover exact Markdown inventory, a forbidden legacy path, an unlisted Markdown file, a missing diagram, an unexpected documentation image, and a retained plugin icon. Use this contract shape:

```python
class DocumentationTests(unittest.TestCase):
    def test_manifest_rejects_unlisted_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(root, markdown=["README.md"])
            (root / "README.md").write_text("# Product\n", encoding="utf-8")
            (root / "OLD.md").write_text("# Old\n", encoding="utf-8")
            with self.assertRaisesRegex(DocumentationContractError, "unlisted Markdown"):
                validate_documentation_contract(root)

    def test_manifest_rejects_forbidden_legacy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(root, markdown=["README.md"], forbidden_paths=["ROADMAP.md"])
            (root / "README.md").write_text("# Product\n", encoding="utf-8")
            (root / "ROADMAP.md").write_text("# Old roadmap\n", encoding="utf-8")
            with self.assertRaisesRegex(DocumentationContractError, "forbidden path"):
                validate_documentation_contract(root)
```

- [ ] **Step 2: Run the new tests and verify the missing module fails**

Run: `python3 scripts/test_documentation.py`

Expected: FAIL because `scripts/documentation_contract.py` does not exist.

- [ ] **Step 3: Implement the reusable validator**

Implement path normalization without following symlinks outside the repository. Hidden Markdown such as `.github/pull_request_template.md` must be included.

```python
class DocumentationContractError(ValueError):
    pass


def repository_markdown(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if ".git" not in path.parts and ".worktrees" not in path.parts
    }


def validate_documentation_contract(root: Path) -> None:
    manifest = json.loads((root / "documentation-manifest.json").read_text(encoding="utf-8"))
    expected = set(manifest["markdown"])
    actual = repository_markdown(root)
    if missing := expected - actual:
        raise DocumentationContractError(f"missing Markdown: {sorted(missing)}")
    if extra := actual - expected:
        raise DocumentationContractError(f"unlisted Markdown: {sorted(extra)}")
    for relative in manifest["forbidden_paths"]:
        if (root / relative).exists():
            raise DocumentationContractError(f"forbidden path exists: {relative}")
```

Also validate that generated Markdown is a subset of `markdown`, required diagrams exist, retained images are the only image files under `assets/`, and every manifest path is normalized, unique, relative, and contains no `..` component.

- [ ] **Step 4: Add the exact final manifest**

The `markdown` array must contain only the paths below, sorted lexicographically:

```text
.github/pull_request_template.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
PRIVACY.md
README.ja.md
README.md
README.vi.md
SECURITY.md
SUPPORT.md
TERMS.md
docs/AUDITOR.md
docs/AUDITOR_EVALUATION.md
docs/AUDITOR_PILOT_PROGRAM.md
docs/AUDITOR_RULES.md
docs/CATALOG.md
docs/CONFIGURATION.md
docs/DISTRIBUTION.md
docs/GETTING_STARTED.md
docs/KIT_ASSURANCE.md
docs/PLAYBOOK.md
docs/README.md
docs/THREAT_MODEL.md
docs/ja/GETTING_STARTED.md
docs/ja/PILOTS.md
docs/ja/PLAYBOOK.md
docs/ja/README.md
docs/ja/SAFETY.md
docs/superpowers/plans/2026-08-24-documentation-reset.md
docs/superpowers/specs/2026-08-24-documentation-reset-design.md
docs/vi/GETTING_STARTED.md
docs/vi/PILOTS.md
docs/vi/PLAYBOOK.md
docs/vi/README.md
docs/vi/SAFETY.md
kits/balanced/.github/PULL_REQUEST_TEMPLATE.md
kits/balanced/README.md
kits/maintainer-defense-kit/README.ja.md
kits/maintainer-defense-kit/README.md
kits/maintainer-defense-kit/README.vi.md
kits/maintainer-defense-kit/locales/en/adoption-record.md
kits/maintainer-defense-kit/locales/en/pull_request_template.md
kits/maintainer-defense-kit/locales/ja/adoption-record.md
kits/maintainer-defense-kit/locales/ja/pull_request_template.md
kits/maintainer-defense-kit/locales/vi/adoption-record.md
kits/maintainer-defense-kit/locales/vi/pull_request_template.md
kits/workflow-hardening/README.md
pilots/2026-08-23-awesome-maintainer-defense/README.md
pilots/2026-08-24-awesome-maintainer-defense/README.md
pilots/README.md
policies/AI_CONTRIBUTIONS.ja.md
policies/AI_CONTRIBUTIONS.md
policies/AI_CONTRIBUTIONS.vi.md
policies/UNSOLICITED_PULL_REQUESTS.ja.md
policies/UNSOLICITED_PULL_REQUESTS.md
policies/UNSOLICITED_PULL_REQUESTS.vi.md
responses/low-quality-pr.md
responses/reproduction-needed.md
skills/audit-repository-workflows/SKILL.md
skills/audit-repository-workflows/references/commands.md
```

`generated_markdown` is exactly `docs/CATALOG.md`, `docs/AUDITOR_EVALUATION.md`, and the two dated pilot `README.md` files. `diagrams` is exactly the three paths from Task 5. `retained_images` is exactly the two plugin icon paths. `forbidden_paths` includes every removed root/doc/visual path from Task 2 and Task 5.

- [ ] **Step 5: Wire the test and validator into project gates**

Add:

```make
documentation-test:
	python3 scripts/test_documentation.py

test: documentation-test audit-test kit-test quickstart-test pilot-test
```

Keep `scripts/validate.py` integration for Task 7, after every final manifest path—including the current-version pilot report—exists. Enabling the final manifest earlier would mask the existing validator mutation tests with expected migration gaps.

- [ ] **Step 6: Run focused tests**

Run: `python3 scripts/test_documentation.py`

Expected: unit fixtures PASS; the real-repository integration case reports the current legacy inventory until Tasks 2–5 complete. Keep the integration assertion in the same test file and run it explicitly after Task 5 rather than weakening the manifest.

- [ ] **Step 7: Commit the validator foundation**

```bash
git add documentation-manifest.json scripts/documentation_contract.py scripts/test_documentation.py scripts/validate.py Makefile
git commit -m "test: define the documentation reset contract"
```

### Task 2: English canonical reset and legacy deletion

**Files:**
- Rewrite: `README.md`, `SECURITY.md`, `SUPPORT.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `PRIVACY.md`, `TERMS.md`, `.github/pull_request_template.md`
- Rewrite: `docs/README.md`, `docs/AUDITOR.md`, `docs/AUDITOR_RULES.md`, `docs/THREAT_MODEL.md`, `docs/KIT_ASSURANCE.md`, `docs/PLAYBOOK.md`, `docs/AUDITOR_PILOT_PROGRAM.md`
- Create: `docs/GETTING_STARTED.md`, `docs/CONFIGURATION.md`, `docs/DISTRIBUTION.md`
- Delete: `CHANGELOG.md`, `ROADMAP.md`, `assets/README.md`
- Delete: `docs/AUDITOR_PILOT.md`, `docs/AUDIT_LOG.md`, `docs/EVALUATION.md`, `docs/MATURITY_MODEL.md`, `docs/NATIVE_CONTROLS.md`, `docs/PROFILE_SIGNALS.md`, `docs/RESOURCE_AUDIT.md`, `docs/SUBMISSION.md`, `docs/VISUAL_STYLE.md`
- Delete: `docs/releases/v1.1.0-pr.md`, `docs/superpowers/plans/2026-08-23-flagship-v1.1.md`, `docs/superpowers/specs/2026-08-23-flagship-v1.1-design.md`
- Modify: `scripts/test_quickstart.py`, `scripts/test_auditor.py`

**Interfaces:**
- Consumes: auditor CLI and existing rule registry without behavioral changes.
- Produces: the complete English product journey, stable auditor help anchors, stable root public-contract URLs, and no legacy narrative paths. Human prose is reviewed directly; automated tests exercise documented commands, paths, links, and generated outputs rather than grepping wording.

- [ ] **Step 1: Add failing English content-contract tests**

In `scripts/test_documentation.py`, assert:

```python
def test_english_product_journey_is_complete(self) -> None:
    for path in (
        "docs/GETTING_STARTED.md",
        "docs/AUDITOR.md",
        "docs/CONFIGURATION.md",
        "docs/THREAT_MODEL.md",
        "docs/KIT_ASSURANCE.md",
        "docs/AUDITOR_PILOT_PROGRAM.md",
        "docs/DISTRIBUTION.md",
    ):
        self.assertTrue((ROOT / path).is_file(), path)

def test_removed_narratives_are_absent(self) -> None:
    for path in MANIFEST["forbidden_paths"]:
        self.assertFalse((ROOT / path).exists(), path)
```

Keep the existing rule registry test: each `### MD-*` section, severity marker, standards URL, and `help_anchor` must remain exact. `scripts/test_quickstart.py` continues to extract and execute the documented source-checkout command instead of asserting prose.

- [ ] **Step 2: Run focused tests and record the expected failures**

Run: `python3 scripts/test_documentation.py DocumentationTests.test_english_product_journey_is_complete DocumentationTests.test_removed_narratives_are_absent`

Expected: FAIL on missing new pages, catalog-first ordering, and present legacy paths.

- [ ] **Step 3: Remove the approved legacy files**

Delete only the exact paths listed for this task with `apply_patch`. Do not remove JSON evidence, schemas, source registries, fixtures, tags, or plugin icons.

- [ ] **Step 4: Write the root product and public-contract pages**

Use new prose throughout. `README.md` has this section order:

```text
# Awesome Maintainer Defense
Security boundary summary
## Quickstart
## What the auditor checks
## From finding to reviewed patch
## Evidence boundaries
## Install options
## Documentation
## Curated catalog
## Contributing and support
## License
```

The quickstart must include `make standalone` followed by `python3 dist/maintainer-defense-kit.py audit .`. Install examples use `maintainer-defense-kit==1.1.1`, verify SHA-256 on POSIX and PowerShell, and never claim repository mutation or online GitHub-settings inspection.

Rewrite the six root public-contract files from their current factual behavior. Preserve the private GitHub Security Advisory route, canonical support URL, local/offline processing statement, warranty limitation, and MIT license reference.

- [ ] **Step 5: Write the canonical English references**

Each page owns one responsibility:

- `GETTING_STARTED.md`: prerequisites, source build, pipx, standalone checksum, first audit, output interpretation, patch generation, and next links.
- `AUDITOR.md`: command grammar and operational behavior only.
- `AUDITOR_RULES.md`: registry-driven rule sections only; no duplicate quickstart.
- `CONFIGURATION.md`: `.maintainer-defense.json`, selector rules, expiry, warnings, and fail-closed errors.
- `THREAT_MODEL.md`: inputs, trust boundaries, excluded online state, attacker capabilities, and residual risk.
- `KIT_ASSURANCE.md`: claim/evidence/limitation table with no field-accuracy claim.
- `PLAYBOOK.md`: triage, review, authorization, rollout, rollback, and recordkeeping used by installed kits.
- `AUDITOR_PILOT_PROGRAM.md`: authority, pinned SHA, disclosure choice, labels, publication gate, and no ranking.
- `DISTRIBUTION.md`: verified channels, artifacts, checksums, Trusted Publisher, existing plugin listing, and release recovery.

- [ ] **Step 6: Update tests that referenced deleted visual or narrative content**

Replace `test_readme_output_matches_published_corpus_case` with a contract that executes the documented quickstart and validates the JSON summary. Remove assertions against `assets/audit-result.svg`; do not replace them with screenshot assertions. Update quickstart tests to read the new root entry points and version 1.1.1 commands.

- [ ] **Step 7: Run English and rule-contract checks**

Run: `python3 scripts/test_documentation.py && python3 scripts/test_quickstart.py && python3 scripts/test_auditor.py`

Expected: content, quickstart, rule anchors, and auditor behavior PASS except for manifest entries intentionally supplied by later tasks.

- [ ] **Step 8: Commit the canonical reset**

```bash
git add -A README.md SECURITY.md SUPPORT.md CONTRIBUTING.md CODE_OF_CONDUCT.md PRIVACY.md TERMS.md .github/pull_request_template.md docs scripts/test_documentation.py scripts/test_quickstart.py scripts/test_auditor.py
git commit -m "docs: replace the canonical product documentation"
```

### Task 3: Vietnamese, Japanese, and runtime Markdown reset

**Files:**
- Rewrite: `README.vi.md`, `README.ja.md`
- Create: `docs/vi/README.md`, `docs/vi/GETTING_STARTED.md`, `docs/vi/SAFETY.md`, `docs/vi/PILOTS.md`
- Create: `docs/ja/README.md`, `docs/ja/GETTING_STARTED.md`, `docs/ja/SAFETY.md`, `docs/ja/PILOTS.md`
- Rewrite: `docs/vi/PLAYBOOK.md`, `docs/ja/PLAYBOOK.md`
- Delete: `docs/vi/KIT_ASSURANCE.md`, `docs/ja/KIT_ASSURANCE.md`
- Rewrite: every manifest-listed Markdown under `kits/`, `policies/`, `responses/`, and `skills/`
- Modify: documentation-like copy in `.github/ISSUE_TEMPLATE/*.yml`, `kits/maintainer-defense-kit/locales/{en,vi,ja}/*.yml`, `i18n/*.json`, and `skills/audit-repository-workflows/agents/openai.yaml` only when it points to removed content or violates the approved language contract.
- Modify: `scripts/test_documentation.py`, `scripts/test_install_kit.py`, `scripts/test_plugin_bundle.py`

**Interfaces:**
- Consumes: English commands and safety/consent markers established by Task 2.
- Produces: localized essential journeys and newly authored runtime Markdown at unchanged embedded-asset paths.

- [ ] **Step 1: Add failing locale parity tests**

Extend `scripts/test_quickstart.py` so each root locale README's documented source-checkout audit command is extracted and executed in a temporary checkout. Keep `scripts/test_install_kit.py::test_profile_language_matrix` as the consumer-level proof that every locale produces the same required installed file set and safe profile behavior. Test local link resolution across every locale page. Review translated safety and consent meaning directly against the approved spec instead of asserting vocabulary strings.

- [ ] **Step 2: Run locale tests and verify expected failures**

Run: `python3 scripts/test_documentation.py -k locale`

Expected: FAIL on missing localized pages and stale commands/copy.

- [ ] **Step 3: Write Vietnamese essentials first**

Write new Vietnamese prose for the root landing page, hub, getting started, safety, pilots, and runtime playbook. Commands stay byte-identical to English. State that English legal/support documents are canonical and that localized explanations do not create separate terms.

- [ ] **Step 4: Write Japanese essentials second**

Write new Japanese prose with the same page responsibilities and command contract. Preserve the same non-execution, non-mutation, patch-review, external-settings, and consent limitations.

- [ ] **Step 5: Rewrite all runtime Markdown**

Use compact operational templates. Adoption records contain owner, date, profile, signal window, findings, false positives, appeals, threshold decision, rollback trigger, and review date. Pull request templates require scope, evidence, permissions/effects, rollback, and human authorization. Policies prohibit agent-authored unsolicited changes without an accountable reviewer and route vulnerabilities privately. Skill/reference pages describe only supported auditor operations and never instruct automatic repository mutation.

- [ ] **Step 6: Verify installer and plugin payloads**

Run: `python3 scripts/test_documentation.py && python3 scripts/test_install_kit.py && make package && python3 scripts/test_plugin_bundle.py`

Expected: locale parity and all profile/language installer matrices PASS; plugin bundle tests may still fail only on the pending version bump in Task 6.

- [ ] **Step 7: Commit localized and runtime content**

```bash
git add -A README.vi.md README.ja.md docs/vi docs/ja kits policies responses skills .github/ISSUE_TEMPLATE i18n scripts/test_documentation.py scripts/test_install_kit.py scripts/test_plugin_bundle.py
git commit -m "docs: replace localized and runtime guidance"
```

### Task 4: Deterministic generated documentation and pilot history

**Files:**
- Create: `docs/CATALOG.md`
- Rewrite: `docs/AUDITOR_EVALUATION.md`
- Rewrite: `pilots/README.md`, `pilots/2026-08-23-awesome-maintainer-defense/README.md`
- Modify: `scripts/render.py`, `scripts/render_audit.py`, `scripts/evaluate_auditor.py`, `scripts/build_pilot_bundle.py`
- Modify: `scripts/validate.py`, `scripts/test_pilot_bundle.py`, `scripts/verify_pilot_evidence.py`

**Interfaces:**
- Consumes: `catalog.json`, `audits.json`, `auditor-rules.json`, corpus JSON, pilot metadata/reports/labels JSON.
- Produces: deterministic `docs/CATALOG.md`, `docs/AUDITOR_EVALUATION.md`, and pilot reports; historical pilot evidence remains reproducible at its recorded source commit.

- [ ] **Step 1: Add failing generator-layout tests**

Require `scripts/render.py` to write only `docs/CATALOG.md`; root READMEs must remain unchanged by `make render`. Require generated notices and deterministic byte-for-byte reruns. Add a historical-pilot test proving an older pilot is fully verified at its pinned source without requiring old runtime files to equal current `HEAD`.

```python
def test_historical_pilot_does_not_claim_current_runtime(self) -> None:
    metadata = {"auditor_version": "1.1.0", "source_commit": "1" * 40}
    self.assertFalse(requires_head_runtime_match(metadata, current_version="1.1.1"))

def test_current_pilot_requires_head_runtime_match(self) -> None:
    metadata = {"auditor_version": "1.1.1", "source_commit": "2" * 40}
    self.assertTrue(requires_head_runtime_match(metadata, current_version="1.1.1"))
```

- [ ] **Step 2: Run generator and pilot tests red**

Run: `python3 scripts/test_pilot_bundle.py && python3 scripts/test_documentation.py`

Expected: FAIL on old output paths/format and historical `HEAD` runtime comparison.

- [ ] **Step 3: Refactor generators around single ownership**

Make `scripts/render.py` combine catalog presentation with audited evidence from `audits.json` into `docs/CATALOG.md`. Keep `scripts/render_audit.py` as a compatibility entry point that delegates to the same renderer without writing a second file, or delete it and update Make/validation in the same commit. `evaluate_auditor.py` writes only the synthetic evaluation page. No generator edits root READMEs.

- [ ] **Step 4: Update pilot report rendering and provenance rules**

Rewrite report headings and explanations while preserving bundle JSON and labels. In `verify_pilot_evidence.py`, always rebuild each auditor at its recorded source and reproduce its reports. Require the source-to-`HEAD` runtime equality check only for a pilot whose `auditor_version` equals the current package version; historical versions remain explicitly historical.

- [ ] **Step 5: Regenerate committed output**

Run: `make render` and rebuild the existing 2026-08-23 pilot README using `scripts/build_pilot_bundle.py` with its unchanged JSON inputs.

Expected: only the three generator-owned Markdown outputs for the current repository state change; root and localized hand-authored pages remain byte-identical.

- [ ] **Step 6: Verify determinism and provenance**

Run: `make render && git diff --exit-code -- docs/CATALOG.md docs/AUDITOR_EVALUATION.md pilots/2026-08-23-awesome-maintainer-defense/README.md && python3 scripts/test_pilot_bundle.py`

Expected: PASS and no second-run diff.

- [ ] **Step 7: Commit generated documentation architecture**

```bash
git add -A docs/CATALOG.md docs/AUDITOR_EVALUATION.md pilots scripts/render.py scripts/render_audit.py scripts/evaluate_auditor.py scripts/build_pilot_bundle.py scripts/validate.py scripts/test_pilot_bundle.py scripts/verify_pilot_evidence.py Makefile
git commit -m "docs: rebuild generated evidence references"
```

### Task 5: Diagram Design visuals and old-asset removal

**Files:**
- Create: `.diagram-design`
- Create: `docs/diagrams/trust-boundaries.html`
- Create: `docs/diagrams/audit-to-action.html`
- Create: `docs/diagrams/consent-to-evidence.html`
- Create: `scripts/verify_diagrams.py`
- Modify: `scripts/test_documentation.py`, `scripts/verify_release_assets.py`, `README.md`, `docs/README.md`, `docs/THREAT_MODEL.md`, `docs/AUDITOR_PILOT_PROGRAM.md`, locale hubs/safety/pilot pages
- Delete: `assets/audit-result.svg`, `assets/audit-result.png`, `assets/demo.gif`, `assets/social-preview.svg`, `assets/social-preview.png`
- Delete: `scripts/render_demo.mjs`, `scripts/render_social_preview.mjs` if no non-documentation consumer remains.
- Preserve byte-for-byte: `assets/plugin-icon.png`, `assets/plugin-icon.svg`

**Interfaces:**
- Consumes: Diagram Design default profile and the exact semantic/type references named below.
- Produces: three accessible single-file HTML diagrams and repository-local validation independent of the installed skill path.

- [ ] **Step 1: Resolve the default profile and read required references**

Create the recoverable `~/.diagram-design/profiles/default.md` snapshot only if absent and only from the pristine shipped `references/style-guide.md`, following `references/profiles.md`. Add `.diagram-design` with exactly:

```text
profile: default
```

Read these references completely before drawing:

```text
/Users/thang/.agents/skills/diagram-design/references/semantic-patterns.md
/Users/thang/.agents/skills/diagram-design/references/type-architecture.md
/Users/thang/.agents/skills/diagram-design/references/type-process.md
/Users/thang/.agents/skills/diagram-design/references/type-data-flow.md
/Users/thang/.agents/skills/diagram-design/references/output-spec.md
/Users/thang/.agents/skills/diagram-design/assets/template.html
```

- [ ] **Step 2: Add failing repository-local diagram tests**

`scripts/verify_diagrams.py` checks exact files, self-contained HTML, the permitted `fonts.googleapis.com/css2` URL only, `<svg role="img">`, prefixed title/description IDs, title-first SVG child, no `writing-mode`, no shadow, no JetBrains Mono, no diagonal `<line>` connectors, at most two accent node treatments, and a bottom legend. `scripts/test_documentation.py` asserts old visuals are absent and plugin icon SHA-256 values equal the pre-reset values recorded before deletion.

- [ ] **Step 3: Run the diagram checks red**

Run: `python3 scripts/verify_diagrams.py`

Expected: FAIL because the three diagram files do not exist.

- [ ] **Step 4: Draw trust boundaries**

Use secure paved road + architecture, `doc-wide`, at most seven nodes. Show repository checkout, offline auditor, findings, reviewable patch, human review, optional authorized apply, and external GitHub settings outside the inspected boundary. Omit rule IDs and distribution channels.

- [ ] **Step 5: Draw audit to action**

Use stage framework + process, `doc-wide`, at most six stages. Each stage states input, governance decision, and output. Make human patch authorization the single focal stage. Omit schema fields and per-rule branches.

- [ ] **Step 6: Draw consent to evidence**

Use data flow, `doc-wide`, at most seven nodes. Show maintainer authority/consent, pinned checkout, offline report, maintainer labels, disclosure choice, deterministic bundle, and permitted publication. Unresolved labels must remain visible. Omit aggregate formulas.

- [ ] **Step 7: Remove old visuals and obsolete renderers**

Delete only the exact approved visual paths. Rewrite `scripts/verify_release_assets.py` to verify retained plugin icons and the three HTML diagram contracts, or replace its Make target with `scripts/verify_diagrams.py`. Do not delete or rewrite plugin icons.

- [ ] **Step 8: Link diagrams with textual equivalents**

English pages link the relevant diagram and summarize its message in prose. Vietnamese and Japanese pages link the same canonical diagram and include localized textual equivalents for accessibility and comprehension.

- [ ] **Step 9: Run Diagram Design and repository checks**

Run:

```bash
python3 /Users/thang/.agents/skills/diagram-design/scripts/self_check.py docs/diagrams/trust-boundaries.html
python3 /Users/thang/.agents/skills/diagram-design/scripts/self_check.py docs/diagrams/audit-to-action.html
python3 /Users/thang/.agents/skills/diagram-design/scripts/self_check.py docs/diagrams/consent-to-evidence.html
python3 scripts/verify_diagrams.py
python3 scripts/test_documentation.py
```

Expected: all checks PASS; only the two plugin icon files remain under `assets/`.

- [ ] **Step 10: Commit the visual reset**

```bash
git add -A .diagram-design docs/diagrams assets scripts/verify_diagrams.py scripts/verify_release_assets.py scripts/test_documentation.py README.md docs
git commit -m "docs: replace legacy visuals with accessible diagrams"
```

### Task 6: Version 1.1.1 and distribution contracts

**Files:**
- Modify: `pyproject.toml`, `scripts/install_kit.py`, `scripts/build_plugin_bundle.py`
- Modify: `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `.kimi-plugin/plugin.json`
- Modify: `Formula/maintainer-defense-kit.rb`, `.github/workflows/release.yml`
- Modify: `.github/ISSUE_TEMPLATE/auditor-false-positive.yml`
- Modify: `scripts/test_distribution.py`, `scripts/test_plugin_bundle.py`, release verification scripts
- Modify: all active documentation containing an install version, release URL, bundle name, or release title.

**Interfaces:**
- Consumes: final documentation/runtime assets from Tasks 2–5.
- Produces: standalone, wheel, sdist, Homebrew formula, checksums, and existing-listing plugin bundle with exact version 1.1.1.

- [ ] **Step 1: Change expected versions in tests first**

Set `EXPECTED_VERSION = "1.1.1"` in distribution and plugin tests. Extend quickstart/package tests to execute versioned install paths and assert produced artifact names at 1.1.1. Review release-facing Markdown for stale version references during Task 8; historical pilot reports and the approved design/plan remain truthful records.

- [ ] **Step 2: Run distribution tests red**

Run: `python3 scripts/test_distribution.py && python3 scripts/test_plugin_bundle.py`

Expected: FAIL with version mismatches and missing 1.1.1 artifacts.

- [ ] **Step 3: Advance every public version contract**

Set package, CLI, three plugin manifests, plugin builder, formula, issue placeholder, documentation URLs, release title, and artifact names to 1.1.1. Keep report schema versions at 1. Do not edit historical pilot JSON fields that truthfully record auditor 1.1.0.

- [ ] **Step 4: Build all artifacts once**

Run: `make package`

Update the Homebrew SHA-256 to the digest emitted for `dist/maintainer-defense-kit.py`. Regenerate `dist/SHA256SUMS.txt` through the existing builder.

- [ ] **Step 5: Run distribution verification**

Run: `make distribution-test && make metadata && make pins`

Expected: standalone aliases, wheel, sdist, clean installs, Homebrew formula, plugin bundle contents, deterministic timestamps, and checksums PASS at 1.1.1.

- [ ] **Step 6: Commit the release contract**

```bash
git add -A pyproject.toml scripts .codex-plugin .claude-plugin .kimi-plugin Formula .github README.md README.vi.md README.ja.md docs kits policies responses skills
git commit -m "release: prepare Maintainer Defense Kit 1.1.1"
```

### Task 7: Pinned 1.1.1 owner-directed pilot

**Files:**
- Create: `pilots/2026-08-24-awesome-maintainer-defense/metadata.json`
- Create: `pilots/2026-08-24-awesome-maintainer-defense/raw-report.json`
- Create: `pilots/2026-08-24-awesome-maintainer-defense/effective-report.json`
- Create: `pilots/2026-08-24-awesome-maintainer-defense/labels.json`
- Create: `pilots/2026-08-24-awesome-maintainer-defense/pilot.json`
- Create: `pilots/2026-08-24-awesome-maintainer-defense/README.md`
- Modify: `pilots/README.md`, `docs/KIT_ASSURANCE.md`, `docs/AUDITOR_EVALUATION.md` generator inputs only if a current-version evidence link is required.
- Modify: `scripts/validate.py`

**Interfaces:**
- Consumes: the exact release-candidate commit after Tasks 1–6 and its 1.1.1 standalone artifact.
- Produces: reproducible `internal-owner-directed` 1.1.1 evidence that is explicitly non-independent and non-representative.

- [ ] **Step 1: Record the release-candidate commit**

Run: `git status --short && git rev-parse HEAD`

Expected: clean worktree. Use the returned full SHA as both `source_commit` and `target_commit` in the new metadata. Do not amend or squash that commit after capturing it.

- [ ] **Step 2: Build and audit the pinned candidate**

Run:

```bash
make standalone
python3 dist/maintainer-defense-kit.py audit . --format json --output pilots/2026-08-24-awesome-maintainer-defense/raw-report.json
python3 dist/maintainer-defense-kit.py audit . --format json --output pilots/2026-08-24-awesome-maintainer-defense/effective-report.json
shasum -a 256 dist/maintainer-defense-kit.py
```

Record the emitted digest, exact command, full source/target SHA, UTC timestamp, disclosure `repository-and-sanitized-results`, `pilot_type` `internal-owner-directed`, reviewer role `implementation-agent-under-owner-direction`, `allow_aggregate_metrics` false, and limitations stating that this is neither independent nor representative.

- [ ] **Step 3: Preserve unresolved labels honestly**

Create `labels.json` as an object keyed only by actual finding fingerprints. If the self-audit has zero findings, use `{}`. Never create true-positive or false-positive labels without repository-local evidence and reviewer authorization.

- [ ] **Step 4: Build the deterministic bundle**

Run `scripts/build_pilot_bundle.py` with the six exact paths in this task and write `pilot.json` plus `README.md`.

- [ ] **Step 5: Verify current and historical pilots**

Run: `python3 scripts/test_pilot_bundle.py && make pilot-verify`

Expected: both dated pilots reproduce at their own pinned commits; only the 1.1.1 pilot is required to match current runtime paths.

- [ ] **Step 6: Enable the final documentation manifest gate**

Import `DocumentationContractError` and `validate_documentation_contract` in `scripts/validate.py`. Call the contract before catalog validation and route errors through `fail(str(exc))`. Run the existing quickstart validator-mutation tests to prove the complete manifest no longer masks their targeted failures.

- [ ] **Step 7: Commit evidence without changing runtime files**

```bash
git add pilots/2026-08-24-awesome-maintainer-defense pilots/README.md docs/KIT_ASSURANCE.md docs/AUDITOR_EVALUATION.md scripts/validate.py
git commit -m "docs: publish pinned 1.1.1 dogfood evidence"
```

### Task 8: Full verification, review, PR, and merge

**Files:**
- Review: all changed files against the spec and documentation manifest.
- Modify: only defects discovered by verification or review.

**Interfaces:**
- Consumes: completed Tasks 1–7.
- Produces: a reviewable PR merged into `main` with all required checks green and no stale branch/worktree residue.

- [ ] **Step 1: Run the full local release gate from a clean state**

Run:

```bash
make render
git diff --exit-code -- docs/CATALOG.md docs/AUDITOR_EVALUATION.md pilots
make test
make validate
make pilot-verify
make package
make distribution-test
make links
make metadata
make pins
python3 scripts/verify_diagrams.py
git diff --check
git status --short
```

Expected: every command PASS; status contains only intended tracked source changes before the final commit and is clean after it.

- [ ] **Step 2: Audit deletion and new-content coverage**

Run the manifest validator, list tracked Markdown including hidden paths, list all remaining image/diagram files, and compare against `documentation-manifest.json`. Verify plugin icon digests equal the pre-reset values. Search active Markdown for old version strings, removed paths, unsupported accuracy claims, and stale catalog-first headings.

- [ ] **Step 3: Review against the approved spec**

Check every acceptance criterion, the exact English/VI/JA priority, diagram complexity budgets, generated ownership, stable external paths, and plugin-listing identity. Fix only evidence-backed gaps, then rerun the affected focused tests and full gate.

- [ ] **Step 4: Commit final verification fixes**

```bash
git add -A
git commit -m "test: enforce documentation and release gates"
```

Skip the commit only when no file changed.

- [ ] **Step 5: Push and open the PR**

Push `codex/documentation-reset-1.1.1`. Open one PR against `main` titled `release: reset documentation for 1.1.1`. The body links the spec, enumerates deleted legacy classes, states the plugin icon preservation boundary, reports exact test counts, and says the new pilot is owner-directed rather than independent.

- [ ] **Step 6: Wait for all required checks and merge**

Use `gh pr checks --watch`. Merge only when Quality and workflow-security checks are successful and the PR is mergeable. Use a merge commit so the 1.1.1 pilot source commit remains reachable.

- [ ] **Step 7: Update and verify `main`**

Fast-forward local `main` to `origin/main`, rerun `make test && make validate && make pilot-verify`, then remove the exact worktree and local/remote feature branch. Verify `git worktree list`, `git branch --all`, open PRs, and `git status --short --branch`.

### Task 9: Publish and verify 1.1.1

**Files:**
- No source edits after the release commit unless a failed gate identifies a real defect requiring a new reviewed commit and tag decision.

**Interfaces:**
- Consumes: verified merged `origin/main`, configured PyPI Trusted Publisher, and existing ChatGPT plugin listing.
- Produces: signed `v1.1.1`, GitHub Release assets, PyPI 1.1.1 wheel/sdist, and existing public ChatGPT listing at 1.1.1.

- [ ] **Step 1: Create and push the release tag**

Verify `origin/main` is clean and all gates are fresh. Create signed tag `v1.1.1` at the exact merge commit and push only that tag.

- [ ] **Step 2: Wait for release workflow completion**

Watch the tag-triggered release workflow. Verify GitHub Release is non-draft/non-prerelease, contains the standalone aliases, checksums, wheel, sdist, and `awesome-maintainer-defense-openai-skills-v1.1.1.zip`, and that asset digests match the committed build contract.

- [ ] **Step 3: Verify PyPI independently**

Read `https://pypi.org/pypi/maintainer-defense-kit/json`, require version 1.1.1 with non-yanked wheel and sdist, install `maintainer-defense-kit==1.1.1` into a new temporary virtual environment, run `maintainer-defense --version`, and run one JSON audit against a safe empty repository.

- [ ] **Step 4: Prepare the existing ChatGPT listing update**

Open listing `plugins_6a6edab2886c81918be9c9772e4ca904`, create or inspect only its 1.1.1 update submission, upload the verified 1.1.1 bundle, and verify category Security, capability Read, canonical support/privacy/terms URLs, one skill, and the approved prompts. Do not touch any other listing.

- [ ] **Step 5: Request action-time confirmation before submission/publication**

Immediately before clicking the browser control that submits for review or publishes the update, report the exact listing, version, and external action and obtain confirmation as required by the browser confirmation policy.

- [ ] **Step 6: Submit, publish, and verify public state**

After confirmation, submit the existing-listing update. If automated scan/review is pending, wait through the configured task/heartbeat mechanism. When approved, publish the update and verify the public directory page displays version 1.1.1, Security, Read, the skill, and prompts.

- [ ] **Step 7: Final release report**

Report the merge commit, tag, GitHub Release URL, PyPI URL, public plugin URL, exact local/CI test evidence, deletion boundary, diagram paths, pilot limitation, and whether the external independent-maintainer pilot remains consent-gated.
