#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from main.models import *
from flask import render_template, request, abort, jsonify, session, redirect, url_for, send_from_directory
import base64


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@app.route('/api/article/data/<url>/json', methods=['GET'])
def article_data(url=None):
    if request.method == 'GET':
        if url == '' or url is None:
            return jsonify({'error': 'true', 'results': ''})
        else:
            articles = select_article_url(base64.b64decode(url))
            print(articles.content)
            return jsonify({'error': 'false', 'results': ''})
    else:
        abort(404)


@app.route('/api/notices/data/<limit>/<page>/json', methods=['GET'])
def news_data(limit, page):
    if request.method == 'GET':
        if limit == '0' and page == '0':
            print(limit)
            return jsonify({'error': 'true', 'results': ''})
        else:
            return jsonify({'error': 'false', 'results': ''})
    else:
        abort(404)


@app.route('/api/topic/data/<limit>/<page>/<isnotices>/json', methods=['GET'])
def topic_data(limit, page, isnotices):
    if request.method == 'GET':
        if limit == '0' and page == '0':
            return jsonify({'error': 'true', 'results': ''})
        else:
            topics = select_topic_limit(limit=int(limit), page=int(page) - 1, isnotices=isnotices)
            if topics is not None:
                for topic in topics:
                    print(topic.title)
                return jsonify({'error': 'false', 'results': '1'})
            else:
                return jsonify({'error': 'false', 'results': ''})
            return jsonify({'error': 'false', 'results': ''})
    else:
        abort(404)


@app.route('/api/login', methods=['POST'])
def log_in():
    if request.method == 'POST':
        stu_id = request.form.get('userid', None)
        stu_name = request.form.get('username', None)
        session['userid'] = stu_id
        session['username'] = stu_name
        if check_login(stu_id, stu_name):
            error = 'false'
        else:
            error = u'true'
        result = 'succeed' if error == 'false' else 'failed'
        return jsonify({'error': error, 'login': result})
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    # app.logger.error('404', (error))
    return "page not found!", 404


@app.errorhandler(Exception)
def unhandled_exception(error):
    # app.logger.error('Unhandled Exception:%s', (error))
    return "Error", 500
