# Maintainer Defense Kit

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

AI作成の判定を主張せず、メンテナーのレビュー負荷を減らす、導入・ロールバック可能なベースラインです。インストーラーは既定でdry-runとなり、内容が異なる既存ファイルを上書きせず、各ファイルのハッシュを記録して検証と安全な削除を行えます。

## プロファイル

| プロファイル | トークン権限 | 効果 |
| --- | --- | --- |
| `observe`（既定） | 読み取り専用 | job summaryのみ。シグナルと誤検知を測定 |
| `balanced` | PR書き込み | `needs-human-review`のみ追加。コメント、close、lockなし |
| `hardened` | ジョブごと | `balanced`に依存関係レビューとワークフロー静的解析を追加 |

すべてのプロファイルは、`en`、`vi`、`ja`のIssueフォーム、PRテンプレート、ポリシー、プレイブック、ラベル仕様、導入記録をインストールします。

## 安全な導入

このリポジトリから実行します。最初のコマンドはプレビューのみです。

```bash
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /path/to/project --verify
```

`balanced`または`hardened`を使う前に、中立的なキュー用ラベルを作成します。

```bash
gh label create needs-human-review --repo OWNER/REPOSITORY --color D4C5F9 --description "メンテナー確認用の中立的なキュー"
```

## ロールバック

```bash
python3 scripts/install_kit.py --target /path/to/project --uninstall
```

アンインストールはインストーラーが作成したファイルだけを削除し、変更済みなら停止します。インストーラーはGitHub APIの呼び出し、ラベル作成、設定変更、コミットを行いません。Actionはcommit SHAで固定され、[`pins.json`](../../pins.json)で追跡されます。

これは技術的にテストされたベースラインであり、セキュリティ認証ではありません。[保証ケース](../../docs/ja/KIT_ASSURANCE.md)に保証済みの範囲と実地証拠がない範囲を記載しています。
