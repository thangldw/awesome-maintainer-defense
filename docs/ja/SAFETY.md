# 安全性と制約

監査ツールはローカルチェックアウトを静的に確認します。GitHub への接続、リポジトリコードの実行、secret の読み取り、ファイル・Git 状態・設定・ブランチ・pull request の変更は行いません。`fix` は常に人が確認する unified diff だけを出力します。

所見は悪用可能性、侵害、作者、意図、コントリビューターの品質を証明しません。Severity は検出パターンが持ち得る権限または影響を表し、適用可能性と外部統制は人が確認します。

PR 由来の信頼できないコードを、secret、OIDC、write token を持つ job で実行しないでください。既定権限を空にし、Action を full commit SHA で固定し、PR 成果物を信頼できないデータとして扱います。個人属性、アカウント年齢、履歴を危険性の証拠にしません。

オンラインの ruleset、branch protection、組織方針、GitHub App、role、label、private reporting 設定、外部サービスの挙動は監査範囲外です。所見がゼロでも、リポジトリ全体の安全性は保証されません。

[英語版](../../SECURITY.md)の security、privacy、support、terms、license が正本です。
