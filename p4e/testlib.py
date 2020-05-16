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
import pexpect
from contextlib import contextmanager
from pathlib import Path

import HtmlTestRunner
from IPython.core.display import display, HTML 

class JupyterResult(HtmlTestRunner.result.HtmlTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)

    def generate_file(self, testRunner, report_name, report):
        display(HTML(report))


def run():
    devnull = io.StringIO()
    template = Path(__file__)
    template = template.parent / "report_template.html"
    runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, verbosity=0, 
        stream=devnull, resultclass=JupyterResult, template=str(template)
        )
    unittest.main(argv=['ignored'], verbosity=0, exit=False, testRunner=runner)
    #unittest.main(argv=['ignored'], verbosity=3, exit=False)

# A list of dictionary words
#words = []
#with open('/usr/share/dict/words') as d :
#    for w in d.readlines():
#        words.append(w.strip())


@contextmanager
def stdio_wrapper(input_text=''):
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

def load_module(filename):
    """
    Load a module from a filename. The module will be loaded anonymously. 

    Arguments:

        filename - A path to the file. 
    
    """
    f = Path(filename)
    mod_spec = importlib.util.spec_from_file_location(f.name, f)
    mod = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)
    return mod

class Project(unittest.TestCase):

    def setUp(self):
        file = Path(self.project_file)
        if not file.exists():
            raise unittest.SkipTest(f"""File ({file}) not found!""")

    @contextmanager
    def launch(self):
        try:
            test = pexpect.spawnu(f'{sys.executable} "{self.project_file}"')
            yield test
        finally:
            test.close()

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

    def check_docstring(self, filename, regex=r'cis(\s*|-)15', module=False):
        if not module:
            with open(filename) as f:
                contents = f.read()
            self.assertIsNotNone(re.search(regex, contents, re.I),
                                 "Your source file doesn't seem to have the right docstring")
            return None
        else:
            stdin = sys.stdin
            stdout = sys.stdout
            sys.stdin = None
            sys.stdout = io.StringIO()
            try:
                mod = self.load_file(filename)
                self.assertIsNotNone(re.search(regex, mod.__doc__, re.I),
                                    "Your source file doesn't seem to have the right docstring")
                return mod
            finally:
                sys.stdin = stdin
                sys.stdout = stdout
        
