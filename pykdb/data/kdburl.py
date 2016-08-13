# -*- coding: utf-8 -*-
from datetime import datetime
import urllib.request
import lxml.html
import pandas as pd


class CreateKdbUrl:
    """
    k-db.comアクセス用のURLを生成する
    """
    _URL_CATEGORY = 'http://k-db.com/{category}/'
    _URL_PRICE = '{symbol}/{freq}'
    _URL_PRICE_DL = '/{date}?download=csv'
    _URL_PRICE_ALL = '{date}{session}?download=csv'

    _DATE_FORMAT_FREQ = {
        '1d': '%Y',
        '4h': '%Y',
        '1h': '%Y%m',
        '30m': '%Y%m',
        '15m': '%Y%m%d',
        '5m': '%Y%m%d'
    }
    _DATE_FORMAT_PRICE_ALL = '%Y-%m-%d'

    def __init__(self, category):
        self._category = category

    @property
    def category_root(self):
        param = dict(category=self._category)
        url = self._URL_CATEGORY.format(**param)
        response = urllib.request.urlopen(url).read().decode('utf-8-sig')
        root = lxml.html.fromstring(response)
        return root

    def urls_price(self, date_from, date_to, symbol, freq):
        """
        create URLs for download single symbol price.
        :param date_from:
        :param date_to:
        :param symbol:
        :param freq:
        :return:
        """
        base_url = self._URL_CATEGORY + self._URL_PRICE + self._URL_PRICE_DL
        dates = self._date_range(date_from, date_to, freq)
        params = [dict(category=self._category, symbol=symbol, freq=freq, date=date) for date in dates]
        return [base_url.format(**param) for param in params]

    def urls_price_all(self, date_from, date_to, session=''):
        """
        create URLs for download all symbol prices.
        :param date_from:
        :param date_to:
        :param session:
        :return:
        """
        if session != '':
            session = '/' + session

        base_url = self._URL_CATEGORY + self._URL_PRICE_ALL
        dates = self._date_range(date_from, date_to)
        params = [dict(category=self._category, date=date, session=session) for date in dates]
        urls = [base_url.format(**param) for param in params]
        return urls, dates

    def _date_range(self, start, end, freq=None):
        """
        create formatted date string list.
        :param start:
        :param end:
        :param freq:
        :return:
        """
        if freq is None:
            date_format = self._DATE_FORMAT_PRICE_ALL
        else:
            date_format = self._DATE_FORMAT_FREQ[freq]
        dates = list({datetime.strftime(date, date_format) for date in pd.date_range(start, end, freq='D')})
        return sorted(dates)
