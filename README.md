# PyKDB
k-dbからのデータ取得スクリプト

# はじめに
k-dbから国内先物、指数、個別株、市場統計の時系列データを取得するクラスを書きました。pandas_datareaderだと米国株のデータしか取れないもんで。
[sawadyrr5/PyKDB: k-dbからのデータ取得スクリプト](https://github.com/sawadyrr5/PyKDB)

# 更新履歴
2016/5/12 k-db.comのサイト構成更新に対応しました。先物、指数、個別株、統計ごとにクラス分けしました。内部処理を整理しました。

# 使用方法
まずインスタンス化します。

```py3:PyKDB
from PyKDB import Futures, Indices, Stocks, Statistics

myFutures = Futures() # 先物データ取得用
myIndices = Indices() # 指数データ取得用
myStocks = Stocks() # 個別株データ取得用
myStatistics = Statistics() # 統計データ取得用
```

## Futuresクラス
### プロパティ
```py3:
# 銘柄コードのリストを返す
Futures.symbols

# {銘柄コード: 銘柄名称}の辞書を返す
Futures.names

# {銘柄コード: 限月}の辞書を返す
Futures.contracts
```

### メソッド
#### 指定銘柄の時系列データ取得
```py3:
Futures.price(date_from, date_to, symbol, freq)
```
date_from, date_to 期間を指定(datetime型)
symbol 銘柄コードを指定
freq 頻度を指定('1d', '4h', '1h', '30m', '15m', '5m')

#### 全銘柄の時系列データ取得
```py3:
Futures.price_all(date_from, date_to, session)
```
date_from, date_to 期間を指定(datetime型)
session セッションを指定(None=全部, 'e'=夜間) 省略時は全部


## Indicesクラス
### プロパティ
```py3:
# 銘柄コードのリストを返す
Indices.symbols

# {銘柄コード: 銘柄名称}の辞書を返す
Indices.names
```

### メソッド
#### 指定銘柄の時系列データ取得
```py3:
Indices.price(date_from, date_to, symbol, freq)
```
date_from, date_to 期間を指定(datetime型)
symbol 銘柄コードを指定
freq 頻度を指定('1d', '4h', '1h', '30m', '15m', '5m')

#### 全銘柄の時系列データ取得
```py3:
Indices.price_all(date_from, date_to, session)
```
date_from, date_to 期間を指定(datetime型)
session セッションを指定(None=全部, 'a'=前場, 'b'=後場) 省略時は全部


## Stocksクラス
### プロパティ
```py3:
# 銘柄コードのリストを返す
Stocks.symbols

# {銘柄コード: 銘柄名称}の辞書を返す
Stocks.names
```

### メソッド
#### 指定銘柄の時系列データ取得
```py3:
Stocks.price(date_from, date_to, symbol, freq)
```
date_from, date_to 期間を指定(datetime.datetime型)
symbol 銘柄コードを指定
freq 頻度を指定('1d', '4h', '1h', '30m', '15m', '5m')

#### 全銘柄の時系列データ取得
```py3:
Stocks.price_all(date_from, date_to, session)
```
date_from, date_to 期間を指定(datetime.datetime型)
session セッションを指定(None=全部, 'a'=前場, 'b'=後場) 省略時は全部


## Statisticsクラス
### プロパティ
```py3:
# 銘柄コードのリストを返す
Statistics.symbols

# {銘柄コード: 銘柄名称}の辞書を返す
Statistics.names
```

### メソッド
#### 指定銘柄の時系列データ取得
```py3:
Statistics.price(date_from, date_to, symbol, freq)
```
date_from, date_to 期間を指定(datetime.datetime型)
symbol 銘柄コードを指定
freq 頻度を指定('1d')

#### 全銘柄の時系列データ取得
```py3:
Statistics.price_all(date_from, date_to, session)
```
date_from, date_to 期間を指定(datetime.datetime型)
session セッションを指定(None=全部) 省略時は全部
