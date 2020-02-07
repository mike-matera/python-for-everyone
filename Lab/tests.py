"""
Helper functions for test cases. 
"""

import io
import os 
import re
import sys
import uuid
import unittest
import importlib.util
from contextlib import contextmanager
from pathlib import Path

def run():
    unittest.main(argv=['ignored'], verbosity=3, exit=False)

# A list of dictionary words
words = []
with open('/usr/share/dict/words') as d :
    for w in d.readlines():
        words.append(w.strip())


@contextmanager
def io_control(input_text=''):
    """Wrap a function redirecting stdin/out/err""" 

    stdin_buf = io.StringIO(input_text)
    stdout_buf = io.StringIO()

    stdin = sys.stdin
    stdout = sys.stdout
    
    sys.stdin = stdin_buf
    sys.stdout = stdout_buf
    
    yield stdout_buf

    sys.stdin = stdin
    sys.stdout = stdout


class Project(unittest.TestCase):

    def load_file_safe(self, filename):
        file = Path(filename)
        if not file.exists():
            self.fail("I can't find your project file.")            
        try:
            mod = self.load_file(filename)
        except:
            self.fail("Test failed because there's code outside of a function.")
        return mod

    def load_file(self, filename):
        mod_spec = importlib.util.spec_from_file_location(str(uuid.uuid4()), filename)
        mod = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(mod)
        return mod

    def check_docstring(self, filename, module=False):
        if not module:
            with open(filename) as f:
                contents = f.read()
            self.assertIsNotNone(re.search(r'cis(\s*|-)15', contents, re.I),
                                 "Your source file doesn't seem to have the right docstring")
            return None
        else:
            stdin = sys.stdin
            stdout = sys.stdout
            sys.stdin = None
            sys.stdout = io.StringIO()
            try:
                mod = self.load_file(filename)
                self.assertIsNotNone(re.search(r'cis(\s*|-)15', mod.__doc__, re.I),
                                    "Your source file doesn't seem to have the right docstring")
                return mod
            finally:
                sys.stdin = stdin
                sys.stdout = stdout
        
