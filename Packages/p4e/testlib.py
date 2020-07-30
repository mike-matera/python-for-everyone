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
import time 
import threading
import requests 
import requests_unixsocket

from contextlib import contextmanager
from pathlib import Path
from jinja2 import Template 
from flask import Flask, request
from werkzeug.exceptions import HTTPException
from IPython.core.display import display, HTML 

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
            if hasattr(test, 'trace'):
                self.trace = list(test.trace)
            else:
                self.trace = []

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
        self.results.append(DetailedTestResult._Result("OK", 'success', test, self))
        self.run_cnt += 1 
        self.passed_cnt += 1 

    def addUnexpectedSuccess(self, test): 
        self.results.append(DetailedTestResult._Result("(BAD)PASS", 'danger', test, self))
        self.run_cnt += 1 
        self.failed_cnt += 1 

    def __repr__(self):
        return f"""{self.__class__.__name__} run={self.run_cnt} passed={self.passed_cnt} failed={self.failed_cnt} skipped={self.skipped_cnt}"""

def run(testname=None, template="template.html"):
    """Run unit tests in a Jupyter notebook. The test results are rendered as simple HTML"""

    with open(Path(__file__).parent / "templates" / template) as t:
        template = Template(t.read())

    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0, buffer=True, resultclass=DetailedTestResult)

    if testname is None:
        program = unittest.main(argv=['ignored'], verbosity=0, exit=False, testRunner=runner)
        result = program.result
    else:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(testname)
        result = runner.run(tests)

    def format_trace(t):
        args = []
        for a in t[1][0]:
            args.append(repr(a))
        for k, v in t[1][1].items():
            args.append(f"{k}={repr(v)}")
        
        return f"""{repr(t[2])} &crarr; {t[0]}({", ".join(args)})"""

    return template.render(
        result=result,
        format_trace=format_trace,
    )

def check(func, message="Failed!"):
    class _wrapper(unittest.TestCase):
        def test(self):
            if not func():
                self.fail(message)
    display(HTML(run(_wrapper, template="compact.html")))

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
        self.files = {}
        self.inputs = []
        self.save_open = None 
        self.save_input = None 

    def setUp(self):
        """Per-test setup. Skipps tests if self.test_file is not found."""
        super().setUp()

        if not hasattr(self, 'test_file'):
            self.test_file = None 
        
        if not hasattr(self, 'test_hasattr'):
            self.test_hasattr = None 

        if self.test_file is None and self.test_hasattr is None: 
            raise unittest.SkipTest(f"""Nothing to test.""")        

        if self.test_file is not None:
            self.absfile = Path(self.test_file)
            if not self.absfile.exists():
                raise unittest.SkipTest(f"""File {self.test_file} not found!""")
            self.absfile = self.absfile.resolve()
            with open(self.absfile) as fh:
                self.source = fh.read()
            self.module = None 
        else:
            self.module = sys.modules['__main__']

        if self.test_hasattr is not None:
            self._ensure_load_module()
            if not hasattr(self.module, self.test_hasattr):
                raise unittest.SkipTest(f"""Attribute {self.test_hasattr} not found in {self.module.__name__}.""")

        # Create a scratch area and make it the working directory.
        self.tempdir = tempfile.TemporaryDirectory()
        self.save_wd = os.getcwd()
        os.chdir(self.tempdir.name)

    def tearDown(self):
        # Restore wd 
        os.chdir(self.save_wd)
        self.tempdir.cleanup()

    def _ensure_load_module(self):

        if self.module is not None:
            return 

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

        self.module = mod

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

        self._ensure_load_module()

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

    def _sandbox_call(self, func, *args, **kwargs):
        """Execute a wrapped function."""
        try:
            if 'with_input' in kwargs:
                self.inputs = list(kwargs['with_input'])
                del kwargs['with_input']
            else:
                self.inputs = list()

            if 'check_return' in kwargs:
                checktype = kwargs['check_return']
                del kwargs['check_return']
            else:
                checktype = None

            self.save_open = builtins.open
            self.save_input = builtins.input
            save_stdout = sys.stdout
            save_stderr = sys.stderr

            builtins.open = self._sandbox_open
            builtins.input = self._sandbox_input

            rval = None
            rval = func(*args, **kwargs)
            return rval
        
        except Exception as e:
            rval = e 
            raise e 

        finally:
            builtins.open = self.save_open
            builtins.input = self.save_input

            # Verify that files are closed. 
            for file in self.files:
                if not self.files[file].closed:
                    self.test.fail(f"""Your function exited and left {file} open.""")

            # Add me to the trace log. 
            self.trace.append((func.__name__, (args, kwargs), rval))

            if checktype is not None \
                and not isinstance(rval, Exception) \
                and not isinstance(rval, checktype):
                self.fail(f"""Your function was supposed to return {checktype.__name__} but returned {rval.__class__.__name__} instead.""")


    def _sandbox_open(self, filename, mode='r', *args, **kwargs):
        """The open function that is exposed to the function under test.""" 
        filepath = Path(filename)
        tempdir = Path(self.tempdir.name) 
        
        if filepath.is_absolute():
            try:
                filepath = filepath.relative_to(tempdir)
            except:
                self.fail(f"""You should not open a file using an absolute path: {filename}""")

        fh = self.save_open(tempdir / filepath, mode, *args, **kwargs)
        self.files[filename] = fh

        return fh

    def _sandbox_input(self, prompt=None):
        """The input function that is exposed to the function under test."""
        if len(self.inputs) == 0:
            self.test.fail("""You should not use input in this function (or you've used it too many times).""")
        print(prompt, end="")
        return str(self.inputs.pop(0)) + '\n'

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


class FunctionSandbox:
    """A sandbox implementation for functions."""

    def __init__(self, test, func):
        self.test = test
        self.func = func 
    
    def __call__(self, *args, **kwargs):
        return self.test._sandbox_call(self.func, *args, **kwargs)


class ClassSandbox:
    """A sandbox implementation for a class and its methods."""

    def __init__(self, test, cls):
        self.test = test
        self.cls = cls 

    def __call__(self, *args, **kwargs):
        """Call the class constructor and wrap the instnace.""" 
        class _SandboxWrapper(self.cls):
            def __getattribute__(inner_self, name):
                attr = self.cls.__getattribute__(inner_self, name)
                if callable(attr):
                    def call_wrapper(*args, **kwargs):
                        return self.test._sandbox_call(attr, *args, **kwargs)
                    return call_wrapper
                return attr 

        return self.test._sandbox_call(_SandboxWrapper, *args, **kwargs)


class FlaskSandbox:
    """A sandbox implementation for Flask applications."""

    class SandboxRequestor:
        """A wrapper around requests.request() that simplifies testing."""

        def __init__(self, test, session, urlpattern):
            self.session = session
            self.url = urlpattern
            self.test = test 

        def get(self, path, status=None):
            if not path.startswith('/'):
                path = '/' + path
            response = self.session.get(self.url.format(path))
            if response.status_code == 500:
                self.test.fail(f"""There was an exception in your Flask program:\n{response.text}""")
            if status is not None and response.status_code != status:
                self.test.fail(f"""The respone code for {path} was {response.status_code} and should have been {status}""")
            return response 

    def __init__(self, test, app):
        self.test = test
        self.app = app 

    @contextmanager
    def run(self):
        """Launch the server and wait for it to handle connections."""

        self.socket = f"{self.test.tempdir.name}/flask.sock"
        self.url = "http+unix://" + self.socket.replace('/', '%2F') + "{}"

        session = requests_unixsocket.Session()

        def _ready():
            return "Ready"

        def _shutdown():
            request.environ.get('werkzeug.server.shutdown')()
            return "Goodbye!"

        def _exception(error):
            # pass through HTTP errors
            if isinstance(error, HTTPException):
                return error
            return str(error), 500

        def _run_thread():
            """Run the flask worker in a separate thread."""
            self.test._sandbox_call(self.app.run, host=f"unix://{self.socket}", threaded=False)

        self.app.add_url_rule('/ready', 'ready', _ready)
        self.app.add_url_rule('/shutdown', 'shutdown', _shutdown)
        self.app.register_error_handler(Exception, _exception)

        try:
            app_thread = threading.Thread(target=_run_thread, daemon=True)
            app_thread.start()

            tries = 10
            while app_thread.is_alive() and tries > 0:
                try:
                    r = session.get(self.url.format('/ready'))
                    break
                except requests.ConnectionError as e:
                    print(e)
                    time.sleep(0.5)
                    tries -= 1

            if not app_thread.is_alive():
                self.test.fail("The Flask server never started!")

            if tries == 0:
                self.test.fail("The Flask server never responded to a request!")

            yield FlaskSandbox.SandboxRequestor(self.test, session, self.url)
                    
        finally:
            session.get(self.url.format('/shutdown'))
            app_thread.join()
