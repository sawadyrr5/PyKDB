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
        expected = 280
        actual = float(df.query("日付 == '2016-01-04' and コード == '1301-T'")['始値'])
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestStocks))
    return suite


if __name__ == '__main__':
    unittest.main()
