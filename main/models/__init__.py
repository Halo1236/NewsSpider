#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from main.website import *

db = SQLAlchemy(app)

from main.models.topic import Topic
from main.models.article import Article
from main.models.user import User
from main.models.site import Site


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


def select_article_url(articleurl):
    articles = Article.query.filter_by(article_url=articleurl).first()
    return articles


def select_topic_limit(limit, page, isnotices):
    topics = Topic.query.filter_by(isnotice=isnotices).order_by(Topic.publish_time.desc()).limit(limit).offset(
        limit * page).all()
    return topics


def check_login(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user is not None:
        if user.isadmin == 1:
            return 1, True
        else:
            return 0, True
    else:
        return 0, False
