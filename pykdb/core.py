# -*- coding: utf-8 -*-

import pandas as pd

from .data.kdb import KdbDownloader, KdbPrice, KdbPriceAll


class _Historical:
    _CATEGORY = ''
    _URL_DOWNLOAD = ''
    _FILE_NAME = ''
    _AVAILABLE_FREQ = tuple()
    _AVAILABLE_SESSION = tuple()
    _XPATH = dict()
    _INDEX_PRICE_ALL = str()
    _param = {}

    def __init__(self, enable_cache=True):
        dl = KdbDownloader(category=self._CATEGORY, enable_cache=enable_cache, )

        self._root = dl.root()
        self._symbols = [symbol.split('/')[-1] for symbol in self._root.xpath(self._XPATH['symbols'])]
        self._names = [e.text for e in self._root.xpath(self._XPATH['names'])]

    @property
    def symbols(self):
        return self._symbols

    @property
    def names(self):
        return dict(zip(self._symbols, self._names))

    def price(self, date_from, date_to, symbol, freq='1d') -> pd.DataFrame:

        if symbol not in self.symbols:
            raise KDBError("specified symbol is not found in this category.")

        if freq not in self._AVAILABLE_FREQ:
            raise KDBError("specified freq is not available.")

        dl = KdbPrice(category=self._CATEGORY, symbol=symbol, freq=freq)

        dfs = []
        for date in dl.date_range(date_from=date_from, date_to=date_to):
            df = dl.read(date)
            dfs.append(df)
        else:
            df = pd.concat(dfs)

        # インデックス設定
        if freq in ['1d', '4h']:
            df['日付'] = pd.to_datetime(df['日付'])
        else:
            df['日付'] = pd.to_datetime(df['日付'] + ' ' + df['時刻'])
        # df.drop(axis=1, labels='時刻', inplace=True)

        df = df.set_index(keys='日付')
        df = df.sort_index(axis=0, level='日付')
        df = df.ix[date_from:date_to]
        return df

    def price_all(self, date_from, date_to, session='', *args, **kwargs) -> pd.DataFrame:

        if session not in self._AVAILABLE_SESSION:
            raise KDBError("specified session is not available.")

        dl = KdbPriceAll(category=self._CATEGORY, session=session)

        dfs = []
        for date in dl.date_range(date_from=date_from, date_to=date_to):
            df = dl.read(date)
            if not df.empty:
                df['日付'] = pd.to_datetime(date)
                dfs.append(df)
        else:
            df = pd.concat(dfs)

        # インデックス設定
        df = df.set_index(keys=['日付', self._INDEX_PRICE_ALL])
        df = df.sort_index(axis=0, level=['日付', self._INDEX_PRICE_ALL])
        return df


class KDBError(Exception):
    pass


class Futures(_Historical):
    _CATEGORY = 'futures'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'e']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[4]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]',
        contracts='//*[@id="maintable"]/tbody//tr/td[4]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _INDEX_PRICE_ALL = '先物'

    _contracts = []

    def __init__(self):
        super().__init__()
        self._contracts = [e.text for e in self._root.xpath(self._XPATH['contracts'])]

    @property
    def contracts(self):
        """
        return symbol contracts.
        :return:
        """
        return dict(zip(self.symbols, self._contracts))


class Indices(_Historical):
    _CATEGORY = 'indices'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'a', 'b']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _INDEX_PRICE_ALL = '指数'

    def __init__(self):
        super().__init__()


class Statistics(_Historical):
    _CATEGORY = 'statistics'
    _AVAILABLE_FREQ = ['1d']
    _AVAILABLE_SESSION = ['']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[2]//div/a/@href'
    )
    _INDEX_PRICE_ALL = '市場'

    def __init__(self):
        super().__init__()


class Stocks(_Historical):
    _CATEGORY = 'stocks'
    _AVAILABLE_FREQ = ['1d', '4h', '1h', '30m', '15m', '5m']
    _AVAILABLE_SESSION = ['', 'a', 'b']
    _XPATH = dict(
        symbols='//*[@id="maintable"]/tbody//tr/td[1]/a/@href',
        names='//*[@id="maintable"]/tbody//tr/td[1]/a',
        date_range='//*[@id="contentmain"]/div[3]//div/a/@href'
    )
    _INDEX_PRICE_ALL = 'コード'

    def __init__(self):
        super().__init__()




if __name__ == '__main__':
    from datetime import datetime
    from pykdb import Stocks

    start = datetime(2016, 1, 4)
    end = datetime(2016, 1, 10)

    obj = Stocks()
    # print(obj.symbols)

    print(obj.price(start, end, '1301-T'))

    print(obj.price_all(start, end, ''))
