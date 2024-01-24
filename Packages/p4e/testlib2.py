"""
Helper functions for test cases. NEW

Author: Mike Matera
"""

import sys
import tempfile
import traceback
import subprocess 

from pathlib import Path
from jinja2 import Template 
from IPython.display import display, HTML 

def run_exam(solution):
    with tempfile.TemporaryDirectory() as temp:
        sfile = Path(temp) / 'solution.py'
        with open(sfile, 'w') as s:
            s.write(solution)
        
        url = 'https://storage.googleapis.com/p4e-resoureces/checker'
        checker = 'checker-binary'
        subprocess.run(f'wget -O {checker} {url}', shell=True, stderr=subprocess.DEVNULL, cwd=temp)
        subprocess.run(f'chmod u+x ./{checker}', shell=True, cwd=temp)

        proc = subprocess.run(f'./{checker} {sfile}', 
                            shell=True, stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, encoding='utf-8', 
                            cwd=temp)
        checker_feedback = f"""
        <h3>Checker Output</h3>
        <pre>{proc.stderr} {proc.stdout}</pre>
        <h3>Graded Code:</h3>
        <div style="margin-left:2em;"><pre>{solution}</pre></div>
        """
        return checker_feedback


class HTMLTestResult:
    """A way to render tests nicely."""

    def __init__(self):
        self.name = " "
        self.description = None 
        self.label = None
        self.style = None
        self.message = None

    def _ipython_display_(self):
        with open(Path(__file__).parent / "templates" / "single.html") as t:
            template = Template(t.read())
        display(HTML(template.render(
            result=self,
        )))

class NBTestSuite:
    """A simplified test suite for testing in notebooks."""

    def __init__(self):
        """Create a new suite."""
        self.cases = []
        self.results = []
        self.stop = False

    def run(self):
        """Run all the test cases."""
        for case in self.cases:
            result, cont = case()
            display(result)
            if not cont:
                break

    def check(self, condition, message):
        """Fail fast with the message if the condition is false."""
        def do_assert():
            tr = HTMLTestResult()
            if condition:
                tr.style = 'success'
                tr.label = 'PASS'
                tr.description = message
                cont = True
            else:
                tr.style = 'danger'
                tr.label = 'FAIL'
                tr.description = message
                cont = False
            return tr, cont
        self.cases.append(do_assert)

    def sourcetest(self, source, module='__main__'):
        """Decorator for a test function that tests a code string."""
        assert module in sys.modules, f"""Invalid module given: {module}"""
        mod = sys.modules[module]
        exe = lambda: exec(source, mod.__dict__)
        def deco(test):
            def wrapper():
                tr = HTMLTestResult()
                tr.name = test.__name__
                tr.description = test.__doc__
                try:
                    test(exe)
                    tr.style = 'success'
                    tr.label = 'PASS'
                except AssertionError as e:
                    tr.style = 'danger'
                    tr.label = 'FAIL'
                    tr.message = str(e)
                except Exception as e:
                    tr.style = 'danger'
                    tr.label = 'FAIL'
                    exc_info = sys.exc_info()
                    tb_e = traceback.TracebackException(*exc_info)
                    tr.message = f"""{str(exc_info[1])}\n{"".join(list(tb_e.format()))}"""
                return tr, True
            self.cases.append(wrapper)
            return wrapper
        return deco 

    def functest(self, funcname, module='__main__'):
        """Decorator for a test case of a student function."""
        assert module in sys.modules, f"""Invalid module given: {module}"""
        mod = sys.modules[module]
        def deco(test):
            def wrapper():
                tr = HTMLTestResult()
                tr.name = test.__name__
                tr.description = test.__doc__
                try:
                    assert hasattr(mod, funcname), \
                        f"""The function {module}.{funcname} is not defined."""
                    func = getattr(mod, funcname) 
                    assert func.__doc__ is not None, \
                        f"""The function {module}.{funcname} has no docstring."""

                    test()
                    tr.style = 'success'
                    tr.label = 'PASS'
                except AssertionError as e:
                    tr.style = 'danger'
                    tr.label = 'FAIL'
                    tr.message = str(e)
                except Exception as e:
                    tr.style = 'danger'
                    tr.label = 'FAIL'
                    exc_info = sys.exc_info()
                    tb_e = traceback.TracebackException(*exc_info)
                    tr.message = f"""{str(exc_info[1])}\n{"".join(list(tb_e.format()))}"""
                return tr, True
            self.cases.append(wrapper)
            return wrapper
        return deco 
