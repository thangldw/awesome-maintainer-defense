# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

An installable, reversible baseline for reducing maintainer review load without claiming to detect AI authorship. The installer defaults to a dry run, never overwrites a conflicting file, records every installed file, and can verify or safely remove its own changes.

## Profiles

| Profile | GitHub token | Repository effect | Intended use |
| --- | --- | --- | --- |
| `observe` (default) | read-only | Job summary only | Measure signals and false positives before changing contributor-visible state. |
| `balanced` | PR write | Adds `needs-human-review`; no comment, close, or lock | Human-review queue after an observation period. |
| `hardened` | mixed, per job | Balanced triage plus dependency review and workflow static analysis | Repositories with dependency or Actions supply-chain exposure. |

All profiles also install a structured bug form, PR template, contribution policies, an operations playbook, a label specification, and an adoption record. English (`en`), Vietnamese (`vi`), and Japanese (`ja`) are complete deployment languages—not README-only translations.

## Install safely

Run these commands from this repository. The first command only previews changes:

```bash
python3 scripts/install_kit.py --target /path/to/project --profile observe --language en --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /path/to/project --profile observe --language en --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /path/to/project --verify
```

After an observation period, switch profiles by uninstalling the current profile and installing another. For `balanced` or `hardened`, create the required neutral queue label before enabling the workflow:

```bash
gh label create needs-human-review --repo OWNER/REPOSITORY --color D4C5F9 --description "Neutral queue for maintainer review"
```

The upstream triage Action logs a warning rather than failing if the label is absent, so this prerequisite is intentional and testable.

## Roll back

```bash
python3 scripts/install_kit.py --target /path/to/project --uninstall
```

Uninstall removes only files that this installer created. It refuses to proceed if an installed file was modified, so local edits cannot be silently lost. Commit the installation separately to make repository-level rollback and review straightforward.

## Trust boundary

The installer makes local files only; it does not call GitHub APIs, create labels, change repository settings, or commit code. Workflow dependencies are pinned to immutable commits and recorded in [`pins.json`](../../pins.json). Read the [assurance case](../../docs/KIT_ASSURANCE.md) before treating the kit as a production control.

This is an engineering-tested baseline, not a security certification or a substitute for GitHub's native repository controls.
