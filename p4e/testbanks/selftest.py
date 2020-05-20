"""
CIS-15 Selftest Machine

This program runs testbank tests against their solutions. It's used for debugging testcases 
and solutions. 
"""

import io
import sys
import unittest
import inspect 

MIN_PYTHON = (3, 7)
assert sys.version_info >= MIN_PYTHON, f"requires Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer"


def flatten(tests):
    """Flatten tests so I can use them as a list."""
    for test in tests:
        if isinstance(test, unittest.suite.TestSuite):
            yield from flatten(test)
        else:              
            yield test 


def load():
    """Load all of the testcases in testbank_* files. Set the solution file to this file.""" 
    global tests
    tests = unittest.defaultTestLoader.discover(".", pattern='testbank*.py')
    for test in flatten(tests):
        test.test_file = __file__
    return tests 


def main():
    """Execute the tests."""
    tests = load()
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(tests)


test_cache = None

def __getattr__(name):
    """This file will be imported by test code and tests will look for thier 
    solution function. This function is called when a symbol is not found in 
    this module. When that happens see if it matches a test symbol and substitute
    the test's solution.
    
    This works in Python versions >= 3.7
    """

    global test_cache 
    if test_cache == None:
        test_cache = list(flatten(load()))

    for test in test_cache:
        if hasattr(test, 'test_hasattr') and test.test_hasattr == name:
            if hasattr(test, 'solution'):
                return test.solution

    raise AttributeError("No solution found.")


if __name__ == '__main__':
    main()

