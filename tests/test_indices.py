# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Indices
from datetime import datetime
import time

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)

test_symbol = 'I101'
test_name = '日経平均株価'

class TestIndices(unittest.TestCase):
    inst = Indices()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = test_symbol in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = test_name
        actual = names[test_symbol]
        self.assertEqual(expected, actual)

    def test_price(self):
        df = self.inst.price(sd, ed, test_symbol)
        expected = float(18818.58)
        target_date = datetime(2016, 1, 4)
        actual = df[df.index == target_date]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)

    def test_price_all(self):
        time.sleep(5)
        df = self.inst.price_all(sd, ed)
        expected = float(18818.58)
        target_date = datetime(2016, 1, 4)
        actual = df.loc[(target_date, test_name)]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestIndices))
    return suite


if __name__ == '__main__':
    unittest.main()
