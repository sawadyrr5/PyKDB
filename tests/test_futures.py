# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Futures
from datetime import datetime

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestFutures(unittest.TestCase):
    inst = Futures()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = 'F101-1609' in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = '日経平均先物'
        actual = names['F101-1609']
        self.assertEqual(expected, actual)

    def test_contract(self):
        contracts = self.inst.contracts
        expected = '2016年09月限'
        actual = contracts['F101-1609']
        self.assertEqual(expected, actual)

    def test_price_all(self):
        df = self.inst.price_all(sd, ed)
        expected = 18830
        actual = float(df.query("日付 == '2016-01-04' and 先物 == '225mini先物 2016年01月限'")['始値'])
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
