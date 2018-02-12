#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import db


class User(db.Model):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isadmin = db.Column(db.Integer, nullable=False, default=0, index=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, isadmin, username, passsword):
        self.isadmin = isadmin
        self.username = username
        self.password = passsword

    def __repr__(self):
        return '<user_id %r>' % self.username

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
