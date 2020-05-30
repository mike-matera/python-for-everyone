"""
A Sandbox for student code. 
"""

import io
import re
import sys
import time
import builtins
from contextlib import contextmanager
from pathlib import Path
import threading
import requests 
import requests_unixsocket
from flask import Flask, request
from werkzeug.exceptions import HTTPException

class Sandbox:
    """A wrapper around test functions that prevents common mistakes from disrupting testing.""" 

    def __init__(self, test):
        """Initialize the wapper with a class that is based on unittest.TestCase and a function or class to wrap."""
        self.test = test
        self.inputs = []
        self.files = {}
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self.instance = None
        self.save_open = None
        self.save_input = None 
        self.save_stdout = None
        self.save_stderr = None 

    def call(self, func, *args, **kwargs):
        """Execute the wrapped function."""
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
            self.save_stdout = sys.stdout
            self.save_stderr = sys.stderr

            builtins.open = self._open
            builtins.input = self._input
            sys.stdout = self.stdout
            sys.stderr = self.stderr

            rval = func(*args, **kwargs)
            if checktype is not None and not isinstance(rval, checktype):
                self.test.fail(f"""Your function was supposed to return {checktype.__name__} but returned {rval.__class__.__name__} instead.""")

            return rval

        except Exception as e: 
            rval = e 
            raise e 
                    
        finally:
            builtins.open = self.save_open
            builtins.input = self.save_input
            sys.stdout = self.save_stdout 
            sys.stderr = self.save_stderr 
            self.stdout.flush()
            self.stderr.flush()

            # Verify that files are closed. 
            for file in self.files:
                if not self.files[file].closed:
                    self.test.fail(f"""Your function exited and left {file} open.""")

            # Add me to the trace log. 
            self.test.trace.append((func.__name__, (args, kwargs), rval))

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
        filepath = Path(filename)
        tempdir = Path(self.test.tempdir.name) 
        
        if filepath.is_absolute():
            try:
                filepath = filepath.relative_to(tempdir)
            except:
                self.test.fail(f"""You should not open a file using an absolute path: {filename}""")

        fh = self.save_open(tempdir / filepath, mode, *args, **kwargs)
        self.files[filename] = fh

        return fh

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
