"""
This is a testbank of questions that use loops (and may use lists or dictionaries)

Use these on the final. 
"""

import random
from p4e import testlib 


class T01AverageList(testlib.TestCase):
    """
    Note:
        Loop over a list to perform simple math. Does not require conditionals. 
    """

    test_hasattr = 'average_list'

    @staticmethod
    def average_list(nums):
        """
        Write a function called ``average_list()`` that takes a list of numbers as an
        argument and returns the average of the numbers in the list.

        Arguments:
            nums (list of float): A list of numbers to filter
        Returns:
            (float): The average of the numbers in ``nums``
        """
        s = 0
        for num in nums:
            s += num
        return s / len(nums) 

    def test_1_average_list(self):
        """Testing your average_list() function."""
        nums = []
        for i in range(random.randint(20, 100)):
            nums.append(random.uniform(1, 1000))
        exp = sum(nums) / len(nums)

        average_list = self.sandbox('average_list')
        got = average_list(nums)
        self.compare(got, exp)


class T02Running_Sum(testlib.TestCase):
    """
    Note:
        Loop over a list with an unknown stop condition. Can be done with ``for`` or ``while``. 
    """

    test_hasattr = 'running_sum'

    @staticmethod
    def running_sum(limit):
        """
        Write a function called ``running_sum()`` that takes one argument called ``limit``.
        The function repeatedly prompts the user for numbers using ``input()`` adding all the numbers together.
        When the sum of the numbers is greater than or equal to ``limit`` the function returns the sum.

        Arguments:
            limit (float): Return when the sum of the ``input()`` numbers is greater than or equal to ``limit``
        Returns:
            (float): The sum of the ``input()`` numbers.
            
        *Note: You can assume that the checker will only give you numbers.*
        """
        sums = 0
        while True:
            sums += float(input('Give me a number:'))
            if sums >= limit:
                return sums

    def test_1_running_sum(self):
        nums = []
        for i in range(random.randint(20, 100)):
            nums.append(random.uniform(1, 1000))
        exp = sum(nums)
        nums.append(random.uniform(1, 1000))

        running_sum = self.sandbox(self.test_hasattr)
        got = running_sum(exp, with_input=nums)
        self.compare(got, exp)
