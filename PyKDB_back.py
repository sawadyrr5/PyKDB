#! /usr/bin/env python
# -*- coding: utf-8 -*-

# define columns sequence.
_cols_type = dict(
    all       =('Symbol', 'Name', 'Exchange', 'Sector', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
    day       =('Date', 'Open', 'High', 'Low', 'Close'),
    day_v     =('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
    session   =('Date', 'Session', 'Open', 'High', 'Low', 'Close'),
    session_v =('Date', 'Session', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
    minute    =('Date', 'Time', 'Open', 'High', 'Low', 'Close'),
    minute_v  =('Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
    statistics=('Date', 'Volume', 'DollarVolume', 'Numbers', 'Pricing', 'Up', 'Unchange', 'Down', 'Incomparable')
)

# define index sequence.
_index_type = dict(
    day    =['Date'],
    session=['Date', 'Session'],
    minute =['Date', 'Time']
)


class Stocks:
    category = 'stocks'
    _column_type = dict(
        d =_cols_type['day_v'],
        a =_cols_type['session_v'],
        m5=_cols_type['minute_v'],
        m =_cols_type['minute_v']
    )
    _index_type = dict(
        d =_index_type['day'],
        a =_index_type['session'],
        m5=_index_type['minute'],
        m =_index_type['minute']
    )

    def __init__(self, interval):
        self.column = self._column_type[interval]
        self.index = self._index_type[interval]
        return


class Indices:
    category = 'indices'
    _column_type = dict(
        d =_cols_type['day'],
        a =_cols_type['session'],
        m5=_cols_type['minute']
    )
    _index_type = dict(
        d =_index_type['day'],
        a =_index_type['session'],
        m5=_index_type['minute']
    )

    def __init__(self, interval):
        self.column = self._column_type[interval]
        self.index = self._index_type[interval]
        return


class Futures:
    category = 'futures'
    _column_type = dict(
        d=_cols_type['session_v'],
        a=_cols_type['session_v'],
        m5=_cols_type['minute_v'],
        m=_cols_type['minute_v']
    )
    _index_type = dict(
        d=_index_type['session'],
        a=_index_type['session'],
        m5=_index_type['minute'],
        m=_index_type['minute']
    )

    def __init__(self, interval):
        self.column = self._column_type[interval]
        self.index = self._index_type[interval]
        return


class Statistics:
    category = 'statistics'
    _column_type = dict(
        d=_cols_type['statistics'],
    )
    _index_type = dict(
        d=_index_type['day']
    )

    def __init__(self, interval):
        self.column = self._column_type[interval]
        self.index = self._index_type[interval]
        return
