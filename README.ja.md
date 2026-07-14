# Awesome Maintainer Defense

> オープンソースメンテナー向けの防御スタック、ポリシー、すぐに使えるワークフロー集。

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Quality](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml/badge.svg)](https://github.com/thangldw/awesome-maintainer-defense/actions/workflows/quality.yml)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

オープンソースは開かれているべきですが、メンテナーがスパム、嫌がらせ、危険なワークフロー、低品質な自動コントリビューション、ノイズの多い脆弱性報告を無制限に引き受ける必要はありません。このリポジトリは、人によるレビューと正当な初参加者の機会を守りながら、実用的な防御策をまとめます。

本プロジェクトは**不正利用への対策であり、反AIではありません**。AI生成を完全に判定できるという主張よりも、透明なシグナル、取り消し可能な操作、最小権限、明確な異議申立て経路を優先します。

## Maintainer Defense Kitの導入

読み取り専用の日本語版をプレビューします。`--apply`を付けるまでファイルは書き込まれません。

```bash
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY
python3 scripts/install_kit.py --target /path/to/project --profile observe --language ja --repo OWNER/REPOSITORY --apply
python3 scripts/install_kit.py --target /path/to/project --verify
```

[導入可能なKit](kits/maintainer-defense-kit/README.ja.md)には`observe`、`balanced`、`hardened`、安全なアンインストール、英語・ベトナム語・日本語の完全なテンプレート、ポリシー、プレイブックが含まれます。[保証ケース](docs/ja/KIT_ASSURANCE.md)は、テスト済みの技術的保証と、実地データがまだない有効性を区別します。

## クイックスタート

| 状況 | 最初の対応 | 次に検討すること |
| --- | --- | --- |
| 通常運用で時間が限られる | 読み取り専用の`observe`を導入 | `balanced`の前に誤検知を測定 |
| Issue/PRが急増 | 自動マージを止め、一時的なinteraction limitを設定 | 所有者と期限を決めたうえでlockdownを検討 |
| 低品質PRが繰り返される | 自動クローズ前に人間レビュー用ラベルを付与 | dry-runで評価し、ポリシーを公開 |
| 嫌がらせ・協調攻撃 | 証拠を保存し、交流を制限 | 不正利用を報告し、内容を拡散しない |
| 不審なワークフロー変更 | 書き込みトークン付きで未信頼コードを実行しない | zizmor、ActionのSHA固定、権限縮小 |

導入前に[優先すべきGitHubネイティブ制御](docs/NATIVE_CONTROLS.md)を確認し、その後[リソース監査](docs/RESOURCE_AUDIT.md)、[評価方法](docs/EVALUATION.md)、[脅威モデル](docs/THREAT_MODEL.md)、[日本語プレイブック](docs/ja/PLAYBOOK.md)を確認してください。

## 原則

1. **作成者ではなく品質を評価する。** 再現性、範囲、テスト、レビューへの応答を確認します。
2. **執行前にレビューする。** dry-runまたはreport-onlyから始め、誤検知を測定します。
3. **最小権限。** 特権ワークフローで未信頼のPRコードを実行しません。
4. **取り消し可能を既定にする。** close、lock、blockより先にラベルとキューを使います。
5. **ルールを公開する。** 証拠基準、ポリシー、異議申立て経路を明確にします。
6. **メンテナーの注意力を守る。** レビューコストが価値を上回る未依頼作業は拒否できます。

## リソース

⭐は推奨される出発点であり、有料掲載ではありません。表は[`catalog.json`](catalog.json)から生成され、翻訳は[`i18n/ja.json`](i18n/ja.json)で管理されます。

<!-- catalog:start -->

### 不正利用の検知・モデレーション

スパム、嫌がらせ、低品質な自動コントリビューションを検知し、ラベル付け、隔離、対応します。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [Niubi Guard](https://github.com/Albert-Weasker/niubi_guard) ⭐ | ツール | Apache-2.0 | スパム、嫌がらせ、協調攻撃に対応するリポジトリ不正利用の検知・対処システム。 |
| [Anti Slop](https://github.com/peakoss/anti-slop) ⭐ | GitHub Action | AGPL-3.0 | 低品質またはAI-slopのプルリクエストを検知し、必要に応じて閉じる設定可能なGitHub Action。 |
| [GitHub AI Moderator](https://github.com/github/ai-moderator) | GitHub Action | MIT | モデルを使い、スパム、リンクスパム、AI生成と推定した内容にラベルを付けるAction。 |
| [AI Community Moderator](https://github.com/benbalter/ai-community-moderator) | GitHub Action | MIT | プロジェクトのコントリビューションガイドと行動規範に基づいてコミュニティ交流をモデレート。 |
| [AI Assessment Comment Labeler](https://github.com/github/ai-assessment-comment-labeler) | GitHub Action | MIT | Issue受付時にAI評価を取得し、設定されたラベルを適用するAction。 |

### コントリビューターの信頼・参加制御

明示的な推薦や貢献履歴を利用し、プロジェクトを全面的に閉じることなく参加を制御します。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [Fossier](https://github.com/PThorpe92/fossier) | ツール | MIT | 未依頼のプルリクエストスパムを減らすVouch互換のワークフローとCLI。 |
| [Vouch](https://github.com/mitchellh/vouch) ⭐ | ツール | MIT | 明示的な推薦を受けた人だけが参加できるコミュニティ信頼管理。 |
| [Good Egg](https://github.com/2ndSetAI/good-egg) | GitHub Action | MIT | GitHub全体の貢献履歴を用いてプルリクエスト作成者をスコアリング。 |

### 受付・トリアージ

構造化された受付、ラベル、ライフサイクル自動化、緊急ロックダウンによってレビュー負荷を減らします。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [Labeler](https://github.com/actions/labeler) | GitHub Action | MIT | 変更ファイルやブランチパターンに基づきプルリクエストへラベルを付ける公式Action。 |
| [Stale](https://github.com/actions/stale) | GitHub Action | MIT | 長期間動きのないIssueやプルリクエストをマークし、任意で閉じる公式Action。 |
| [Lock Threads](https://github.com/dessant/lock-threads) | GitHub Action | MIT | 設定期間後に、閉じたIssue、プルリクエスト、Discussionをロック。 |
| [Repo Lockdown](https://github.com/dessant/repo-lockdown) ⭐ | GitHub Action | MIT | 新しいIssueやプルリクエストを即時に閉じてロックする緊急用Action。 |
| [Issue Metrics](https://github.com/github-community-projects/issue-metrics) | GitHub Action | MIT | Issue、プルリクエスト、Discussionの応答時間を計測してMarkdownレポートを生成。 |

### リポジトリ統制・アクセス管理

複数プロジェクトのセキュリティポリシー、ブランチ保護、リポジトリ設定を一貫させます。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [OpenSSF Allstar](https://github.com/ossf/allstar) ⭐ | GitHub App | Apache-2.0 | GitHub Organization全体のセキュリティポリシーを継続的に検査・適用。 |
| [Safe Settings](https://github.com/github-community-projects/safe-settings) ⭐ | GitHub App | ISC | リポジトリ設定、ブランチ保護、チームを一元管理し、プルリクエストではdry-runを実施。 |
| [Repository Settings App](https://github.com/repository-settings/app) | GitHub App | ISC | バージョン管理された`.github/settings.yml`からリポジトリ設定を同期。 |

### ワークフロー・サプライチェーン防御

CI、依存関係、シークレット、マージ経路を悪意ある、または侵害されたコントリビューションから守ります。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [Harden-Runner](https://github.com/step-security/harden-runner) ⭐ | GitHub Action | Apache-2.0 | GitHub-hosted runner上のネットワーク送信、ファイル整合性、プロセス活動を監視。 |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) ⭐ | ツール | Apache-2.0 | オープンソースプロジェクトと依存関係のセキュリティ状態を自動評価。 |
| [zizmor](https://github.com/zizmorcore/zizmor) ⭐ | ツール | MIT | GitHub Actionsワークフローのセキュリティと正当性の問題を静的解析。 |
| [pinact](https://github.com/suzuki-shunsuke/pinact) | ツール | MIT | GitHub Actionと再利用可能ワークフローを不変のコミットハッシュに固定。 |
| [Dependency Review Action](https://github.com/actions/dependency-review-action) ⭐ | GitHub Action | MIT | 脆弱な依存関係や許可されていないライセンスを追加するプルリクエストをブロック。 |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | ツール | AGPL-3.0 | 漏えいした認証情報を発見・検証し、インシデント化する前に対処を支援。 |
| [PRevent](https://github.com/apiiro/PRevent) | GitHub App | MIT | 悪意あるコードを示す可能性のある不審なプルリクエスト変更を検知。 |
| [OSV-Scanner](https://github.com/google/osv-scanner) ⭐ | ツール | Apache-2.0 | ロックファイル、SBOM、ソース成果物をOSV脆弱性データベースでスキャン。 |
| [Gitleaks](https://github.com/gitleaks/gitleaks) ⭐ | ツール | MIT | Git履歴、ディレクトリ、ファイル、標準入力からシークレットを検知。 |

### ポリシー・プレイブック

問題が起きる前に期待事項を定め、発生時に一貫して対応します。

| リソース | 種別 | ライセンス | 主な価値 |
| --- | --- | --- | --- |
| [Open Source AI Contribution Policies](https://github.com/melissawm/open-source-ai-contribution-policies) ⭐ | リスト | CC0-1.0 | 各オープンソースプロジェクトのAI生成コントリビューション方針を比較するカタログ。 |
| [OpenSSF AI-Slop Best-Practices Work Item](https://github.com/ossf/wg-vulnerability-disclosures/issues/178) | ワーキンググループ | N/A | 低品質なAIセキュリティ報告とコントリビューションの実務指針を検討中の作業項目。完成した標準ではありません。 |

<!-- catalog:end -->

## すぐに使える資料

- [導入可能なMaintainer Defense Kit](kits/maintainer-defense-kit/README.ja.md) — テスト済みプロファイル、manifest検証、安全なロールバック、3言語の完全な導入資産。
- [Balanced starter kit](kits/balanced) — PRテンプレート、Issueフォーム、review-firstトリアージ。
- [Workflow-hardening starter kit](kits/workflow-hardening) — コミットSHA固定済みの依存関係レビューとGitHub Actions解析。
- [AI支援コントリビューションポリシー](policies/AI_CONTRIBUTIONS.ja.md)。
- [未依頼プルリクエストポリシー](policies/UNSOLICITED_PULL_REQUESTS.ja.md)。
- [日本語運用プレイブック](docs/ja/PLAYBOOK.md)。
- [成熟度モデル](docs/MATURITY_MODEL.md)と[評価方法](docs/EVALUATION.md)。
- [Kit保証ケース](docs/ja/KIT_ASSURANCE.md)と[ネイティブ制御ベースライン](docs/NATIVE_CONTROLS.md)。
- [監査ログ](docs/AUDIT_LOG.md) — 重要な修正と削除したエントリ。

テンプレートは出発点であり、法的助言ではありません。執行モードを有効にする前に、非重要リポジトリでテストし、権限とデータフローを確認してください。

## ライセンス

本プロジェクトは[MIT License](LICENSE)で提供されます。
