"""
Execute a test from a testbank.
"""

import io
import sys
import unittest
import inspect 

class SelfTestRunner(unittest.TextTestRunner):
    pass

def selftest():
    tests = unittest.defaultTestLoader.discover(".", pattern='testbank*.py')
    for group in tests:
        for suite in group:
            for test in suite:
                test.test_file = 'answers_sp20.py'
    
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(tests)

def main():
    tests = unittest.defaultTestLoader.discover(".", pattern='testbank*.py')
    class MyResult(unittest.TextTestResult):

        def startTest(self, test):
            test.test_file = 'answers_sp20.py'
            print("SOLUTION IS:", inspect.getsource(test.solution), file=sys.stderr)

    #result = unittest.TextTestResult(unittest.runner._WritelnDecorator(sys.stdout), True, 3)
    runner = unittest.TextTestRunner(verbosity=3, resultclass=MyResult)
    runner.run(tests)
    #tests.run(result)
    
if __name__ == '__main__':
    main()
