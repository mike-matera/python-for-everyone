"""
This is a testbank for file I/O. 

These may or may not be suitable for the midterm. 
"""

import math
import random
from p4e import testlib 

class T03_FileSums(testlib.TestCase):
    """
    Note:
        Open and read a file, add a fixed number of values. 
    """

    test_hasattr = 'file_sums'

    @staticmethod
    def file_sums(file):
        """
        Write a function called ``file_sums`` that takes one argument, the name of a 
        file. The file will have four numbers on separate lines. For example::
            
            12.23
            322.33
            21.9
            7.1

        The function should return ``True`` if the sum of all of the numbers in the file
        is greater than 100, ``False`` otherwise. 

        Definition of ``file_sums``: 

        Arguments: 
            filename (string): A file name
        Returns:
            bool: ``True`` if the sum is greater than 100. Otherwise ``False``
        """
        s = 0
        with open(file) as fh:
            for num in fh:
                s += float(num)
        return s > 100

    def test_1_file_sums(self): 
        """Testing file_sums()"""

        file_sums = self.sandbox(self.test_hasattr)

        with open('small.txt', 'w') as f:
            for _ in range(4):
                f.write(str(random.uniform(0, 20)) + "\n")

        with open('large.txt', 'w') as f:
            for _ in range(4):
                f.write(str(random.uniform(75, 200)) + "\n")

        got = file_sums('small.txt')
        self.compare(got, False)

        got = file_sums('large.txt')
        self.compare(got, True)


class T06_FileFibo(testlib.TestCase):
    """
    Note:
        Open and read and write the same file. This can be done using only 'r' and 'w' modes. 
        Students must understand the role of ``readline()`` and ``read()``. Can be done with 
        ``seek()``. 
    """

    test_hasattr = 'file_fibo'

    @staticmethod
    def file_fibo(file):
        """
        Write a function called ``file_fibo``. The function takes one argument, a 
        filename. The file will contain at least two lines with integers. Your 
        function should add the top two lines together, then overwrite the file, 
        adding the computed sum to the beginning of the file and moving the rest of 
        the numbers down. 

        For example, if the file contains the following before your function is 
        executed::
            
            5
            3
            2
            1
            1

        After executing your function the file should contain::

            8
            5
            3
            2
            1
            1
            
        Your function should not assume the file is any particular number of lines 
        (it's guaranteed to have at least two). The test program will call it 
        repeatedly. 

        Definition of ``file_fibo``:

        Arguments:
            filename (str): A file name
        """
        with open(file, "r") as fh:
            num1 = int(fh.readline())
            num2 = int(fh.readline())
            the_rest = fh.read()

        with open(file, 'w') as fh:
            fh.write(f"{num1 + num2}\n")
            fh.write(f"{num1}\n")
            fh.write(f"{num2}\n")
            fh.write(the_rest)

    def test_1_file_fibo(self):
        """Testing file_fibo()""" 

        file_fibo = self.sandbox(self.test_hasattr)

        with open('numbers.txt', 'w') as f:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            f.write(f'{num2}\n')
            f.write(f'{num1}\n')
         
        for i in range(random.randint(5,10)) : 
            file_fibo('numbers.txt')

        try:
            with open('numbers.txt', 'r') as f:
                nums = list(reversed([int(x) for x in f]))
        except:
            self.fail("The file should only contain integers!")

        got1 = nums.pop(0)
        got2 = nums.pop(0)
        for num in nums:
            s = got1 + got2
            self.compare(num, got1 + got2)
            got1 = got2 
            got2 = s


class T07_FileDecoderRing(testlib.TestCase):
    """
    Note:
        A tricky problem that uses file I/O. The trick is to use ``seek()`` and to recognize that the
        seek offset can be computed from the ``decoder_letter`` argument. Advanced students will do 
        this using arrays and file iterators. 
    """

    test_hasattr = 'decoder_ring'

    @staticmethod
    def decoder_ring(decoder_file, decoder_letter):
        """
        Write a function called ``decoder_ring`` that takes two arguments, ``decoder_file`` and ``decoder_letter``. The
        function returns a letter from the file ``decoder_file`` based on the integer in ``decoder_letter``. The contents of
        ``decoder_file`` will be a list of letters on different lines. For example::

            a
            b
            c
            d
            e

        The function should return the letter on the line number given in ``decoder_letter``. **The first line is line number one**.
        For example if the ``decoder_letter`` is 3 for the file shown above ``decoder_ring`` should return the letter ``c``. The file will always
        have one letter on each line with no additional spaces. The function should return the letter by itself without a newline.

        Definition of ``decoder_ring``:

        Arguments:
            decoder_file (str): A file that contains the decoder letters.
            decoder_letter (int): The line number of the letter to return.
        Returns:
            (str): The letter on the specified line of the file without a newline.
        """
        with open(decoder_file) as fh:
            fh.seek((decoder_letter-1) * 2)
            return fh.read(1)

    def test_01_decoder_ring(self):
        """Testing decoder_ring()"""
        letters = ""
        for _ in range(random.randint(1,1)):
            letters += random.choice(testlib.words()).strip()
        number = random.randint(1, len(letters))
        exp = letters[number-1]

        decoder_ring = self.sandbox(self.test_hasattr)
        with open('codes.txt', 'w') as fh:
            for l in letters:
                fh.write(l + "\n")

        got = decoder_ring('codes.txt', number)
        self.compare(got, exp)

