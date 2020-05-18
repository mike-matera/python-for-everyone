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
import tempfile
import builtins
from contextlib import contextmanager
from pathlib import Path
from jinja2 import Template 
from IPython.core.display import display, HTML

class JupyterTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def addSuccess(self, test):
        self.successes.append((test, None))

def run():
    devnull = io.StringIO()
    with open(Path(__file__).parent / "simple_template.html") as t:
        template = Template(t.read())
    runner = unittest.TextTestRunner(stream=devnull, resultclass=JupyterTestResult, buffer=True)
    with stdio_wrapper():
        program = unittest.main(argv=['ignored'], verbosity=0, exit=False, testRunner=runner)


    display(HTML(template.render(
        result=program.result
    )))

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
        super().setUp()
        file = Path(self.project_file)
        if not file.exists():
            raise unittest.SkipTest(f"""File ({file}) not found!""")
   
    def mktemp(self, contents):
        t = tempfile.NamedTemporaryFile(mode='w')
        for line in contents:
            t.write(line + '\n')
        t.flush()
        return t 

    @contextmanager
    def spawn(self, *cmdline):
        try:
            self.test = pexpect.spawnu(f'{sys.executable}', [self.project_file] + list(cmdline), 
                    logfile=sys.stdout, timeout=2, echo=False,
                    )
            yield self.test
        finally:
            self.test.close()

    def expect(self, value, message):
        if 2 != self.test.expect([pexpect.EOF, pexpect.TIMEOUT, value]):
            self.fail(message)

    def sendline(self, line):
        self.test.sendline(line)

    def load_module(self):
        file = Path(self.project_file)
        try:
            mod_spec = importlib.util.spec_from_file_location(str(uuid.uuid4()), str(file))
            mod = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod)
        except:
            self.fail("Test failed because there might be code outside of a function.")
        return mod

    def load_function(self, name):
        mod = self.load_module()
        if not hasattr(mod, name):
            self.fail(f"""Your program doesn't have a function named {name}""")
        func = getattr(mod, name)
        if func.__doc__ is None:
            self.fail(f"""Your {name} function has no docstring.""")
        #return Sandbox(self, func) 
        return func 

    def check_docstring(self, filename, regex=r'cis(\s*|-)15'):
        with open(filename) as f:
            contents = f.read()
        self.assertIsNotNone(re.search(regex, contents, re.I),
                                "Your source file doesn't seem to have the right docstring")
        return None

    def compare(self, got, exp):
        message = self._compare(got, exp)
        if message is not None:
            self.fail(message)

    def _compare(self, got, exp):
        """Recursively check for equality in common types."""

        # Check type
        if not isinstance(got, exp.__class__):
            return f"""Mismatched type: {got.__class__.__name__} expected: {exp.__class__.__name__}"""

        if isinstance(exp, str) or isinstance(exp, int):
            if exp != got:
                return f"""Mismatched value: {got} expected: {exp}"""

        elif isinstance(exp, float):
            if round(got,3) != round(exp,3):
                return f"""Mismatched value: {got} expected: {exp} (rounded)"""

        elif isinstance(exp, list) or isinstance(exp, tuple):
            if len(exp) != len(got):
                return f"""Length mismatch: {got} (length {len(got)}) expected: {exp} (length: {len(exp)})"""
            for i in range(len(exp)):
                message = self._compare(got[i], exp[i])
                if message is not None: 
                    return f"""List value mismatch on index {i}: {message}"""

        elif isinstance(exp, dict):
            if len(exp) != len(got):
                return f"""Key count mismatch: {got} (length {len(got)}) expected: {exp} (length: {len(exp)})"""
            for k in exp:
                if k not in got:
                    return f"""Missing dictionary key: {k} in {got} expected: {exp}""" 
                message = self._compare(got[k], exp[k])
                if message is not None: 
                    return f"""Dictionary value mismatch on key {k}: {message}"""

        else:
            raise ValueError("The compare function doesn't work on this type:", exp.__class__.__name__)

    @contextmanager
    def fake_input(self, value):
        try:
            save_input = builtins.input
            builtins.input = lambda p: f"{value}\n"
            yield 
        finally:
            builtins.input = save_input

    @contextmanager
    def fake_open(self):
        stream = {
            'filename': None, 
            'mode': None, 
            'data': io.StringIO(),
        }
        def _open_wrapper(name, mode="r"):
            stream['filename'] = name
            stream['mode'] = mode
            return stream['data']
        try:
            save_open = builtins.open
            builtins.open = _open_wrapper
            yield stream
        finally:
            builtins.open = save_open


class Sandbox:
    """A class to wrap test functions.""" 

    def __init__(self, test, func):
        self.func = func
        self.test = test
        self.files = []

    def __call__(self, *args, **kwargs):

        try:
            save_open = builtins.open
            save_input = builtins.input
            builtins.open = self._open
            builtins.input = self._input
            return self.func(*args, **kwargs)
        finally:
            builtins.open = save_open
            builtins.input = save_input


    @contextmanager
    def _open(filename, mode):
        yield None

    def _input(prompt):
        return "Junk"
