import io
import os
import random
import re
import subprocess
import sys
import traceback
import unittest
from pathlib import Path
from p4e import testlib 


class T00Docstrings(testlib.TestCase):

    test_file = 'final.py'

    def test_has_docstring(self):
        """Testing your docstring."""        
        self.check_docstring()


class T01AverageList(testlib.TestCase):
    """
    Write a function called ``average_list()`` that takes a list of numbers as an
    argument and returns the average of the numbers in the list.

    - Arguments:
        - ``nums`` - A list of floats
    - Returns:
        - The average of the numbers in ``nums``

    """

    test_file = 'final.py'
    test_hasattr = 'average_list'

    def test_1_does_numbers(self):
        """Testing your average_list() function."""
        print("Testing average_list()")
        nums = []
        for i in range(random.randint(20, 100)):
            nums.append(random.uniform(1, 1000))
        exp = sum(nums) / len(nums)

        average_list = self.sandbox_function('average_list')
        got = average_list(nums)
        self.compare(got, exp)


class T02Running_Sum(testlib.TestCase):
    """
    Write a function called ``running_sum()`` that takes one argument called ``limit``.
    The function repeatedly prompts the user for numbers using ``input()`` adding all the numbers together.
    When the sum of the numbers is greater than or equal to ``limit`` the function returns the sum.

    - Arguments:
        - ``limit`` - Return when the sum of the ``input()`` numbers is greater than or equal to ``limit``
    - Returns:
        - The sum of the ``input()`` numbers.
        
    *Note: You can assume that the checker will only give you numbers.*
    """

    test_file = 'final.py'
    test_hasattr = 'running_sum'

    def test_1_check_sum(self):
        print("""+ Testing your running_sum() function""")

        nums = []
        for i in range(random.randint(20, 100)):
            nums.append(random.uniform(1, 1000))
        exp = sum(nums)
        nums.append(random.uniform(1, 1000))

        running_sum = self.sandbox_function('running_sum')
        running_sum.sandbox.allow_input(*nums)
        got = running_sum(nums, exp)
        self.compare(got, exp)


class T03ListFilter(testlib.TestCase):
    """
    Write a function called ``list_filter()`` that takes two arguments, ``number_list`` 
    and ``limit``. ``number_list`` is a list of floats and ``limit`` is a float. 
    The function returns a list containing only the numbers in ``number_list`` that are less than or equal to ``limit``.

    - Arguments:
        - ``number_list`` - A list of floats
        - ``limit``- Return numbers in ``number_list`` that are less than or equal to this. 
    - Returns:
        - The numbers in ``number_list`` that are less than or euqal to ``limit``
        
    """

    test_file = 'final.py'
    test_hasattr = 'list_filter'

    def test_1_check_list(self):
        """Test list_filter()"""
        print("""+ Testing your list_filter() function""")

        nums = []
        for i in range(random.randint(20, 100)):
            nums.append(random.uniform(1, 1000))
        limit = random.uniform(400, 600)
        exp = sorted([x for x in nums if x < limit])
        dut = self.sandbox_function(self.test_hasattr)
        got = sorted(dut(nums, limit))
        self.compare(exp, got)


class T04LetterCount(testlib.TestCase):
    """
    Write a function called ``letter_count()`` that takes one argument called ``phrase``.
    The function returns a dictionary with letters as keys and the number of times the letter
    appears in the ``phrase`` as values. The letter count is case insensitive so "A" is the same as "a".
    Only count characters where the ``isalpha()`` function returns ``True`` (in other words don't count punctuation.)

    For example. Given the phrase ``"Hello, World!"`` the ``letter_count()`` function should return:

    .. code-block:: python

    {
        'h' : 1,
        'e' : 1,
        'l' : 3,
        'o' : 2,
        'w' : 1,
        'r' : 1,
        'd' : 1,
    }
    

    - Arguments:
        - ``phrase`` - A phrase
    - Returns:
        - A dictionary that counts the frequency of each letter.
        
    """

    test_file = 'final.py'
    test_hasattr = 'letter_count'

    def letter_count(self, phrase):
        """Count the letters in the phrase."""
        rval = {}
        for letter in phrase.lower():
            if letter.isalpha():
                if letter not in rval:
                    rval[letter] = 1
                else:
                    rval[letter] += 1
        return rval

    def test_1_do_random_phrase(self):
        """Testing letter_count()"""
        print("""+ Testing your letter_count() function""")
        phrase = ""
        for _ in range(random.randint(5, 10)):
            phrase += random.choice(testlib.words()) + " "
        expected = self.letter_count(phrase)

        dut = self.sandbox_function(self.test_hasattr)
        got = dut(phrase)
        self.compare(expected, got)


class T05Counter(testlib.TestCase):
    """
    Write a class called ``Counter``. The class has the variables:

    - ``self.count`` - Keeps track of the current count.
    - ``self.initial_count`` - Stores the initial count passed to ``__init__()``.

    The class has the following methods:

    - ``__init__(start_num)`` - Initialize the counter with a starting count.
        - Arguments:
            - ``start_num`` - A number with the initial count.
    - ``plus_one()`` - Adds one to ``self.count``
        - Arguments: ``None``
        - Returns: ``None``
    - ``minus_one()`` - Subtracts one from ``self.count``
        - Arguments: ``None``
        - Returns: ``None``
    - ``reset_count()`` - Sets ``self.count`` to ``self.initial_count``
        - Arguments: ``None``
        - Returns: ``None``
    """

    test_file = "final.py"
    test_hasattr = 'Counter'

    def test_1_init(self):
        """There was an error creating an instance of class Counter"""
        print('+ Creating an in instance of final.Counter')
        Counter = self.sandbox_class('Counter')
        c = Counter(10)

    def test_2_has_count(self):
        """Your counter class doesn't have a count member variable"""
        print('+ Checking for the count member variable.')
        init = random.randint(1, 100)
        Counter = self.sandbox_class('Counter')
        c = Counter(init)
        self.assertEqual(init, c.count, "Your count variable doesn't exist or is not the right value")

    def test_3_increment(self):
        """Your counter didn't count up like it's supposed to."""
        print('+ Calling plus_one() to see if it works.')
        init = random.randint(1, 100)
        Counter = self.sandbox_class('Counter')
        c = Counter(init)    
        add = random.randint(1, 100)
        for i in range(add):
            c.plus_one()
        self.assertEqual(add + init, c.count, "Calling plus_one() doesn't seem to do the right thing.")

    def test_4_decrement(self):
        """Your counter didn't count down like it's supposed to."""
        print('+ Calling minus_one() to see if it works.')
        init = random.randint(1, 100)
        Counter = self.sandbox_class('Counter')
        c = Counter(init)    
        add = random.randint(1, 100)
        for i in range(add):
            c.minus_one()
        self.assertEqual(init - add, c.count, "Calling minus_one() doesn't seem to do the right thing.")

    def test_5_reset(self):
        """Your counter didn't go back to the initial value after calling reset_count()."""
        print('+ Calling reset_count() to see if it works.')
        init = random.randint(1, 100)
        Counter = self.sandbox_class('Counter')
        c = Counter(init)    
        add = random.randint(1, 100)
        for i in range(add):
            c.minus_one()

        c.reset_count()
        self.assertEqual(init, c.count, "Calling reset_count() doesn't seem to do the right thing.")

if __name__ == '__main__':
    unittest.main(verbosity=3)
