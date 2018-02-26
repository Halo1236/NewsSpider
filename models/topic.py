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
    belong = db.Column(db.String(20), default='sqc', index=True)
    article_url = db.Column(db.String(100), unique=True, nullable=False)
    publish_time = db.Column(db.String(20), index=True)
    isnotice = db.Column(db.Boolean, default=False, nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, title, url, publish_time, isnotice, belong):
        self.publish_time = publish_time
        self.title = title
        self.article_url = url
        self.isnotice = isnotice
        self.belong = belong

    def __repr__(self):
        return '<topic_id %r>' % self.title

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
