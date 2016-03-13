import pandas as pd
import urllib.request
from datetime import datetime


class PyKDB:
    master = pd.DataFrame()
    master_col = ['銘柄名', '市場', '業種']

    # define columns sequence.
    cols = dict(
        all       = ('Symbol', 'Name', 'Exchange', 'Sector', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        day       = ('Date', 'Open', 'High', 'Low', 'Close'),
        day_v     = ('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        session   = ('Date', 'Session', 'Open', 'High', 'Low', 'Close'),
        session_v = ('Date', 'Session', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        minute    = ('Date', 'Time', 'Open', 'High', 'Low', 'Close'),
        minute_v  = ('Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'DollarVolume'),
        statistics= ('Date', 'Volume', 'DollarVolume', 'Numbers', 'Pricing', 'Up', 'Unchange', 'Down', 'Incomparable')
    )
    # define index sequence.
    index = dict(
        day     = ['Date'],
        session = ['Date', 'Session'],
        minute  = ['Date', 'Time']
    )
    # define base url.
    base_url = dict(
        all       ='http://k-db.com/?p=all&download=csv',
        futures   ='http://k-db.com/futures/{symbol}',
        indices   ='http://k-db.com/indices/{symbol}',
        stock     ='http://k-db.com/stocks/{symbol}',
        statistics='http://k-db.com/statistics/{symbol}'
    )
    # define url, columns and index at future DataFrame
    futures = dict(
        url=base_url['futures'],
        cols=dict(
            d =cols['session_v'],
            a =cols['session_v'],
            m5=cols['minute_v'],
            m =cols['minute_v']
        ),
        index=dict(
            d =index['session'],
            a =index['session'],
            m5=index['minute'],
            m =index['minute']
        )
    )
    # define url, columns and index at index DataFrame
    indices = dict(
        url=base_url['indices'],
        cols=dict(
            d =cols['day'],
            a =cols['session'],
            m5=cols['minute']
        ),
        index=dict(
            d =index['day'],
            a =index['session'],
            m5=index['minute']
        )
    )
    # define url, columns and index at stock DataFrame
    stocks = dict(
        url=base_url['stock'],
        cols=dict(
            d =cols['day_v'],
            a =cols['session_v'],
            m5=cols['minute_v'],
            m =cols['minute_v']
        ),
        index=dict(
            d =index['day'],
            a =index['session'],
            m5=index['minute'],
            m =index['minute']
        )
    )
    # define url, columns and index at statistic DataFrame
    statistics = dict(
        url=base_url['statistics'],
        cols=dict(
            d=cols['statistics']
        ),
        index=dict(
            d=index['day']
        )
    )
    # define categories
    ctg = dict(指数=indices, 先物=futures, 個別株=stocks, 統計=statistics)
    # define future symbols
    symbols_futures = (

    )
    # define statistic symbols
    symbols_stat = (
        'T1', 'T2', 'TM', 'JQS',
        'T1-I201', 'T1-I202', 'T1-I203', 'T1-I204', 'T1-I205', 'T1-I206', 'T1-I207', 'T1-I208', 'T1-I209', 'T1-I210',
        'T1-I211', 'T1-I212', 'T1-I213', 'T1-I214', 'T1-I215', 'T1-I216', 'T1-I217', 'T1-I218', 'T1-I219', 'T1-I220',
        'T1-I221', 'T1-I222', 'T1-I223', 'T1-I224', 'T1-I225', 'T1-I226', 'T1-I227', 'T1-I228', 'T1-I229', 'T1-I230',
        'T1-I231', 'T1-I232', 'T1-I233'
    )

    def __init__(self):
        """
        Initialize class.
        :return: None
        """
        url = self.base_url['all']
        self.master = self._fetch(url)
        self.master.set_index('コード', inplace=True)
        return

    def _ctg(self, symbol):
        if symbol in self.symbols_stat:                       # if symbol is contained symbols_stat, "statistic"
            res = self.ctg['統計']
        else:
            ser = self.master['業種'].ix[symbol]              # symbol is not statistic, check symbol's sector
            if isinstance(ser, str):
                res = ser
            else:
                res = ser.drop_duplicates()[0]

            res = self.ctg.get(res, self.ctg['個別株'])       # sector contains word "指数", "先物" and others
        return res

    def hist(self, symbol, interval=None, start=None, end=None):
        ctg = self._ctg(symbol)

        # day
        df = pd.DataFrame()
        if interval in ('d', 'a'):
            if start > end:
                end = start

            date = datetime(start.year, 1, 1)
            while date <= end:
                url = self._url(symbol, interval, date)
                df = df.append(self._fetch(url))
                date = datetime(date.year+1, 1, 1)

            df.columns = ctg['cols'][interval]
            df.set_index(ctg['index'][interval], inplace=True)

#            df.index = pd.to_datetime(df.index)
#            df = df[(df.index >= start) & (df.index <= end)]

        # minute
        elif interval in ('m5', 'm'):
            url = self._url(symbol, interval, start)            # fetching data at start date. (ignore end date.)
            df = self._fetch(url)
            df.columns = ctg['cols'][interval]
            df.set_index(ctg['index'][interval], inplace=True)
        return df

    def _url(self, symbol, interval, date):
        ctg = self._ctg(symbol)
        url_interval = dict(
            d ='?{date}',
            a ='/a?{date}',
            m5='/5min?{date}',
            m ='/minute?{date}'
        )

        param = dict()
        param['symbol'] = symbol
        if interval in ('d', 'a') and isinstance(date, datetime):
            param['date'] = 'year=' + str(date.year) + '&'
        elif interval in ('m5', 'm') and isinstance(date, datetime):
            param['date'] = 'date=' + datetime.strftime(date, '%Y-%m-%d') + '&'
        else:
            url_interval[interval] = None
            param['date'] = None

        url = (ctg['url'] + url_interval[interval] + 'download=csv').format(**param)
        return url

    @staticmethod
    def _fetch(url):
        response = urllib.request.urlopen(url)
        df = pd.read_csv(response, encoding='Shift_JIS', skiprows=1)
        return df


if __name__ == '__main__':
    d_start = datetime(2015,  3,  9)
    d_end   = datetime(2015, 12, 20)
    d_date    = datetime(2016,  3,  7)

    myKDB = PyKDB()

#    u_symbol = 'F101-1606'  #future
#    u_symbol = 'I101'       #index
    u_symbol = '1301-T'     #stock
#    u_symbol = 'T1'         #stat

    u_df = myKDB.hist(u_symbol, 'a', d_start, d_end)
    print(u_df.head(5))

    print(u_df.index)
#    tmp = pd.to_datetime(u_df.index, utc=True).tz_convert('Asia/Tokyo')
#    print(tmp)
#    u_df = myKDB.hist(u_symbol, 'a', d_start, d_end)
#    print(u_df.head(5))
#    u_df = myKDB.hist(u_symbol, 'm5', d_start, None)
#    print(u_df.head(5))
#    u_df = myKDB.hist(u_symbol, 'm', d_start, None)
#    print(u_df.head(5))
