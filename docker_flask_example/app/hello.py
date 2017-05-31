#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
hello_app = Flask(__name__)

@hello_app.route("/")
def hello():
    return "Hello Strange World!"

@hello_app.route("/a/")
def a():
    return "Apples Armadillos!"


if __name__ == '__main__':
    hello_app.run(debug=True, host='0.0.0.0')
