# Maintainer Defense Kit — 保証ケース

**状態:** 技術的に検証されたベースライン。セキュリティ認証ではなく、代表的な公開リポジトリ群での実地検証は未完了です。

ここでの「Defense」はレビューコストと危険な自動化経路を減らすことであり、人間またはAIの作成を判定することではありません。

## テストで保証していること

- `observe`は`pull_request`、読み取り専用トークン、PRコードのcheckoutなしで、コメント、ラベル、close、lockを行いません。
- インストーラーは既定でdry-run、書き込み前に競合を検査し、上書きせず、SHA-256と所有情報をmanifestに保存します。
- アンインストールはインストーラー作成ファイルだけを削除し、変更済みなら停止します。リポジトリ外のパス、悪意あるmanifest、symlinkは拒否します。
- `balanced`と`hardened`が行える効果は、名前付きstatus checkの失敗だけです。コメント、ラベル、close、lock、merge、PRコード実行はありません。
- username、アカウント年齢、fork頻度、公開・完成プロフィール、全体のmerge履歴、emoji、commit author同一性などのproxyを明示的に無効化しています。
- すべてのActionは完全なcommit SHAで固定され、`pins.json`に記録され、upstream tagとverified commit状態を定期検証します。
- 3プロファイル×3言語に加え、競合、ロールバック、変更ファイル、既存ファイル、悪意あるmanifest、symlinkをend-to-endでテストします。

## 2回目の監査で修正した問題

以前のワークフローはコメントを繰り返す可能性があり、ラベル付けが警告だけで失敗し、upstream既定値にはquality-firstに合わないidentity/history proxyが含まれていました。最初のlabel-only修正も`pull_request_target`を使い、zizmorが特権的trust boundaryとして正しく拒否しました。最終設計は読み取り専用`pull_request`でコメント・ラベルを行わず、proxyを無効化し、制御された出力をstatus gateに変換します。Issueフォームも未宣言ラベルに依存しません。

## 保証していないこと

- AI作成、意図、コントリビューター品質を確実に証明する検知機能はありません。
- precision、recall、誤検知、短縮時間、参加断念率を測る、プライバシーレビュー済み実地データセットはまだありません。
- upstream commitのverified状態は、第三者Actionコードの完全監査を意味しません。
- GitHub設定、ruleset、ラベルの存在、private vulnerability reportingはインストーラーの管理外です。
- ベトナム語・日本語は構造テスト済みですが、母語のセキュリティ・法務専門家による独立レビューは未実施です。
- コンプライアンス制御、法的助言、SLA、保証ではありません。

## production受入条件

ネイティブ制御の確認、owner・レビューSLA・異議申立て経路・緊急停止責任者の指定、baseline記録、status gateの失敗・回復テスト、人による誤検知レビュー、verification/CI通過が完了するまで`observe`から移行しないでください。

正確な結論は、**導入、権限、ロールバック、pinning、localizationはテスト済みですが、実環境でのモデレーション効果は未保証**です。

インストーラーはPython 3.10以降をサポートし、CIはLinux上のPython 3.10、3.12、3.14とmacOS上のPython 3.12を検証します。シグナル、閾値、無効化したproxyは[`PROFILE_SIGNALS.md`](../PROFILE_SIGNALS.md)に公開しています。機密情報を除いた集計結果は[field-report issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=field-report.yml)から共有できます。リポジトリ名、コントリビューターの識別情報、生のPRデータは不要です。
