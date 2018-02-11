#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('404', (error))
    return "page not found!", 404


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception:%s', (error))
    return "Error", 500


if __name__ == '__main__':
    app.run()
