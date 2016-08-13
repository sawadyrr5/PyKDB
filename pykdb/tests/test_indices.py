import unittest
from pykdb.core import Indices


class TestIndices(unittest.TestCase):
    inst = Indices()

    def test_name(self):
        sym = self.inst.symbols
        expected = '日経平均株価'
        actual = sym['I101']['name']
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
