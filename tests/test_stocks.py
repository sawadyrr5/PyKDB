# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Stocks, KDBError
from datetime import datetime
import time

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
        expected = '1301-T 極洋'
        actual = names['1301-T']
        self.assertEqual(expected, actual)

    def test_contracts(self):
        self.assertRaises(NotImplementedError, lambda: self.inst.contracts)

    def test_price(self):
        df = self.inst.price(sd, ed, '1301-T', '1d')
        expected = float(280)
        target_date = datetime(2016, 1, 4)
        actual = df[df.index == target_date]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)

    def test_price_all(self):
        time.sleep(5)
        df = self.inst.price_all(sd, ed)
        expected = float(280)
        target_date = datetime(2016, 1, 4)
        actual = df.loc[(target_date, '1301-T')]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestStocks))
    return suite


if __name__ == '__main__':
    unittest.main()
