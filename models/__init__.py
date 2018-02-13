#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from website import *
import MySQLdb
db = SQLAlchemy(app)

from models.topic import Topic
from models.article import Article
from models.user import User
