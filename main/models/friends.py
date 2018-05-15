#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import db


class Friends(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userid = db.Column(db.Integer, nullable=False, index=True)
    friend_id = db.Column(db.Integer, index=True)
    friend_name = db.Column(db.String(32))
    friend_tel = db.Column(db.String(32), index=True)
    state = db.Column(db.Integer, default=1, nullable=False)

    def __init__(self, userid, friendid, friendname, friend_tel, state):
        self.userid = userid
        self.friend_tel = friend_tel
        self.friend_id = friendid
        self.friend_name = friendname
        self.state = state

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
