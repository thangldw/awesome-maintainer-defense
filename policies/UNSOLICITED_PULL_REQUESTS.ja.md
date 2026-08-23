# 依頼されていない pull request

承認済み issue または maintainer request がない大きな変更は、実装前に相談してください。短い proposal に、問題、範囲、対象 file、security/compatibility への影響、検証方法を記載します。

自動 agent は、責任を持つ human reviewer と maintainer の明示的な authorization なしに、依頼されていない repository change を作成・提出してはいけません。ローカル patch の生成は、pull request 作成、branch push、setting change の許可ではありません。

独立して検証可能な小さな typo 修正は直接受理される場合があります。Security report は private vulnerability channel へ送ってください。Maintainer は重複、範囲外、大量生成、policy 違反、保守不能な提出を詳細レビューなしで終了できます。

承認範囲は周辺 refactoring の許可ではありません。実装中に実質的に異なる変更が必要になった場合は停止し、新しい判断を求めてください。
