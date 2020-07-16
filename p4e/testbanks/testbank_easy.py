"""
This is a testbank of easy questions. 

These are free points on a test.
"""

import re
import random
from p4e import testlib 

class T00Docstrings(testlib.TestCase):
    """
    Your program must have a docstring at the top of the file. 
    """

    def test_has_docstring(self):
        """Testing docstring"""
        if re.search(r'(?i)cis[ -]15', self.source) is None:
            self.fail('Your source file does not have a docstring')

class T01_ArgumentReverser(testlib.TestCase):
    """
    Note:
        Tests arguments and return values.
    """

    test_hasattr = "arg_reverser"

    @staticmethod
    def arg_reverser(arg1: object, arg2: object, arg3: object) -> tuple:
        """
        Write a function called ``arg_reverser`` that takes three arguments and returns 
        them in reverse order. 

        Function ``arg_reverser``:

        Args: 
            arg1 (object): The first argument.
            arg2 (object): The second argument.
            arg3 (object): The third argument.
        Returns:
            tuple: (arg3, arg2, arg1) 
        """
        return (arg3, arg2, arg1)

    def test_1_arg_reverser(self):
        """Testing arg_reverser()"""

        w1 = random.choice(testlib.words()).strip()
        w2 = random.choice(testlib.words()).strip()
        w3 = random.choice(testlib.words()).strip()

        arg_reverser = self.sandbox(self.test_hasattr)
        got = arg_reverser(w1, w2, w3)
        self.compare(got, (w3, w2, w1))


class T03_TriangeArea(testlib.TestCase):
    """
    Note:
        Tests arguments and return values, simple math. 
    """

    test_hasattr = 'triangle_area'

    @staticmethod
    def triangle_area(base, height):
        """
        Write a function called ``triangle_area`` that takes two arguments, `base` and `height`. The function returns the area
        of a triangle that has the given ``base`` and ``height``.

        Function ``triangle_area``:

        Arguments:
            base (float): The base of the triangle.
            height (float): The height of the triangle.
        Returns:
            float: The area of a triangle with ``base`` and ``height``.
        """
        return (base * height) / 2 

    def test_1_triangle_area(self):
        """Testing triangle_area()"""
        b = random.uniform(0, 100)
        h = random.uniform(0, 100)
        exp = (b * h) / 2
        triangle_area = self.sandbox(self.test_hasattr)
        got = triangle_area(b, h)
        self.compare(got, exp)
