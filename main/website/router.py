#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from main.models import *
from flask import render_template, request, abort, json, jsonify, session, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit
import base64
import datetime


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@socketio.on('send_msg')
def send_msg(data):
    socketio.emit(data['to'], data)


@app.route('/api/article/data/<url>/json', methods=['GET'])
def article_data(url=None):
    if request.method == 'GET':
        if url == '' or url is None:
            return jsonify({'error': 'true', 'results': ''})
        else:
            articles = select_article_url(base64.b64decode(url))
            if articles is not None:
                dic = {
                    'id': articles.id,
                    'title': articles.title,
                    'img_url': articles.imgurl,
                    'article_url': articles.article_url,
                    'publish_time': articles.publish_time,
                    'publisher': articles.publisher,
                    'content': articles.content,
                    'create_time': articles.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
                print(articles.content)
                return jsonify({'error': 'false', 'results': dic})
            else:
                return jsonify({'error': 'true', 'results': {}})
    else:
        abort(404)


@app.route('/api/topic/data/<limit>/<page>/<isnotices>/json', methods=['GET'])
def topic_data(limit, page, isnotices):
    if request.method == 'GET':
        if limit == '0' and page == '0':
            return jsonify({'error': 'true', 'results': {}})
        else:
            topics = select_topic_limit(limit=int(limit), page=int(page) - 1, isnotices=isnotices)
            if topics is not None:
                article_list = []
                for topic_tmp in topics:
                    dic = {
                        'id': topic_tmp.id,
                        'title': topic_tmp.title,
                        'belong': topic_tmp.belong,
                        'article_url': topic_tmp.article_url,
                        'publish_time': topic_tmp.publish_time,
                        'isnotice': topic_tmp.isnotice,
                        'create_time': topic_tmp.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    article_list.append(dic)
                return jsonify({'error': 'false', 'results': article_list})
            else:
                return jsonify({'error': 'true', 'results': {}})
    else:
        abort(404)


@app.route('/api/user/<telephone>/json', methods=['GET'])
def user_data(telephone):
    if request.method == 'GET':
        if telephone is not None:
            tmp_user = select_user(telephone)
            if tmp_user is not None:
                dic = {
                    'id': tmp_user.id,
                    'username': tmp_user.username,
                    'telephone': tmp_user.telephone,
                    'belong': tmp_user.belong,
                    'xueid': tmp_user.xueid,
                }
                return jsonify({'error': 'false', 'results': dic})
            else:
                return jsonify({'error': 'true', 'results': {}})
    else:
        abort(404)


@app.route('/api/friend/<userid>/json', methods=['GET'])
def friend_data(userid):
    if request.method == 'GET':
        if userid is not None:
            friend = select_friend(int(userid))
            if friend is not None:
                friend_list = []
                for tmp_friend in friend:
                    dic = {
                        'id': tmp_friend.id,
                        'userid': tmp_friend.userid,
                        'friend_id': tmp_friend.friend_id,
                        'friend_name': tmp_friend.friend_name,
                        'friend_tel': tmp_friend.friend_tel,
                        'state': tmp_friend.state,
                    }
                    friend_list.append(dic)
                return jsonify({'error': 'false', 'results': friend_list})
            else:
                return jsonify({'error': 'true', 'results': {}})
    else:
        abort(404)


# 添加好友
@app.route('/api/add/friend/json', methods=['POST'])
def friend_add():
    if request.method == 'POST':
        userid = request.form.get('userid', None)
        friend_tel = request.form.get('friend_tel', None)
        if friend_tel is not None:
            if add_friend(userid, friend_tel):
                error = 'false'
            else:
                error = 'true'
            result = 'succeed' if error == 'false' else 'failed'
            return jsonify({'error': error, 'results': result})
        else:
            abort(404)


# 删除好友
@app.route('/api/delete/friend/<friend_id>/json', methods=['GET'])
def friend_id_delete(friend_id):
    if request.method == 'GET':
        if friend_id is not None:
            if delete_friend(int(friend_id)):
                error = 'false'
            else:
                error = 'true'
            result = 'succeed' if error == 'false' else 'failed'
            return jsonify({'error': error, 'results': result})
        else:
            abort(404)


# 登录
@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        telephone = request.form.get('telephone', None)
        password = request.form.get('password', None)
        tmp_user = check_login(password, telephone)
        if tmp_user is False:
            error = 'true'
        else:
            error = 'false'
        result = 'succeed' if error == 'false' else 'failed'
        return jsonify({'error': error, 'results': result})
    else:
        abort(404)


# 注册
@app.route('/api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        telephone = request.form.get('telephone', None)
        xueid = request.form.get('xueid', None)
        belong = request.form.get('belong', None)
        if user_register(telephone, username, password, belong, xueid):
            error = 'false'
        else:
            error = 'true'
        result = 'succeed' if error == 'false' else 'failed'
        return jsonify({'error': error, 'results': result})
    else:
        abort(404)


# 密码修改
@app.route('/api/update_user', methods=['POST'])
def update_user():
    if request.method == 'POST':
        userid = request.form.get('userid', None)
        password = request.form.get('password', None)
        if user_update(userid, password):
            error = 'false'
        else:
            error = 'true'
        result = 'succeed' if error == 'false' else 'failed'
        return jsonify({'error': error, 'results': result})
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    # app.logger.error('404', (error))
    return "page not found!", 404


@app.errorhandler(Exception)
def unhandled_exception(error):
    print(error)
    # app.logger.error('Unhandled Exception:%s', (error))
    return "Error", 500
