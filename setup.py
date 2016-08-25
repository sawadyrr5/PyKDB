# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

sys.path.append('./pykdb')
sys.path.append('./tests')

setup(
    name='pykdb',
    version='0.0.2',
    description='Download historical price data from k-db.com',
    author='@sawadybomb',
    install_requires=['pandas', 'lxml'],
    url='https://twitter.com/sawadybomb/',
    test_suite='test_all.suite',
    packages=find_packages()
)
