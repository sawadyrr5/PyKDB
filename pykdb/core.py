# -*- coding: utf-8 -*-
import pandas as pd

from pykdb.data.download import download_csv
from pykdb.utils import indexing
from pykdb.data.kdburl import CreateKdbUrl


class BaseHistorical:
    """
    先物,指数,個別株,統計の基底クラス
    """
    _CATEGORY = str()
    _AVAILABLE_FREQ = tuple()
    _AVAILABLE_SESSION = tuple()
    _XPATH = dict()
    _INDEX_PRICE_ALL = str()

    def __init__(self):
        """
        1. instancing CreateKdbUrl class.
        2. get category root for parse by lxml.
        """
        self._web = CreateKdbUrl(self._CATEGORY)
        self._root = self._web.category_root

    @property
    def symbols(self):
        """
        returns symbols list.
        :return:
        """
        return [symbol.split('/')[-1] for symbol in self._root.xpath(self._XPATH['symbols'])]

    @property
    def names(self):
        """
        returns symbols name dict.
        :return:
        """
        n = [e.text for e in self._root.xpath(self._XPATH['names'])]
        return dict(zip(self.symbols, n))

    @property
    def contracts(self):
        """
        returns symbols contracts.(futures only)
        :return:
        """
        c = [e.text for e in self._root.xpath(self._XPATH['contracts'])]
        return dict(zip(self.symbols, c))

    def price(self, date_from, date_to, symbol: str, freq: str) -> pd.DataFrame:
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
        # シンボルがユニバースにない場合は中断
        if symbol not in self.symbols:
            raise KDBError("specified symbol is not found in this _category.")

        # freqが使用可能でない場合は中断
        if freq not in self._AVAILABLE_FREQ:
            raise KDBError("specified freq is not available.")

        # 取得対象URLを生成
        urls = self._web.urls_price(date_from=date_from, date_to=date_to, symbol=symbol, freq=freq)

        # 取得対象URLを順次取得して結合
        dfs = []
        for url in urls:
            df = download_csv(url)
            dfs.append(df)
        else:
            df = pd.concat(dfs)

        # 日付変換やらインデックス付けやら
        df['日付'] = pd.to_datetime(df['日付'])

        if freq in ['1d', '4h']:
            df = indexing(df, ['日付'])

            df = df.ix[min(df[df.index >= date_from].index):max(df[df.index <= date_to].index)]
        else:
            # TODO: 2016/8/14 先物が時刻でもソートされるようにする
            df = indexing(df, ['日付', '時刻'])

        return df

    def price_all(self, date_from, date_to, session='') -> pd.DataFrame:
        """
        Download historical price of all symbols.
        :param date_from:
        :param date_to:
        :param session:
            Specify session.
        :return: pandas.DataFrame
        """
        # sessionが使用可能でない場合は中断
        if session not in self._AVAILABLE_SESSION:
            raise KDBError("specified session is not available.")

        # 取得対象URLと対応日付を生成
        urls, dates = self._web.urls_price_all(date_from=date_from, date_to=date_to, session=session)


        # 取得対象URLを順次取得して結合
        dfs = []
        for url, date in zip(urls, dates):
            df = download_csv(url)
            if not df.empty:
                df['日付'] = date
                dfs.append(df)
        else:
            df = pd.concat(dfs)

        df = indexing(df, ['日付', self._INDEX_PRICE_ALL])
        return df


class Futures(BaseHistorical):
    _CATEGORY = 'futures'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'e']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[4]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]',
        contracts='//*[@id="maintable"]/tbody//tr/td[4]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _index = {
        '1d': ['日付', '時刻'],
    }
    _INDEX_PRICE_ALL = '先物'


class Indices(BaseHistorical):
    _params = dict(
        category='indices'
    )
    _CATEGORY = 'indices'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'a', 'b']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _INDEX_PRICE_ALL = '指数'

    @property
    def contracts(self):
        raise NotImplementedError


class Statistics(BaseHistorical):
    _CATEGORY = 'statistics'
    _AVAILABLE_FREQ = ['1d']
    _AVAILABLE_SESSION = ['']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[2]//div/a/@href'
    )
    _INDEX_PRICE_ALL = '市場'

    @property
    def contracts(self):
        raise NotImplementedError


class Stocks(BaseHistorical):
    _CATEGORY = 'stocks'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'a', 'b']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _INDEX_PRICE_ALL = 'コード'

    @property
    def contracts(self):
        raise NotImplementedError


class KDBError(Exception):
    pass
