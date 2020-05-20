"""
A testbank that uses the input() function. 

This is a midterm test bank: 
    - No if
    - No loops 
    - No list/dict
"""

import math
import random
from p4e import testlib 


class T02_UserInput(testlib.TestCase):
    """
    Write a function called ``compute_sinc`` that asks the user to input a number and
    computes the ``sinc`` function of that number. The ``sinc`` function of ``x`` is: 

    .. math:: 

        sin(x) / x 

    Function definition:

    - Name: ``compute_sinc``
    - Arguments: ``None``
    - Returns:
        - ``sinc(x)`` 
    """

    test_hasattr = 'compute_sinc'

    @staticmethod
    def solution(x):
        """Compute sin(x)/x"""
        return math.sin(x) / x 

    def test_01_does_sinc(self):
        """Testing compute_sinc"""
        x = random.uniform(0, 2 * math.pi)
        compute_sinc = self.sandbox_function(self.test_hasattr)
        compute_sinc.sandbox.allow_input(x)
        exp = math.sin(x) / x 
        got = compute_sinc(x)
        self.compare(got, exp)


class TestAddingMachine(testlib.TestCase) :
    """
    Write a function called ``adding_machine`` that uses the ``input()`` function three 
    times to get three floating point numbers from the user and returns the sum of
    the numbers. 

    Function definition:

    - Name: ``adding_machine``
    - Arguments
        - ``None``
    - Returns
        - The sum (``float``)
    """

    test_hasattr = "adding_machine"

    @staticmethod
    def solution():
        """The adding_machine function."""
        s = 0
        s += float(input('Enter a number: '))
        s += float(input('Enter a number: '))
        s += float(input('Enter a number: '))
        return s 

    def test_1_add(self) : 
        """Testing your adding_machine function."""
        n1 = random.random()
        n2 = random.random()
        n3 = random.random()
        adding_machine = self.sandbox_function(self.test_hasattr)
        adding_machine.sandbox.allow_input(n1, n2, n3)
        exp = n1 + n2 + n3
        got = adding_machine()
        self.compare(got, exp)
