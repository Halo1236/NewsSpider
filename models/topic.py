#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import db
from datetime import datetime


class Topic(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), unique=True, nullable=False, index=True)
    article_url = db.Column(db.String(100), unique=True, nullable=False)
    publish_time = db.Column(db.String(20), index=True)
    create_time = db.Column(db.DateTime, default=datetime.now,nullable=False)

    def __init__(self, title, url,publish_time):
        self.publish_time = publish_time
        self.title = title
        self.article_url = url

    def __repr__(self):
        return '<topic_id %r>' % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self
