# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Indices, KDBError
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

    def test_contracts(self):
        self.assertRaises(NotImplementedError, lambda: self.inst.contracts)

    def test_price(self):
        df = self.inst.price(sd, ed, 'I101', '1d')
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
        actual = df.loc[(target_date, '日経平均株価')]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestIndices))
    return suite


if __name__ == '__main__':
    unittest.main()
