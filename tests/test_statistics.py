# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Statistics
from datetime import datetime

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestStatistics(unittest.TestCase):
    inst = Statistics()

    def test_symbol(self):
        symbols = self.inst.symbols
        expected = True
        actual = 'T1' in symbols
        self.assertEqual(expected, actual)

    def test_name(self):
        names = self.inst.names
        expected = '東証1部'
        actual = names['T1']
        self.assertEqual(expected, actual)

    def test_price_all(self):
        df = self.inst.price_all(sd, ed)
        expected = 1986751900
        actual = df.query("日付 == '2016-01-04' and 市場 == '東証1部'")['出来高']
        self.assertEqual(expected, actual)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestStatistics))
    return suite


if __name__ == '__main__':
    unittest.main()
