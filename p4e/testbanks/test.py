"""
Execute a test from a testbank.
"""

import unittest

def main():
    tests = unittest.defaultTestLoader.discover(".", pattern='testbank*.py')
    for group in tests:
        for suite in group:
            for test in suite:
                test.test_file = 'answers_sp20.py'
    
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(tests)


if __name__ == '__main__':
    main()
