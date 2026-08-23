# パイロットと同意

パイロットは、メンテナーまたは明示的に権限を与えられた担当者が、公開リポジトリ、full commit SHA、レビュー担当者の役割、公開範囲を[パイロット issue form](https://github.com/thangldw/awesome-maintainer-defense/issues/new?template=auditor-pilot.yml)で指定した場合にのみ開始します。公開 URL や無回答は公開への同意ではありません。

監査は固定した revision に対してオフラインで行い、コード実行や対象変更はしません。担当者は各所見を true positive、false positive、not applicable、unresolved に分類し、raw report と suppression 適用後 report を分離して保持します。

参加者が選んだ公開範囲の情報だけを公開し、secret、個人情報、非公開内容を除去します。プロジェクト所有者自身による dogfood は、独立評価でも代表サンプルでもないと明記します。再現性は示せますが、実環境での精度は示せません。

[同意から証拠までの図](../diagrams/consent-to-evidence.html)は同じ流れを示します。権限と同意の後に、固定 checkout のオフライン監査を行い、unresolved を含む人のラベルを保持します。公開範囲の選択によって、再現可能な bundle と公開に含められるデータを制限します。

リポジトリの score、ranking、コントリビューター profile は作りません。完全な契約は英語の [pilot program](../AUDITOR_PILOT_PROGRAM.md)、公開 bundle は [pilot evidence](../../pilots/README.md)を参照してください。
