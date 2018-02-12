#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from models.topic import Topic

MAIN_URL = u'http://www.sqc.edu.cn'

NEWS_PATH = u'/article-list-157-s52102500_start-%d.html'


class News_spider(object):

    MAIN_URL = u'http://www.sqc.edu.cn'

    NEWS_PATH = u'/article-list-157-s52102500_start-%d.html'

    data = {}
    driver = None
    page = 1
    need_save = True
    item = []

    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome()

    def start(self):
        topic = Topic.query.all()

        if topic is None:
            self.crawlAll(MAIN_URL + NEWS_PATH)
        else:
            pass

    def crawlAll(self, url):
        index = (self.page - 1) * 14
        self.driver.get(url % index)

if __name__ == '__main__':
    topic = News_spider()
    topic.start()
