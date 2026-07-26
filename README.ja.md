# Awesome Maintainer Defense — 日本語

[3言語ドキュメント](README.md) · [Tiếng Việt](README.vi.md)

Maintainer Defense Kit は、repository policy と GitHub Actions の信頼境界を監査するオフライン Python CLI です。network や GitHub token は不要です。`fix` はレビュー用 unified diff を出力するだけで、ファイル編集、設定変更、commit、push を行いません。

```bash
python3 scripts/build_standalone.py
python3 generated/maintainer-defense-kit.py audit .
python3 generated/maintainer-defense-kit.py fix . --output recommended.patch
```

所見は人が確認するための証拠であり、作者、意図、安全性の結論ではありません。`kits/**/.github/` 内の workflow は製品サンプルであり、この repository では実行されません。

## レビュー済みカタログ

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

正規リリース: `v1.0.0`。[MIT License](LICENSE)。
