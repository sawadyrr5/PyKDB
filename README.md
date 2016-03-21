# PyKDB
k-dbからのデータ取得スクリプト

## メソッド
```py3:PyKDB
hist(symbol, interval=None, start=None, end=None)
```
**symbol** : *string*
取得したい銘柄コードまたは指数・統計コードを指定します。

**interval** : *d, a, m5, m*
取得したいデータ頻度をd(日次), a(前場、後場、夜間), m5(5分足), m(分足)のいずれかで指定します。先物、個別株はすべて取得可能ですが、指数は分足以外、統計は日足のみ取得可能です。

|            | d | a | m5 | m |
|------------|---|---|----|---|
| futures    | o | o | o  | o |
| indices    | o | o | o  | x |
| stocks     | o | o | o  | o |
| statistics | o | x | x  | x |

**start** : *datetime.datetime*
取得開始日を指定します。intervalがm5, mの場合は取得日として扱われます。

**end** : *datetime.datetime*
取得終了日を指定します。intervalがm5, mの場合は無視されます。