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

    hello_app = Flask(__name__)

    @hello_app.route('/')
    def index():
        return "Welcome"
    
    @hello_app.route('/hello')
    def hello():
        return 'Hello'

    def test_1_hello_app(self):
        """Testing Flask application hello_app"""
        app = self.sandbox(self.test_hasattr)
        with app.run() as session:
            r = session.get("/", status=200)
            if r.text != "Welcome":
                self.fail(f"""You didn't say "Welcome" on the default route.""")
    
            r = session.get("/hello", status=200)
            if r.text != "Hello":
                self.fail(f"""Your hello routed said the wrong thing: {r.text}""")

            r = session.get('/def_not_here', status=404)
