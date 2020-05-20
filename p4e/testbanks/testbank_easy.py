"""
This is a testbank of easy questions. 

These are free points on a test.
"""

import random
from p4e import testlib 

class T00Docstrings(testlib.TestCase):

    def test_has_docstring(self):
        """Testing your docstring."""        
        self.check_docstring()

class T01_ArgumentReverser(testlib.TestCase):
    """
    Write a function called ``arg_reverser`` that takes three arguments and returns 
    them in reverse order. 

    Function definition:

    - Name: ``arg_reverser``
    - Arguments: 
        - ``arg1`` 
        - ``arg2`` 
        - ``arg3``
    - Returns:
        - ``arg3``, ``arg2``, ``arg1`` 
    """

    test_hasattr = "arg_reverser"

    @staticmethod
    def solution(arg1, arg2, arg3):
        """Reverse my arguments."""
        return (arg3, arg2, arg1)

    def test_01_does_reverse(self):
        """Testing arg_reverser()"""

        w1 = random.choice(testlib.words()).strip()
        w2 = random.choice(testlib.words()).strip()
        w3 = random.choice(testlib.words()).strip()

        arg_reverser = self.sandbox_function(self.test_hasattr)
        got = arg_reverser(w1, w2, w3)
        self.compare(got, (w3, w2, w1))


class T03_TriangeArea(testlib.TestCase):
    """
    Write a function called ``triangle_area`` that takes two arguments, `base` and `height`. The function returns the area
    of a triangle that has the given ``base`` and ``height``.

    Function definition:

    - Name: ``triangle_area``
    - Arguments:
        - ``base`` - The base of the triangle.
        - ``height`` - The height of the triangle.
    - Returns:
        - The area of a triangle with ``base`` and ``height``.
    """

    test_hasattr = 'triangle_area'

    @staticmethod
    def solution(base, height):
        """Calculate the area of a triangle."""
        return (base * height) / 2 

    def test_01_does_compute(self):
        """You did not properly compute the area."""
        b = random.uniform(0, 100)
        h = random.uniform(0, 100)
        exp = (b * h) / 2
        triangle_area = self.sandbox_function(self.test_hasattr)
        got = triangle_area(b, h)
        self.compare(got, exp)
