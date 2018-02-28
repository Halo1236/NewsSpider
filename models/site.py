#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from models import db
from datetime import datetime


class Site(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    base_url = db.Column(db.String(100), nullable=False, index=True)
    site_url = db.Column(db.String(100), nullable=False, index=True)
    belong = db.Column(db.String(20), default='sqc', nullable=False)
    isnotice = db.Column(db.Boolean, nullable=True, default=False)
    tab_xpath = db.Column(db.String(255), nullable=False)
    td_xpath = db.Column(db.String(255), nullable=False)
    title_xpath = db.Column(db.String(255), nullable=False)
    url_xpath = db.Column(db.String(255), nullable=False)
    time_xpath = db.Column(db.String(255), nullable=False)
    content_xpath = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<site %r>' % self.base_url + self.site_url

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
