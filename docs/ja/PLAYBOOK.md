# メンテナー防御プレイブック

## 1. トリアージ

元の URL、revision、workflow run、時刻、機密情報を除いた証拠を保存します。セキュリティ報告は公開受付から分離します。注意力の消耗、危険な workflow、credential 漏えい、破壊的 automation、governance 不備のどれかを先に特定し、属性や文体から作者や意図を推定しません。

## 2. レビュー

所見を有効なファイルとリポジトリ文脈に照合します。外部 ruleset、組織方針、設定によって適用可能性が変わらないか確認します。Workflow では、信頼できない入力から実行点または権限までを追跡します。

## 3. 承認

担当 owner を決め、統制、権限、データ送信先、コントリビューターへの影響、例外、異議申立て、review date、正確な rollback を記録します。影響の大きい統制には repository owner の承認が必要で、監査の提案自体は承認ではありません。

## 4. 展開

ローカル監査と `observe` profile から始めます。代表的なテストを行い、flag されたものとされなかったものを両方標本確認します。中立的な routing と status check を優先します。Close、lock、block、delete、interaction limit は、測定された必要性、人のレビュー、期限がある場合だけ使います。

## 5. インシデントと復旧

Incident owner を割り当て、不確かな automation を止め、secret を公開ログに入れず証拠を保全します。信頼できない実行を隔離し、credential を失効し、疑わしい artifact を無効化します。その後 rollback し、正当な item を再開し、期限どおり制限を解除して、非難を目的としない記録を残します。

各統制の adoption record には owner、日付、profile、signal window、findings、false positives、appeals、threshold decision、rollback trigger、review date を含めます。Owner、review date、検証済み rollback がない統制は observe に戻します。
