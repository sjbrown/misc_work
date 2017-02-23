#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Strange World!"

@app.route("/a/")
def a():
    return "Apples Armadillos!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
