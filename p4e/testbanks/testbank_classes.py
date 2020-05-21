"""
This is a testbank for questions involving simple Classes 

Used on the final. 
"""

import random
from p4e import testlib 

class T05Counter(testlib.TestCase):
    """
    Note:
        Students create a simple class with three methods and two class variables. 

    Write a class called ``Counter``. The class has the variables:

    - ``self.count`` - Keeps track of the current count.
    - ``self.initial_count`` - Stores the initial count passed to ``__init__()``.

    The class has the following methods:

    Definition of ``__init__``:

    Arguments:
        self (Counter): The instance 
        start_num (int):  Initialize ``self.count`` with a starting count

    Definition of ``plus_one()``. Add one to the counter. 

    Arguments:
        self (Counter): The instance 

    Definition of ``minus_one()``. Subtract one from the counter. 

    Arguments:
        self (Counter): The instance 

    Definition of ``reset_count()``. Reset the counter to the initial value. 

    Arguments:
        self (Counter): The instance 
    """

    test_hasattr = 'Counter'

    class solution:
        """A Counter Class"""

        def __init__(self, start_num):
            """Initialize the class."""
            self.start = start_num
            self.count = start_num 

        def plus_one(self):
            """Add one."""
            self.count += 1 

        def minus_one(self):
            """Subtract one."""
            self.count -= 1 

        def reset_count(self):
            """Reset"""
            self.count = self.start


    def test_1_counter(self):
        """Testing your Counter class."""
        Counter = self.sandbox_class(self.test_hasattr)

        c = Counter(10)
        if not hasattr(c, 'count'):
            self.fail("""Your Counter class doesn't have a count attribute.""")

        if c.count != 10:
            self.fail("""The count attribute was not set in __init__()""")

        for _ in range(10):
            c.plus_one()
        if c.count != 20:
            self.fail("""I the count is not correct after calling plus_one()""")

        for _ in range(5):
            c.minus_one()
        if c.count != 15:
            self.fail("""I the count is not correct after calling minus_one()""")

        c.reset_count()
        if c.count != 10:
            self.fail("""I the count is not correct after calling reset_count()""")
