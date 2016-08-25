import unittest
from tests.test_futures import TestFutures
from tests.test_indices import TestIndices
from tests.test_statistics import TestStatistics
from tests.test_stocks import TestStocks


class TestAll(unittest.TestCase):
    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestAll))
    suite.addTests(unittest.makeSuite(TestFutures))
    suite.addTests(unittest.makeSuite(TestIndices))
    suite.addTests(unittest.makeSuite(TestStatistics))
    suite.addTests(unittest.makeSuite(TestStocks))
    return suite

if __name__ == '__main__':
    unittest.main()
