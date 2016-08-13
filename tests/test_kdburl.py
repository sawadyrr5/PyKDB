# -*- coding: utf-8 -*-
import unittest
from pykdb.data.kdburl import CreateKdbUrl
from datetime import datetime

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 7)


class TestCreateKdbUrl(unittest.TestCase):
    def test_date_range(self):
        f = CreateKdbUrl('futures')
        expected = ['2016-01-04', '2016-01-05', '2016-01-06', '2016-01-07']
        actual = f._date_range(sd, ed)
        self.assertEqual(expected, actual)

    def test_futures_price(self):
        f = CreateKdbUrl('futures')
        expected = ['http://k-db.com/futures/F101-1609/1d/2016?download=csv']
        actual = f.urls_price(sd, ed, 'F101-1609', '1d')
        self.assertEqual(expected, actual)

    def test_futures_price_all(self):
        f = CreateKdbUrl('futures')
        expected = (
            ['http://k-db.com/futures/2016-01-04/e?download=csv',
             'http://k-db.com/futures/2016-01-05/e?download=csv',
             'http://k-db.com/futures/2016-01-06/e?download=csv',
             'http://k-db.com/futures/2016-01-07/e?download=csv', ],
            ['2016-01-04', '2016-01-05', '2016-01-06', '2016-01-07'])
        actual = f.urls_price_all(sd, ed, 'e')
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestCreateKdbUrl))
    return suite


if __name__ == '__main__':
    unittest.main()
