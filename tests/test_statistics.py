# -*- coding: utf-8 -*-
import unittest
from pykdb.core import Statistics, KDBError
from datetime import datetime, date
import time

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

    def test_contracts(self):
        self.assertRaises(NotImplementedError, lambda: self.inst.contracts)

    def test_price(self):
        df = self.inst.price(sd, ed, 'T1', '1d')
        expected = float(1986571900)
        target_date = datetime(2016, 1, 4)
        actual = df[df.index == target_date]['出来高']
        actual = float(actual)
        self.assertEqual(expected, actual)

    def test_price_invalid_symbol(self):
        self.assertRaises(KDBError, lambda: self.inst.price(sd, ed, 'XX', '1d'))

    def test_price_invalid_freq(self):
        self.assertRaises(KDBError, lambda: self.inst.price(sd, ed, 'T1', '4h'))

    def test_price_all(self):
        time.sleep(5)
        df = self.inst.price_all(sd, ed)
        expected = float(1986571900)
        target_date = date(2016, 1, 4)
        actual = df[(target_date, '東証1部')]['出来高']
        actual = float(actual)
        self.assertEqual(expected, actual)

    def test_price_all_invalid_session(self):
        self.assertRaises(KDBError, lambda: self.inst.price_all(sd, ed, 'e'))


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestStatistics))
    return suite


if __name__ == '__main__':
    unittest.main()
