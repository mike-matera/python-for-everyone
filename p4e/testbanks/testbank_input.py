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
    Note:
        Use the ``input()`` function and convert the value to a `float`. Students need to ``import math``    
    """

    test_hasattr = 'compute_sinc'

    @staticmethod
    def compute_sinc(x):
        """
        Write a function called ``compute_sinc`` that asks the user to input a number and
        computes the ``sinc`` function of that number. The ``sinc`` function of ``x`` is: 

        .. math:: 

            sin(x) / x 

        Definition of ``compute_sinc``:

        Returns:
            float: The sinc() function computed on the input.  
        """
        return math.sin(x) / x 

    def test_1_compute_sinc(self):
        """Testing compute_sinc"""
        x = random.uniform(0, 2 * math.pi)
        compute_sinc = self.sandbox(self.test_hasattr)
        compute_sinc.sandbox.allow_input(x)
        exp = math.sin(x) / x 
        got = compute_sinc(x)
        self.compare(got, exp)


class TestAddingMachine(testlib.TestCase) :
    """
    Note:
        Use input and convert the results to numbers. 
    """

    test_hasattr = "adding_machine"

    @staticmethod
    def adding_machine():
        """
        Write a function called ``adding_machine`` that uses the ``input()`` function three 
        times to get three floating point numbers from the user and returns the sum of
        the numbers. 

        Definition of ``adding_machine``:

        Returns:
            float: The sum of the input numbers. 
        """
        s = 0
        s += float(input('Enter a number: '))
        s += float(input('Enter a number: '))
        s += float(input('Enter a number: '))
        return s 

    def test_1_adding_machine(self) : 
        """Testing your adding_machine function."""
        n1 = random.random()
        n2 = random.random()
        n3 = random.random()
        adding_machine = self.sandbox(self.test_hasattr)
        adding_machine.sandbox.allow_input(n1, n2, n3)
        exp = n1 + n2 + n3
        got = adding_machine()
        self.compare(got, exp)
