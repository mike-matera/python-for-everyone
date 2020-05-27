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
from contextlib import contextmanager
from pathlib import Path
from jinja2 import Template 
import threading
import time
import requests 
import requests_unixsocket
from IPython.core.display import display, HTML
from flask import Flask, request
from werkzeug.exceptions import HTTPException

class JupyterTestResult(unittest.TextTestResult):
    """A test result class that is rendered into a Jupyter notebook.
    
    The only difference between this and TextTestResult is that successes are recorded. 
    """ 
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def addSuccess(self, test):
        self.successes.append((test, None))

def run():
    """Run unit tests in a Jupyter notebook. The test results are rendered as simple HTML"""
    devnull = io.StringIO()
    with open(Path(__file__).parent / "simple_template.html") as t:
        template = Template(t.read())
    runner = unittest.TextTestRunner(stream=devnull, resultclass=JupyterTestResult, buffer=True)
    with stdio_wrapper():
        program = unittest.main(argv=['ignored'], verbosity=0, exit=False, testRunner=runner)

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


class TestCase(unittest.TestCase):
    """
    A wrapper around unittest.TestCase that simplifies testing student code. 

    """

    def setUp(self):
        """Per-test setup. Skipps tests if self.test_file is not found."""
        super().setUp()
        file = Path(self.test_file)
        if not file.exists():
            raise unittest.SkipTest(f"""File {file} not found!""")

        self.module = None
        if hasattr(self, 'test_hasattr'):
            self.module = self._load_module()
            if not hasattr(self.module, self.test_hasattr):
                raise unittest.SkipTest(f"""Attribute {self.test_hasattr} not found in {self.module.__file__}.""")

        # Create a scratch area.
        self.tempdir = tempfile.TemporaryDirectory()

    def _load_module(self):
        file = Path(self.test_file)
        try:
            mod_spec = importlib.util.spec_from_file_location(str(uuid.uuid4()), str(file))
            mod = importlib.util.module_from_spec(mod_spec)
            mod_spec.loader.exec_module(mod)
        except:
            self.fail("Test failed because there might be code outside of a function.")
        return mod

    def tearDown(self):
        self.tempdir.cleanup()

    def open(self, filename, *args, **kwargs):
        """Open a file in the scratch area. Arguments are passed to open(). Can be used as a context manager."""
        filepath = Path(self.tempdir.name) / filename 
        return open(filepath, *args, **kwargs)

    @contextmanager
    def spawn(self, *cmdline):
        """Start a pexpect session and return the pexpect test. The program will be run in a temporary directory and the conversation will be echoed to sys.stdout.
        
        Arguments: 
            cmdline (str): A list of command line values to send to the program. 

        Returns: 
            (pexpect.spawn): A pexpect test object (can be used as a context manager).
        """ 
        error = None
        absfile = Path(self.test_file).resolve()
        try:
            class SpawnWrapper(pexpect.spawn):
                def __init__(self, *args, **kwargs):
                    self.what = None
                    super().__init__(*args, **kwargs)
                
                def expect(self, *args, **kwargs):
                    self.what = args[0]
                    super().expect(*args, **kwargs)

                def expect_exact(self, *args, **kwargs):
                    self.what = args[0]
                    super().expect_exact(*args, **kwargs)

            spawn = SpawnWrapper(f'{sys.executable}', [str(absfile)] + list(cmdline), 
                    logfile=sys.stdout, timeout=2.0, echo=False, encoding='utf-8', 
                    cwd=self.tempdir.name,
                )
            yield spawn 

        except (pexpect.exceptions.EOF,  pexpect.exceptions.TIMEOUT) as e:
            self.fail(f"""I expected to see one of [{','.join(spawn.what)}] from your program.""")


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

    def check_docstring(self, regex=r'cis(\s*|-)15'):
        """Check the project file for a docstring matching regex"""
        file = Path(self.test_file)
        with open(file) as f:
            contents = f.read()
        self.assertIsNotNone(re.search(regex, contents, re.I),
                                "Your source file doesn't seem to have the right docstring")
        return None

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


class SandboxFile:
    """Container that can be opened, read and written from the sandbox."""

    class StringIOWrapper(io.StringIO):
        """Keep file contents on close()"""

        def __init__(self, vf, *args, **kwargs):
            self.vf = vf
            super().__init__(vf.data, *args, **kwargs)

        def close(self):
            self.vf.data = self.getvalue()
            self.vf.io = None
            super().close()

    def __init__(self, test, name, modes, data=None):
        self.test = test
        self.name = name
        self.modes = modes
        self.data = None
        self.io = None 

    def open(self, mode, *args, **kwargs):
        """Open a virtual file, possibly overwriting contents.""" 
        if self.io is None: 
            self.io = SandboxFile.StringIOWrapper(self, *args, **kwargs)
            if mode == 'w' or mode == 'w+':
                self.io.truncate()
            elif mode == 'a':
                self.io.seek(0,2)
        else:
            raise self.test.fail(f"Attempted to open an already opened file: {self.name}")

    def close(self):
        """Close the stream but maitain the data."""
        if self.io is not None:
            self.io.close()
        else:
            self.test.fail(f"Attempted to close an already closed file: {self.name}")


class Sandbox:
    """A wrapper around test functions that prevents common mistakes from disrupting testing.""" 

    def __init__(self, test):
        """Initialize the wapper with a class that is based on unittest.TestCase and a function or class to wrap."""
        self.test = test
        self.files = {}
        self.inputs = []
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.instance = None

    def call(self, func, *args, **kwargs):
        """Execute the wrapped function."""
        try:            
            save_open = builtins.open
            save_input = builtins.input
            save_stdout = sys.stdout
            save_stderr = sys.stderr

            builtins.open = self._open
            builtins.input = self._input
            sys.stdout = self.stdout
            sys.stderr = self.stderr

            return func(*args, **kwargs)

        finally:
            builtins.open = save_open
            builtins.input = save_input
            sys.stdout = save_stdout 
            sys.stderr = save_stderr 
            self.stdout.flush()
            self.stderr.flush()

            # Verify that files are closed. 
            for file in self.files:
                if self.files[file].io is not None:
                    self.test.fail(f"""Your function exited and left {file} open.""")

    def open(self, name, mode='r', clientmodes=['r', 'w', 'r+', 'w+', 'a'], *args, **kwargs):
        """Open a virtual file. This is meant to be called from unittest code (not client code). 
        This function takes the same arguments as open with one additional argument: clientmodes. 
        The clientmodes argument is a list of modes that test code is allowed to open this file using. 
        The default allows the function under test to open a file with any mode. 

        Arguments:
            name - The file name 
            mode - The file mode passed to open (default: "r")
            clientmodes - The modes code under test will be able to use to open this file.

        Returns: A io.StringIO() to be used in place of the file. 
        """
        if name not in self.files:
            self.files[name] = SandboxFile(self.test, name, clientmodes)
        self.files[name].open(mode)
        return self.files[name].io

    def allow_open(self, name, clientmodes):
        """Allow the function under test to open a file. If open or allow_open are not executed 
        the function under test will fail if open() is used. This function explicitly allows the 
        function under test to write a file without having to first put data in it using TestCase.open()
        
        Arguments:
            name - The name of the file. 
            clientmodes - The modes code under test will be able to use to open this file.
        """
        if name not in self.files:
            self.files[name] = SandboxFile(self.test, name, clientmodes)
        self.files[name].modes = clientmodes

    def file_contents(self, filename):
        """Retrieve the contents of a virtual file. Useful to compare the contents of a file to 
        the expected contents.
        
        Arguments:
            name - The file name 
        
        Returns: The file contents.
        """ 

        if filename not in self.files or self.files[filename].data is None:
            self.test.fail(f"""Your function didn't create the file {filename}""")
        return self.files[filename].data 

    def allow_input(self, *args):
        """Allow the function under test to run the input() function some number of times. The 
        argument is a list of values to be returned by input(). When the list is exhausted the 
        function will fail when input() is run.

        Arguments:
            *args - A list of inputs. Appended to the existing list. 
        """
        self.inputs += args

    def expect(self, pattern):
        """Look in the function's stdout for a particular pattern. Fail if it is not found."""        
        stdout = self.stdout.getvalue()
        print(stdout)
        if re.match(pattern, stdout) is None:
            self.test.fail(f"""I expected to see {pattern} but it wasn't there.""")

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()

    def _open(self, filename, mode='r', *args, **kwargs):
        """The open function that is exposed to the function under test.""" 
        if filename not in self.files:
            self.test.fail(f"""Wrong filename in open: {filename} expected one of: {list(self.files.keys())}""")
        
        if mode not in self.files[filename].modes:
            self.test.fail(f"""Wrong file mode in open: {mode} expected one of: {self.files[filename].modes}""")

        self.files[filename].open(mode, *args, **kwargs)
        return self.files[filename].io

    def _input(self, prompt=None):
        """The input function that is exposed to the function under test."""
        if len(self.inputs) == 0:
            self.test.fail("""You should not use input in this function (or you've used it too many times).""")
        print(prompt, end="")
        return str(self.inputs.pop(0)) + '\n'

class FunctionSandbox:
    """A sandbox implementation for functions."""

    def __init__(self, test, func):
        self.sandbox = Sandbox(test)
        self.func = func 
    
    def __call__(self, *args, **kwargs):
        return self.sandbox.call(self.func, *args, **kwargs)

class ClassSandbox:
    """A sandbox implementation for a class and its methods."""

    def __init__(self, test, cls):
        self.sandbox = Sandbox(test)
        self.cls = cls 

    def __call__(self, *args, **kwargs):
        """Call the class constructor and wrap the instnace.""" 
        class _SandboxWrapper(self.cls):
            def __getattribute__(inner_self, name):
                attr = self.cls.__getattribute__(inner_self, name)
                if callable(attr):
                    def call_wrapper(*args, **kwargs):
                        return self.sandbox.call(attr, *args, **kwargs)
                    return call_wrapper
                return attr 

        return self.sandbox.call(_SandboxWrapper, *args, **kwargs)

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
        self.sandbox = Sandbox(test)
        self.app = app 

    @contextmanager
    def run(self):
        """Launch the server and wait for it to handle connections."""

        self.socket = f"{self.sandbox.test.tempdir.name}/flask.sock"
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
            self.sandbox.call(self.app.run, host=f"unix://{self.socket}", threaded=False)

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
                self.sandbox.test.fail("The Flask server never started!")

            if tries == 0:
                self.sandbox.test.fail("The Flask server never responded to a request!")

            yield FlaskSandbox.SandboxRequestor(self.sandbox.test, session, self.url)
                    
        finally:
            session.get(self.url.format('/shutdown'))
            app_thread.join()
