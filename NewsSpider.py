#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.website import app
from main.website import socketio

if __name__ == "__main__":
    # app.debug = app.config['DEBUG']
    # app.run(host='0.0.0.0', port=10086)
    socketio.run(app, host='0.0.0.0', port=10086)
