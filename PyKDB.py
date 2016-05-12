# -*- coding: utf-8 -*-
import urllib.request
import lxml.html
from datetime import datetime
import pandas as pd


# 先物,指数,個別株,統計の基底クラス
class __Historical:
    _master_url = str()
    _freq = tuple()
    _category = str()
    _session = tuple()
    _xpath = dict()
    _all_index_col = str()

    _base_url = 'http://k-db.com/{category}'
    _base_url_single = 'http://k-db.com/{category}/{symbol}/{freq}'
    _base_url_single_dl = 'http://k-db.com/{category}/{symbol}/{freq}/{date}?download=csv'
    _base_url_all = 'http://k-db.com/{category}/{date}{session}?download=csv'
    _freq_format = {'1d': '%Y', '4h': '%Y', '1h': '%Y%m', '30m': '%Y%m', '15m': '%Y%m%d', '5m': '%Y%m%d'}

    def __init__(self):
        # カテゴリーの展開
        param = dict(category=self._category)
        self._base_url = self._base_url.format(**param)
        root = _get_root(self._base_url)

        # ドキュメントルートのparse用
        def parse_root(xpath):
            return [e.text for e in root.xpath(xpath)]

        # コードのリスト作成
        self.symbols = [symbol.split('/')[-1] for symbol in root.xpath(self._xpath['symbols'])]

        # コード名称の辞書作成
        self.names = dict(zip(self.symbols, parse_root(self._xpath['names'])))

        # 先物限月の辞書作成, エラーの場合無視
        try:
            self.contracts = dict(zip(self.symbols, parse_root(self._xpath['contracts'])))
        except KeyError:
            pass

    def price(self, date_from: datetime, date_to: datetime, symbol: str, freq: str) -> pd.DataFrame:
        """
        Download historical price of specified symbol.
        :param date_from:
        :param date_to:
        :param symbol:
            Specify symbol.
        :param freq:
            Specify frequency.
        :return: pandas.DataFrame
        """
        # symbolが存在しなかった場合は中断
        if symbol not in self.symbols:
            raise KDBError("specified symbol is not found in this category.")

        # freqがリストに無い場合は中断
        if freq not in self._freq:
            raise KDBError("specified freq is not available.")

        # 取得可能なdate_rangeを抽出
        params = dict(category=self._category, symbol=symbol, freq=freq)
        url = self._base_url_single.format(**params)
        root = _get_root(url)
        date_range_web = set([date.split('/')[-1] for date in root.xpath(self._xpath['date_range'])])
        date_range_f = _formatted_date_range(date_from, date_to, self._freq_format[freq])
        date_range = date_range_web.intersection(date_range_f)

        # 期間がとれない場合は処理中断
        if not date_range:
            return pd.DataFrame()

        params = [dict(category=self._category, date=date, symbol=symbol, freq=freq) for date in date_range]
        urls = [self._base_url_single_dl.format(**param) for param in params]
        dfs = _fetch_csv(urls)

        df = pd.concat(dfs)
        df['日付'] = pd.to_datetime(df['日付'])

        if freq in ('1d', '4h'):
            index_level = ['日付']
            df = df.set_index(keys=index_level)
            df = df.ix[min(df[df.index >= date_from].index):max(df[df.index <= date_to].index)]
        else:
            index_level = ['日付', '時刻']
            df = df.set_index(keys=index_level)

        df = df.sort_index(level=index_level, ascending=True)
        return df

    def price_all(self, date_from: datetime, date_to: datetime, session=None) -> pd.DataFrame:
        """
        Download historical price of all symbols.
        :param date_from:
        :param date_to:
        :param session:
            Specify session.
        :return: pandas.DataFrame
        """
        # sessionが指定されなかった場合または適合しない場合は''とする
        if session in self._session:
            session = '/' + str(session)
        else:
            session = ''

        date_range = _formatted_date_range(date_from, date_to, '%Y-%m-%d')
        params = [dict(category=self._category, date=date, session=session) for date in date_range]

        urls = [self._base_url_all.format(**param) for param in params]
        dfs = _fetch_csv(urls)

        # 取得結果がすべて空だった場合は空DataFrameを返して終了
        if all([df.empty for df in dfs]):
            return pd.DataFrame()

        # DataFrameに日付列を追加する
        def add_date(df: pd.DataFrame, date: datetime):
            df['日付'] = date
            return df

        dfs = [add_date(df, date) for df, date in zip(dfs, date_range) if not df.empty]

        df = pd.concat(dfs)
        df = df.set_index(keys=['日付', self._all_index_col]).sort_index()
        return df


def _get_root(url):
    """
    ドキュメントルートを取得する(parse用)
    """
    response = urllib.request.urlopen(url).read().decode('utf-8-sig')
    return lxml.html.fromstring(response)


def _formatted_date_range(date_from, date_to, date_format):
    """
    ドキュメントルートを取得する(parse用)
    """
    return set([datetime.strftime(date, date_format) for date in pd.date_range(date_from, date_to, freq='D')])


def _fetch_csv(urls):
    """
    CSVを取得する
    """
    if not urls:
        return []

    def read_csv(url):
        try:
            df = pd.read_csv(urllib.request.urlopen(url), encoding='Shift_JIS')
        except ValueError or urllib.error.HTTPError:
            df = pd.DataFrame()
        return df

    dfs = [read_csv(url) for url in urls]
    return dfs


class Futures(__Historical):
    _category = 'futures'
    _freq = ('1d', '4h', '1h', '30m', '15m', '5m')
    _session = ('e',)
    _xpath = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[4]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]',
        contracts='//*[@id="maintable"]/tbody//tr/td[4]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _all_index_col = '先物'


class Indices(__Historical):
    _category = 'indices'
    _freq = ('1d', '4h', '1h', '30m', '15m', '5m')
    _session = ('a', 'b')
    _xpath = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _all_index_col = '指数'


class Stocks(__Historical):
    _category = 'stocks'
    _freq = ('1d', '4h', '1h', '30m', '15m', '5m')
    _session = ('a', 'b')
    _xpath = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _all_index_col = 'コード'


class Statistics(__Historical):
    _category = 'statistics'
    _freq = ('1d',)
    _session = []
    _xpath = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[2]//div/a/@href'
    )
    _all_index_col = '市場'


class KDBError(Exception):
    pass
