# -*- coding: utf-8 -*-
import os
import time
import urllib.request

import pandas as pd
import lxml.html
from datetime import datetime


class KdbDownloader:
    _CACHE_DIR = '/cache/'
    _URL_CATEGORY = 'http://k-db.com/{category}/'
    _URL_DOWNLOAD = ''
    _FILE_NAME = ''

    _param = {}

    def __init__(self, category, enable_cache=True):
        self._param['category'] = category
        self._enable_cache = enable_cache
        self._lib_root = os.path.dirname(os.path.abspath(__file__))

    def root(self):
        url = self._URL_CATEGORY.format(**self._param)
        response = urllib.request.urlopen(url).read().decode('utf-8-sig')
        root = lxml.html.fromstring(response)
        return root

    def read(self, date):
        self._param['date'] = date

        if self._enable_cache:
            _path = self._lib_root + self._CACHE_DIR + self._path(**self._param)
            if os.path.exists(_path):
                df = pd.read_csv(_path, encoding='Shift_JIS')
            else:
                df = self._download(**self._param)
                if not df.empty:
                    print()
                    print(_path)
                    df.to_csv(_path, index=False)
        else:
            df = self._download(**self._param)

        return df

    def del_cache(self, **kwargs):
        _path = self._path(**kwargs)
        for f in os.listdir(self._CACHE_DIR):
            if f == _path:
                os.remove(_path)

    def _path(self, **kwargs):
        _path = self._FILE_NAME.format(**kwargs)
        return _path

    def _download(self, **kwargs):
        url = self._URL_CATEGORY + self._URL_DOWNLOAD
        url = url.format(**kwargs)
        try:
            df = pd.read_csv(urllib.request.urlopen(url), encoding='Shift_JIS')
        except ValueError:
            df = pd.DataFrame()
        finally:
            time.sleep(2)
        return df

    def date_range(self, date_from, date_to):
        dates = sorted(
            list({datetime.strftime(date, self._format) for date in pd.date_range(date_from, date_to, freq='D')}))
        return dates


class KdbPrice(KdbDownloader):
    _URL_DOWNLOAD = '{symbol}/{freq}/{date}?download=csv'
    _FILE_NAME = '{category}_{symbol}_{freq}_{date}.csv'
    _DATE_FORMAT = {
        '1d': '%Y',
        '4h': '%Y',
        '1h': '%Y%m',
        '30m': '%Y%m',
        '15m': '%Y%m%d',
        '5m': '%Y%m%d'
    }

    def __init__(self, category, symbol, freq):
        super().__init__(category=category)
        self._param['symbol'] = symbol
        self._param['freq'] = freq
        self._format = self._DATE_FORMAT[freq]


class KdbPriceAll(KdbDownloader):
    _URL_DOWNLOAD = '{date}{session}?download=csv'
    _FILE_NAME = '{category}_{date}{session}.csv'

    def __init__(self, category, session):
        super().__init__(category=category)
        self._param['session'] = session
        self._format = '%Y-%m-%d'
