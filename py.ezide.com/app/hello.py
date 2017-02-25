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

@app.route("/downtown.svg")
def downtown():
    from downtown import process
    process.make_map()
    contents = file('/tmp/new_map/new_map.svg').read()
    resp = app.make_response(contents)
    resp.mimetype = 'image/svg+xml'
    return resp



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
