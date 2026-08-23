# はじめに

Python 3.10 以降と、監査権限のあるリポジトリのチェックアウトが必要です。実行時依存関係、GitHub トークン、ネットワーク接続は不要です。

## ソースから実行

```bash
git clone https://github.com/thangldw/awesome-maintainer-defense.git
cd awesome-maintainer-defense
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

監査ツールはローカルの方針ファイル、ワークフロー、Git メタデータを読むだけで、コードの実行や対象への書き込みは行いません。

## pipx でインストール

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit /path/to/repository
```

## 結果の確認

各所見には severity、安定した rule ID、場所、観測証拠、脅威シナリオ、安全な修復案が含まれます。所見を受け入れる前に、対象ファイルが有効か、チェックアウト外の統制で補われていないか確認してください。

```bash
maintainer-defense audit . --format json --output maintainer-defense.json
maintainer-defense audit . --format sarif --output maintainer-defense.sarif
maintainer-defense audit . --fail-on high
```

`--fail-on` は有効な所見がしきい値以上なら終了コード 2、入力または設定エラーなら 1 を返します。

## レビュー用パッチ

```bash
maintainer-defense fix . --output recommended.patch
git apply --check recommended.patch
```

パッチは自動適用されません。リポジトリの通常の承認と CI を通してください。

次に [安全性](SAFETY.md)、[プレイブック](PLAYBOOK.md)、英語の [CLI 正本](../AUDITOR.md)を確認してください。
