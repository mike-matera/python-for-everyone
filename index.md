# Python for Everyone

This is documentation for how to operate an introduction to Python class using my infrastrucutre. There are three parts of the infrastructure that you might find useful. 

  1. The Notebooks. They are designed to be used instead of a textbook. 
  2. Notebook extras. Functions (like the Pen) that make for a richer learning experience. 
  3. Unittest infrastructure and testbanks. 

## Setup 

The [README](README) shows you how to setup this repository on your own machine. 

## Jupyter Notebooks 

The Jupyter notebooks are orgnized into LessonXX directories. The ``welcome.ipynb`` notebook in the root directory is designed to be a landing page for students to navigate the course. 

```eval_rst
.. toctree::
    :glob:

    welcome
```

## Turtle Graphics in Jupyter

The p4e package contains a class that can be used in a notebook to draw simple graphics on a canvas. The commands are similar to the [Logo Programming Language](https://en.wikipedia.org/wiki/Logo_(programming_language)). Drawing shapes line by line is a good way to learn about algorithms and a visual way to see the action of a program. 

There are examples of how to use the pen in the following notebooks: 

  - [Using the Pen](./Lesson02/using_the_pen)
  - [Algorithms](./Lesson02/algorithms)

```eval_rst
.. automodule:: p4e.drawing
   :members:
```

## Unittest Infrastructure 

Students benefit from rapid feedback on the correctness of their code and correct code is easier to grade and give useful feedback on. I have used various systems for testing student code and found that that it has unique challenges. Typical unit tests are not a good fit because student's code has to be tested defensively. Students are learning to program and make mistakes that are not common for programmers. Test cases need an additional level of sanity checking to ensure proper execution and should provide useful feedback leading to a lot of repetitive code. This repository contains tools to help teachers write effective and simple unit tests that benefit learning and make grading more reliable and less exhausting. 

### Writing Test Cases

There are two ways to run tests in Python: 

1. By running the test program and interacting with it as a separate process. 
2. By importing the test program and running functions directly. 

I use both in my class. Once students start writing code with functions it helps them to have more granular feedback on particular functions. This guide will show you how to write both kinds of test cases. 

### Testing With ``pexpect``

The ``pexpect`` functions are useful for testing the operation of a whole program. Test cases must contain the ``test_file`` member that communicates to the test fixture what file to open. If the file is missing the test case will be skipped and the user alerted. Here's an example of a simple test case:

```python
from p4e.testlib import TestCase, run

class SimpleTest(TestCase):

   test_file = 'assignment.py'
      
   def test_1_for_docstring(self):
      """Looking for the docstring"""
      self.check_docstring(regex=r'(?i)cis-15')
      
   def test_2_check_output(self):        
      """Looking for output in your program."""
      with self.spawn() as test:
            self.expect("Hello World")

run()
```

A temporary directory is created before every test and cleaned up after every test 
finishes. The open function is provided so that implementers can write into the temporary
directory without knowing its path. For example:

```python
with self.open('myfile.txt') as f:
   f.write('Some stuff')
```

The file `myfile.txt` will appear in the working directory of the executed program. Programs
are started using the spawn() function, which returns a pexpect `spawn` object and can be 
used as a context manager:

```python
with self.spawn(args...) as test:
   self.expect('suff')
   ...
   self.sendline('other-stuff')
```

Using the built-in spawn function ensures proper handling of the working directory and 
guarantees that the session will be visible in the output of an error or failure. 

### The Sandbox

It's important to test functions in isolation. In principle Python makes this very easy, 
but student functions must be seen as more adversarial than normal ones. For example, a 
function that uses `input()` when it's not supposed to will freeze the test case and be a 
pain. Functions can also overwrite files causing confusion. The Sandbox prevents common 
mistakes and extends the reach of unit tests to help students diagnose problems more quickly
and with less frustration. 

A sandbox is created with the `sandbox_function()` function. The returned value is a callable
that will execute the wrapped function in a sandbox. The sandbox has the following properties:

1. Wrapping `sys.stdout` - Anything written to stdout will be contained in an `io.StringIO` 
   available to test code. 
2. Wrapping `input()` - Code under test will receive supplied values on `input()` or take an 
   exception. 
3. Wrapping `open()` - Code under test works on virtual files that can be accessed and limited
   by the test harness. This abstraction is not complete, but it's useful to construct guard
   rails on client code. 

.. autoclass:: p4e.testlib.TestCase
   :members:

## Testbanks

A test question is as a Python ``uinttest.TestCase``. The test case has a docstring that's rendered by Sphinx into HTML. The HTML is suitable to be copy-and-pasted into Canvas or any other document or LMS. The test cases can be run against a student's answer to give them feedback as to how well they answered the question. 

### Easy Questions 

```.. automodule:: p4e.testbanks.testbank_easy
   :members:
```

### Questions Using ``input()``

```.. automodule:: p4e.testbanks.testbank_input
   :members:
```

### Questions Using File I/O

```.. automodule:: p4e.testbanks.testbank_files
   :members:
```
### Questions Using Lists

```.. automodule:: p4e.testbanks.testbank_lists
   :members:
```
### Questions Using Loops

```.. automodule:: p4e.testbanks.testbank_loops
   :members:
```
### Questions Using Dictionaries

```.. automodule:: p4e.testbanks.testbank_dicts
   :members:
```
### Questions Using Classes

```.. automodule:: p4e.testbanks.testbank_classes
   :members:
```
### Questions Using Flask

```.. automodule:: p4e.testbanks.testbank_flask
   :members:
```
