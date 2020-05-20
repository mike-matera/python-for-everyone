.. Python for Everyone documentation master file, created by
   sphinx-quickstart on Tue May 19 18:43:27 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python for Everyone
===================

This is documentation for how to operate an introduction to Python class using my infrastrucutre. There are three parts of the infrastructure that you might find useful. 

  1. The Notebooks. They are designed to be used instead of a textbook. 
  2. Notebook extras. Functions (like the Pen) that make for a richer learning experience. 
  3. Unittest infrastructure and testbanks. 


Jupyter Notebooks 
=================

The Jupyter notebooks are orgnized into LessonXX directories. The ``welcome.ipynb`` notebook in the root directory is designed to be a landing page for students to navigate the course. 

.. toctree::
    :glob:

    welcome


Testbanks
=========

A test question is as a Python ``uinttest.TestCase``. The test case has a docstring that's rendered by Sphinx into HTML. The HTML is suitable to be copy-and-pasted into Canvas or any other document or LMS. The test cases can be run against a student's answer to give them feedback as to how well they answered the question. 

.. toctree::
   :maxdepth: 4

   testbanks


