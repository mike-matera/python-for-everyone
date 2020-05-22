"""
CIS-15 Selftest Machine

This program runs testbank tests against their solutions. It's used for debugging testcases 
and solutions. 
"""

import io
import sys
import unittest
import inspect 

testfile = 'final_sp20.py'
testlib = '/home/maximus/lifealgorithmic-web/source/content/python-for-everyone/p4e/testbanks'

def flatten(tests):
    """Flatten tests so I can use them as a list."""
    for test in tests:
        if isinstance(test, unittest.suite.TestSuite):
            yield from flatten(test)
        else:              
            yield test 


def load():
    """Load all of the testcases in testbank_* files. Set the solution file to this file.""" 
    global testfile, testlib
    tests = unittest.defaultTestLoader.discover(testlib, pattern='testbank*.py')
    for test in flatten(tests):
        test.test_file = testfile
    return tests 


def main():
    """Execute the tests."""

    class MyResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.passes = []

        def addError(self, test, err):
            super().addError(test, err)
            print("ERROR:", test)

        def addFailure(self, test, err):
            super().addFailure(test, err)
            print("FAIL:", test)

        def addSuccess(self, test):
            super().addSuccess(test)
            self.passes.append(test)
            print("PASS:", test)

        def addSkip(self, test, reason):
            super().addSkip(test, reason)
            print("SKIP:", test)

    tests = load()
    runner = unittest.TextTestRunner(verbosity=0, resultclass=MyResult)
    got = runner.run(tests)

    for test in got.passes:
        print("PASS:", test)
    for test in got.failures:
        print("FAIL:", test[0])
    for test in got.errors:
        print("FAIL:", test[0])

if __name__ == '__main__':
    main()