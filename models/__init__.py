#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from website import app
import pymysql
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)

from models.topic import Topic
from models.article import Article
from models.user import User
