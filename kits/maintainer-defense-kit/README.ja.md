# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

元に戻せるリポジトリ方針と読み取り専用 workflow を導入します。既定は preview です。Apply は異なる既存内容を上書きせず、所有権と hash を記録し、危険な path と symlink を拒否し、変更済みファイルを削除しません。

## Profile

| Profile | 実行時の効果 |
| --- | --- |
| `observe` | PR の読み取り専用分析と job summary。コントリビューターに見える操作なし |
| `balanced` | 同じ signal contract と失敗可能な status check。comment、label、close、lock なし |
| `hardened` | `balanced` に dependency review と GitHub Actions 静的解析を追加 |

各 profile は bug form、PR template、policy、playbook、任意の手動 label 仕様、adoption record を English、Vietnamese、Japanese のいずれかで導入します。

## Preview、apply、verify

```bash
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /path/to/project --verify
```

インストーラーはローカルファイルだけを書き込み、GitHub API、label 作成、required check 設定、commit、push は行いません。オンライン設定は repository owner が別途行います。

## ロールバック

```bash
python3 scripts/install_kit.py --target /path/to/project --uninstall
```

Uninstall は変更されていない installer-owned file だけを削除し、編集済みなら停止します。`observe` から開始し、代表標本、owner の承認、異議申立て、検証済み rollback が揃ってから status gate に進んでください。[安全上の制約](../../docs/ja/SAFETY.md)と[プレイブック](../../docs/ja/PLAYBOOK.md)を参照してください。
