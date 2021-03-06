#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import db


class User(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isadmin = db.Column(db.Integer, nullable=False, default=0, index=True)
    telephone = db.Column(db.String(32), nullable=False, unique=True, index=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    password = db.Column(db.String(64), nullable=False)
    belong = db.Column(db.String(64), nullable=True)
    xueid = db.Column(db.String(64), nullable=False, default='000000')

    def __init__(self, telephone, username, passsword, belong, xueid):
        self.telephone = telephone
        self.username = username
        self.password = passsword
        self.belong = belong
        self.xueid = xueid

    def __repr__(self):
        return '<user_id %r>' % self.id

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
