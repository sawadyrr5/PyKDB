#! /usr/bin/env python
# -*- coding: utf-8 -*-
from PyKDB_back import Stocks, Futures, Indices, Statistics
import pandas as pd
import urllib.request
from datetime import datetime


class PyKDB:
    # define statistic symbols
    symbols_stat = (
        'T1', 'T2', 'TM', 'JQS',
        'T1-I201', 'T1-I202', 'T1-I203', 'T1-I204', 'T1-I205', 'T1-I206', 'T1-I207', 'T1-I208', 'T1-I209', 'T1-I210',
        'T1-I211', 'T1-I212', 'T1-I213', 'T1-I214', 'T1-I215', 'T1-I216', 'T1-I217', 'T1-I218', 'T1-I219', 'T1-I220',
        'T1-I221', 'T1-I222', 'T1-I223', 'T1-I224', 'T1-I225', 'T1-I226', 'T1-I227', 'T1-I228', 'T1-I229', 'T1-I230',
        'T1-I231', 'T1-I232', 'T1-I233'
    )
    _all_url = 'http://k-db.com/?p=all&download=csv'
    _base_url = 'http://k-db.com/{category}/{symbol}{interval}?{date}download=csv'
    _master = pd.DataFrame()

    def __init__(self):
        """
        Initialize class.
        :return: None
        """
        response = urllib.request.urlopen(PyKDB._all_url)
        PyKDB._master = pd.read_csv(response, encoding='Shift_JIS', skiprows=1)
        PyKDB._master.set_index('コード', inplace=True)
        return

    def hist(self, symbol, interval=None, start=None, end=None):
        """
        :param symbol: stock, index, future or statistics symbol
        :param interval: d, a, m5, m
        :param start: when interval is 'd' or 'a', start date.
                      when interval is 'm5' or 'm', specify date.
        :param end: when interval is 'd' or 'a', end date.
                    when interval is 'm5' or 'm', ignored.
        :return: pandas.DataFrame
        """
        if interval in ('d', 'a') and start > end:
            end = start

        hist_type = PyKDB.categories(symbol, interval)                            # select historical data type
        urls = self.urls(hist_type.category, symbol, interval, start, end)     # make url list

        df = pd.concat([PyKDB.fetch_data(url) for url in urls])                       # fetch by url list
        df = self.indexing(df, symbol, interval)

        if interval in ('d', 'a'):                                              # truncate outer period
            result = df.ix[start:end]
        else:
            result = df
        return result

    @classmethod
    def categories(cls, symbol, interval):
        if symbol in cls.symbols_stat:
            hist_type = Statistics(interval)
        elif any(cls._master[cls._master['業種'] == '先物'].index.isin([symbol])):
            hist_type = Futures(interval)
        elif any(cls._master[cls._master['業種'] == '指数'].index.isin([symbol])):
            hist_type = Indices(interval)
        else:
            hist_type = Stocks(interval)
        return hist_type

    @staticmethod
    def indexing(df, symbol, interval):
        hist_type = PyKDB.categories(symbol, interval)                            # select historical data type

        df.columns = hist_type.column                                           # set column name
        if interval in ('d', 'a'):
            df.set_index(pd.to_datetime(df['Date']), inplace=True)
            df.drop('Date', axis=1, inplace=True)
        elif interval in ('m5', 'm'):
            df['Date'] = df['Date'] + ' ' + df['Time']
            df.set_index(pd.to_datetime(df['Date']), inplace=True)
            df.drop(hist_type.index, axis=1, inplace=True)
        df.sort_index(ascending=True, inplace=True)
        df = df[df['Volume'] > 0]
        return df

    @staticmethod
    def urls(category, symbol, interval, start, end):
        url_interval = dict(
            d='',
            a='/a',
            m5='/5min',
            m='/minutely'
        )
        params = [dict(
                category=category,
                symbol=symbol,
                interval=url_interval[interval],
                date=date
        ) for date in PyKDB.datestr(interval, start, end)]

        result = [PyKDB._base_url.format(**param) for param in params]
        return result

    @staticmethod
    def datestr(interval, start, end):
        if interval in ('d', 'a') and isinstance(start, datetime) and isinstance(end, datetime):
            result = ['year=' + str(year) + '&' for year in range(start.year, end.year+1)]
        elif interval in ('m5', 'm') and isinstance(start, datetime):
            result = ['date=' + datetime.strftime(start, '%Y-%m-%d') + '&']
        else:
            result = []
        return result

    @staticmethod
    def fetch_data(url):
        response = urllib.request.urlopen(url)
        result = pd.read_csv(response, encoding='Shift_JIS', skiprows=1)
        return result
