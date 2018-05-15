#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from main.website import *

db = SQLAlchemy(app)

from main.models.topic import Topic
from main.models.article import Article
from main.models.user import User
from main.models.site import Site
from main.models.friends import Friends


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


def check_login(password, telephone):
    user = User.query.filter_by(password=password, telephone=telephone).first()
    if user is not None:
        return True
    else:
        return False


def user_register(telephone, username, passsword, belong, xueid):
    user = User(telephone=telephone, username=username, passsword=passsword, belong=belong, xueid=xueid)
    user.save()
    if user.id > 0:
        return user
    else:
        return False


# 密码修改
def user_update(id, passsword):
    tmp = User.query.filter_by(id=id).first()
    if tmp is None:
        return False
    else:
        tmp.password = passsword
        tmp.update()
        return True


def select_user(telephone):
    user = User.query.filter_by(telephone=telephone).first()
    return user


def add_friend(userid, friend_tel):
    user_tmp = select_user(friend_tel)
    friend = Friends(userid, user_tmp.id, user_tmp.username, user_tmp.telephone, 1)
    friend.save()
    if friend.id > 0:
        return True
    else:
        return False


def select_friend(userid):
    friend = Friends.query.filter_by(userid=userid).all()
    return friend


# 好友删除
def delete_friend(friend_id):
    friend = Friends.query.filter_by(friend_id=friend_id).first()
    if friend is None:
        return False
    else:
        friend.delete()
        return True
