"""
Helper functions for test cases. 

Author: Mike Matera
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
import traceback
from contextlib import contextmanager
from pathlib import Path
from jinja2 import Template 
from flask import Flask

from IPython.core.display import display, HTML

from .sandbox import ClassSandbox, FlaskSandbox, FunctionSandbox


class DetailedTestResult(unittest.TestResult):
    """
    An implementation of unittest.TestResult that keeps result information instead of flattening it
    into a string and keeps a unified list of results in the same order that tests were run.  
    """ 

    class _Result:

        def __init__(self, label, visual, test, result, message=None, exc_info=None):
            self.label = label
            self.style = visual
            self.test_name = test.id().split('.')[-1]
            self.test_descr = test.shortDescription()
            self.stdout = sys.stdout.getvalue()
            self.stderr = sys.stderr.getvalue()
            self.message = message
            self.trace = list(test.trace)
            if exc_info is None:
                self.long_message = None 
            else:
                tb_e = traceback.TracebackException(*exc_info)
                self.message = str(exc_info[1])
                self.long_message = "".join(list(tb_e.format()))


    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.results = []
        self.run_cnt = 0
        self.passed_cnt = 0 
        self.failed_cnt = 0
        self.skipped_cnt = 0 
    
    def addError(self, test, err):
        self.results.append(DetailedTestResult._Result("ERROR", 'danger', test, self, exc_info=err))
        self.run_cnt += 1 
        self.failed_cnt += 1 
        
    def addExpectedFailure(self, test, err):
        self.results.append(DetailedTestResult._Result("(OK)FAIL", 'success', test, self, exc_info=err))
        self.run_cnt += 1 
        self.passed_cnt += 1 
        self.failed_cnt += 1 

    def addFailure(self, test, err):
        self.results.append(DetailedTestResult._Result("FAIL", 'danger', test, self, exc_info=err))
        self.run_cnt += 1 
        self.failed_cnt += 1 

    def addSkip(self, test, reason):
        self.results.append(DetailedTestResult._Result("SKIP", 'warning', test, self, message=reason))
        self.run_cnt += 1 
        self.skipped_cnt += 1 

    def addSuccess(self, test):
        self.results.append(DetailedTestResult._Result("PASS", 'success', test, self))
        self.run_cnt += 1 
        self.passed_cnt += 1 

    def addUnexpectedSuccess(self, test): 
        self.results.append(DetailedTestResult._Result("(BAD)PASS", 'danger', test, self))
        self.run_cnt += 1 
        self.failed_cnt += 1 

    def __repr__(self):
        return f"""{self.__class__.__name__} run={self.run_cnt} passed={self.passed_cnt} failed={self.failed_cnt} skipped={self.skipped_cnt}"""

def run():
    """Run unit tests in a Jupyter notebook. The test results are rendered as simple HTML"""
    with open(Path(__file__).parent / "template.html") as t:
        template = Template(t.read())
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0, buffer=True, resultclass=DetailedTestResult)
    program = unittest.main(argv=['ignored'], verbosity=0, exit=False, testRunner=runner)

    print(program.result)
    display(HTML(template.render(
        result=program.result
    )))

_dict_words = None
def words():
    """Get a list of dictionary words on the system."""
    global _dict_words
    if _dict_words is None:
        with open('/usr/share/dict/words') as f:
            _dict_words = list(f) 
    return _dict_words


class TestCase(unittest.TestCase):
    """
    A wrapper around unittest.TestCase that simplifies testing student code. 

    """

    def __init__(self, *args, **kwargs):
        """Initialize public attributes"""
        super().__init__(*args, **kwargs)

        self.absfile = None
        self.source = None
        self.module = None 
        self.trace = []

    def setUp(self):
        """Per-test setup. Skipps tests if self.test_file is not found."""
        super().setUp()
        self.absfile = Path(self.test_file)
        if not self.absfile.exists():
            raise unittest.SkipTest(f"""File {self.test_file} not found!""")
        self.absfile = self.absfile.resolve()
        with open(self.absfile) as fh:
            self.source = fh.read()

        self.module = None
        if hasattr(self, 'test_hasattr'):
            self.module = self._load_module()
            if not hasattr(self.module, self.test_hasattr):
                raise unittest.SkipTest(f"""Attribute {self.test_hasattr} not found in {self.test_file}.""")

        # Create a scratch area and make it the working directory.
        self.tempdir = tempfile.TemporaryDirectory()
        self.save_wd = os.getcwd()
        os.chdir(self.tempdir.name)

    def tearDown(self):
        # Restore wd 
        os.chdir(self.save_wd)
        self.tempdir.cleanup()

    def _load_module(self):
        try:
            save_stdin = sys.stdin
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            save_open = builtins.open
            sys.stdin = None
            sys.stdout = None
            sys.stderr = None
            builtins.open = None
            mod_spec = importlib.util.spec_from_file_location(str(uuid.uuid4()), str(self.absfile))
            mod = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod)

        except SyntaxError as e:
            self.fail("Test failed because there is a syntax error in your file.")

        except:
            self.fail("Test failed because there is code outside of a function.")

        finally:
            sys.stdin = save_stdin
            sys.stdout = save_stdout 
            sys.stderr = save_stderr
            builtins.open = save_open

        return mod

    @contextmanager
    def spawn(self, *cmdline):
        """Start a pexpect session and return the pexpect test. The program will be run in a temporary directory and the conversation will be echoed to sys.stdout.
        
        Arguments: 
            cmdline (str): A list of command line values to send to the program. 

        Returns: 
            (pexpect.spawn): A pexpect test object (can be used as a context manager).
        """ 
        error = None
        try:
            class SpawnWrapper(pexpect.spawn):
                def __init__(self, *args, **kwargs):
                    self.what = None
                    super().__init__(*args, **kwargs)
                
                def expect(self, what, *args, **kwargs):
                    self.what = what
                    super().expect(what, *args, **kwargs)

                def expect_exact(self, what, *args, **kwargs):
                    self.what = what
                    super().expect_exact(what, *args, **kwargs)

            spawn = SpawnWrapper(f'{sys.executable}', [str(self.absfile)] + list(cmdline), 
                    logfile=sys.stdout, timeout=2.0, echo=False, encoding='utf-8', 
                    cwd=self.tempdir.name,
                )
            yield spawn 

        except (pexpect.exceptions.EOF,  pexpect.exceptions.TIMEOUT) as e:
            if isinstance(spawn.what, list):
                choices = ', '.join(spawn.what)
            else:
                choices = spawn.what
            self.fail(f"""I expected to see one of [{choices}] from your program.""")


    def sandbox(self, attr):
        """Factory function to create a Sandbox that wraps the object named in `attr` in a Sandbox. The name must be present in the project, which will be loaded if it has not been already. The argument can be the name of a class, name of a function or name of a flask application. If `attr` is a callable the callable will be wrapped without a lookup in the project.

        Arguments:
            attr - The name of the function, Class or Flask app.

        Returns: The object `attr` wrapped in a Sandbox.
        """
        if callable(attr):
            return FunctionSandbox(self, attr) 

        if self.module is None:
            self.module = self._load_module()

        if not hasattr(self.module, attr):
            self.fail(f"""Your an object named {attr} not found!""")

        obj = getattr(self.module, attr)

        if isinstance(obj, type):
            if obj.__doc__ is None:
                self.fail(f"""Class {attr} has no docstring.""")
            return ClassSandbox(self, obj) 

        elif isinstance(obj, Flask):
            return FlaskSandbox(self, obj) 

        elif callable(obj):
            if obj.__doc__ is None:
                self.fail(f"""Function {attr} has no docstring.""")
            return FunctionSandbox(self, obj)
        else:
            raise ValueError(f"No Sandbox type for {attr}")

    def compare(self, got, exp):
        """Compare complex types for value equality. This is a convenience to simplify the 
        process of checking lists and dictionaries. This function does a "deep" comarison of 
        the two arguments, which must be of the same type.

        The self.fail() method will be executed if there is a mismatch. 

        Argumengs:
            got - The value given by test code. 
            exp - The golen (or expected) value. 

        Returns: None 
        """        
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


