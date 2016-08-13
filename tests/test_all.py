import unittest
from .test_futures import TestFutures
from .test_indices import TestIndices
from .test_statistics import TestStatistics
from .test_stocks import TestStocks
from .test_kdburl import TestCreateKdbUrl


class TestAll(unittest.TestCase):
    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestAll))
    suite.addTests(unittest.makeSuite(TestFutures))
    suite.addTests(unittest.makeSuite(TestIndices))
    suite.addTests(unittest.makeSuite(TestStatistics))
    suite.addTests(unittest.makeSuite(TestStocks))
    suite.addTests(unittest.makeSuite(TestCreateKdbUrl))
    return suite

if __name__ == '__main__':
    unittest.main()
