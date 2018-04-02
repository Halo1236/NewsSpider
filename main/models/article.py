#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import db
from datetime import datetime


class Article(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_url = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(100), unique=True, nullable=False, index=True)
    publish_time = db.Column(db.String(100), nullable=False, index=True)
    publisher = db.Column(db.String(100), nullable=True)
    imgurl = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text(4095), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, title, publisher, publish_time, content, imgurl, url):
        self.title = title
        self.article_url = url
        self.publisher = publisher
        self.publish_time = publish_time
        self.content = content
        self.imgurl = imgurl

    def __repr__(self):
        return '<article_id %r>' % self.title

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        return self

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return self
