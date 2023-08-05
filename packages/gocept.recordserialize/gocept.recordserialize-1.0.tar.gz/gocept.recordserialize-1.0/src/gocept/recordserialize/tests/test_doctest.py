import doctest
import os.path
import unittest


def test_suite():
    readme = '../../../README.txt'
    if not os.path.exists(readme):
        return unittest.TestSuite()
    return doctest.DocFileSuite('../' + readme)
