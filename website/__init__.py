#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

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
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(
    logging.Formatter(datefmt='%Y-%m-%d %H:%M:%S',
                      fmt='%(color)s[%(levelname)1.1s ' '%(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'))

handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

from website import router

# from spider.news_spider import News_spider
#
# topic = News_spider()
# topic.start()
