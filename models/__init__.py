#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from website import *
import MySQLdb

db = SQLAlchemy(app)

from models.topic import Topic
from models.article import Article
from models.user import User
from models.site import Site


def find_by_title(title, url):
    topic = Topic.query.filter_by(title=title, article_url=url).first()
    if topic is None:
        return True
    else:
        return False


def insert_topic_to_db(title, url, publisher_time, isnotice, belong):
    topic = Topic(title=title, url=url, publish_time=publisher_time, isnotice=isnotice, belong=belong)
    topic.save()


def insert_article_to_db(tite, publisher, publish_time, html_content, datas1, url):
    article = Article(tite, publisher, publish_time, html_content, datas1, url)
    article.save()


def find_all_site():
    site = Site.query.all()
    # site = Site.query.filter_by(belong='sie')
    if site is None:
        return None
    else:
        return site