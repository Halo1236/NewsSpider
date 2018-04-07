#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, instance_relative_config=True)
app.wsgi_app = ProxyFix(app.wsgi_app)
# 加载配置
# app.config.from_object('config')
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']

# 记录日志
# logger = logging.getLogger("newslog")
# handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=7)
# handler.setLevel(logging.WARNING)
# handler.setFormatter(
#    logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))

# logger.addHandler(handler)

from main.website import router
