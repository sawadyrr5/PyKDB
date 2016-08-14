# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Indices
from datetime import datetime
import time

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestIndices(unittest.TestCase):
    inst = Indices()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = 'I101' in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = '日経平均株価'
        actual = names['I101']
        self.assertEqual(expected, actual)

    def test_price_all(self):
        time.sleep(10)
        df = self.inst.price_all(sd, ed)
        expected = float(18818.58)
        actual = float(df.query("日付 == '2016-01-04' and 指数 == '日経平均株価'")['始値'])
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestIndices))
    return suite

if __name__ == '__main__':
    unittest.main()
