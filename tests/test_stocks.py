# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Stocks
from datetime import datetime

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestStocks(unittest.TestCase):
    inst = Stocks()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = '1301-T' in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = '極洋'
        actual = names['1301-T']
        self.assertEqual(expected, actual)

    def test_price_all(self):
        df = self.inst.price_all(sd, ed)
        expected = 280.00
        actual = df.query("日付 == '2016-01-04' and 銘柄名 == '極洋'")['始値']
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
