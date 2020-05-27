"""
This is a testbank of questions using dictionaries.

Use this on the final.
"""

import random
from p4e import testlib 

class T04LetterCount(testlib.TestCase):
    """
    Note:
        Loop over a string to create a dictionary. Students need to handle create/add case. 
    """

    test_hasattr = 'letter_count'

    @staticmethod
    def letter_count(phrase):
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

        Function ``letter_count``: 

        Arguments:
            phrase (str): A phrase
        Returns:
            dict: A dictionary that counts the frequency of each letter.        
        """
        rval = {}
        for letter in phrase.lower():
            if letter.isalpha():
                if letter not in rval:
                    rval[letter] = 1
                else:
                    rval[letter] += 1
        return rval

    def test_1_letter_count(self):
        """Testing letter_count()"""
        phrase = ""
        for _ in range(random.randint(5, 10)):
            phrase += random.choice(testlib.words()) + " "
        expected = self.letter_count(phrase)

        dut = self.sandbox(self.test_hasattr)
        got = dut(phrase)
        self.compare(got, expected)

