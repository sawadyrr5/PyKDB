import unittest
from pykdb.core import Futures
from datetime import datetime

sd = datetime(2016, 1, 4)
ed = datetime(2016, 1, 10)


class TestFutures(unittest.TestCase):
    inst = Futures()

    def test_name(self):
        sym = self.inst.symbols
        expected = '日経平均先物'
        actual = sym['F101-1609']['name']
        self.assertEqual(expected, actual)

    def test_contract(self):
        sym = self.inst.symbols
        expected = '2016年09月限'
        actual = sym['F101-1609']['contract']
        self.assertEqual(expected, actual)

    def test_price_all(self):
        df = self.inst.price_all(sd, ed)
        expected = 18830
        actual = df.query("日付 == '2016-01-04' and 先物 == '225mini先物 2016年01月限'")['始値']
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
