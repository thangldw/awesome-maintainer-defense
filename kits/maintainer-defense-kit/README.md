# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

The kit installs reversible repository policy and read-only workflow controls. Preview is the default. Apply never overwrites different content, records file ownership and hashes, rejects unsafe paths and symlinks, and refuses to remove modified files.

## Profiles

| Profile | Runtime effect |
| --- | --- |
| `observe` | Read-only pull-request analysis and job summary; no contributor-visible action |
| `balanced` | `observe` signal contract plus a named failing status check; no comment, label, close, or lock |
| `hardened` | `balanced` plus dependency review and GitHub Actions static analysis |

Each profile installs a structured bug form, pull-request template, contribution policies, playbook, optional manual label specification, and adoption record in English, Vietnamese, or Japanese.

## Preview, apply, verify

```bash
python3 scripts/install_kit.py --target /path/to/project --profile observe --language en --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /path/to/project --profile observe --language en --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /path/to/project --verify
```

Review every preview. The installer writes local files only; it does not call GitHub, create labels, set required checks, commit, or push. Repository owners configure any live rules separately.

## Change profile or roll back

Uninstall the current profile before installing another:

```bash
python3 scripts/install_kit.py --target /path/to/project --uninstall
```

Uninstall removes only unchanged installer-owned files. A modified owned file stops the operation so user work is not lost. Commit adoption as an isolated change for repository-level review and rollback.

Start with `observe`. Move to a contributor-visible status gate only after representative sampling, owner authorization, an appeal route, and a tested rollback. Review the [assurance boundary](../../docs/KIT_ASSURANCE.md) and [playbook](../../docs/PLAYBOOK.md).
