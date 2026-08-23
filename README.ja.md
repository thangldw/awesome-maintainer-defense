# Awesome Maintainer Defense

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

Awesome Maintainer Defense は、オフラインかつ読み取り専用のリポジトリ監査ツールと、元に戻せるメンテナー向け防御策です。トークンやネットワーク接続なしで、ローカルのガバナンス文書と GitHub Actions の信頼境界を確認します。リポジトリのコードは実行せず、GitHub のオンライン設定も取得せず、コントリビューションの作者も判定しません。

## クイックスタート

Python 3.10 以降が必要です。

```bash
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

所見は人が調査するための手掛かりであり、侵害、悪意、作者を証明するものではありません。

## 監査対象

- セキュリティ方針、所有境界、構造化された受付、依存関係更新、ブランチ保護方針のローカル証拠。
- 過大なトークン権限、可変な Action 参照、PR 入力の特権実行、シェルへの直接展開、危険なワークフロー間成果物。
- 破壊的なモデレーション、個人属性や履歴に基づく代理指標、異議申立て経路の欠如。

## 所見からレビュー済みパッチへ

`fix` は unified diff を生成するだけで、リポジトリを編集しません。

```bash
python3 dist/maintainer-defense-kit.py fix . --output recommended.patch
git apply --check recommended.patch
```

証拠、影響、CI をメンテナーが確認した後にのみ適用してください。

## 証拠の限界

テストで確認しているのは、決定的な検出、JSON/SARIF、パッチのみの修復、インストール競合処理、同梱ワークフローの不変条件です。代表的な実リポジトリでの精度、オンライン設定の網羅、作者や意図の判定は主張しません。

## インストール

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit .
```

チェックサムと配布チャネルは英語版の [Distribution](docs/DISTRIBUTION.md) を参照してください。

## ドキュメント

- [はじめに](docs/ja/GETTING_STARTED.md)
- [安全性と制約](docs/ja/SAFETY.md)
- [運用プレイブック](docs/ja/PLAYBOOK.md)
- [パイロットと同意](docs/ja/PILOTS.md)
- [日本語ドキュメント](docs/ja/README.md)

## カタログ

[レビュー済みデータから生成されるカタログ](docs/CATALOG.md)は補助資料であり、認証や推奨ではありません。権限、データ境界、最大の影響、保守状況、ライセンスを採用前に確認してください。

## 規約

英語の [Security](SECURITY.md)、[Support](SUPPORT.md)、[Privacy](PRIVACY.md)、[Terms](TERMS.md)、[License](LICENSE) が正本です。日本語の説明は利用支援であり、別の条件を作るものではありません。
