"""
A testbank of Flask questions (experimental)
"""

import sys
import random
import threading
import time
import requests 
import requests_unixsocket

from p4e import testlib 
from flask import Flask, request

class SimpleFlask(testlib.TestCase):
    """
    Write a Flask program called ``hello_app``. The program should have two routes:

      - ``/`` - The default route, returns the word "Welcome"
      - ``/hello`` - Returns the word "Hello"
    """

    test_hasattr = "hello_app"

    solution = Flask(__name__)

    @solution.route('/')
    def index():
        return "Welcome"
    
    @solution.route('/hello')
    def hello():
        return "Hello"

    def test_01_test_routes(self):
        
        app = self.sandobx_flask(self.test_hasattr)
        with app.run() as session:
            r = session.get("/")
            if r.status_code != 200:
                self.fail(f"""Failed on the index route. The response was: {r.text}""")
            if r.text != "Welcome":
                self.fail(f"""You didn't say "Welcome" on the default route.""")

            r = session.get("/hello")
            if r.status_code != 200:
                self.fail(f"""Failed on the index route. The response was: {r.text}""")
            if r.text != "Hello":
                self.fail(f"""You didn't say "Welcome" on the default route.""")
