# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Futures
from datetime import datetime
import time

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)

test_symbol = 'F101-1609'
test_name = '日経平均先物'
test_contract = '2016年09月限'
test_name_contract = '225mini先物 2016年01月限'


class TestFutures(unittest.TestCase):
    inst = Futures()

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

    def test_contract(self):
        contracts = self.inst.contracts
        expected = test_contract
        actual = contracts[test_symbol]
        self.assertEqual(expected, actual)

    def test_price(self):
        sd = datetime(2016, 8, 12)
        ed = datetime(2016, 8, 13)
        df = self.inst.price(sd, ed, test_symbol, '1h')
        expected = float(16800)
        target_date = datetime(2016, 8, 12, 8)
        actual = float(df[df.index == target_date]['始値'])
        self.assertEqual(expected, actual)

    def test_price_all(self):
        time.sleep(5)
        df = self.inst.price_all(sd, ed)
        expected = float(18830)
        target_date = datetime(2016, 1, 4)
        actual = df.loc[(target_date, test_name_contract)]['始値']
        actual = float(actual)
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFutures))
    return suite


if __name__ == '__main__':
    unittest.main()
