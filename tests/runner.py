#!/usr/bin/env python
import sys
from unittest import TestLoader
from unittest import TextTestRunner


def main(path):
    loader = TestLoader()
    test = loader.discover(path)
    runner = TextTestRunner()
    runner.run(test)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s path' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])